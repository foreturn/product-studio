import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { basename, dirname, join, relative as relativePath, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const PROJECT_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const SKILLS_ROOT = join(PROJECT_ROOT, "skills");

const EXPECTED_SKILLS = [
  "product-management",
  "software-architecture",
  "backend-engineering",
  "web-engineering",
  "android-engineering",
  "ios-engineering",
  "database-engineering",
  "platform-engineering",
  "security-engineering",
  "quality-engineering",
  "release-engineering",
];
const REMOVED_SKILLS = [
  "product-experience",
  "frontend-engineering",
  "fact-sync",
];
const REMOVED_FACT_BOOKS = [
  "design.md",
  "architecture.md",
  "backend.md",
  "frontend.md",
  "product-experience.md",
  "verification.md",
  "release.md",
];
const REMOVED_RUNTIME_ASSETS = [
  "hooks",
  "hooks/hooks.json",
  "scripts/terminal-hook.mjs",
  "tests/terminal-hook.test.mjs",
  "tests/fixtures/terminal-envelope.json",
  "references/terminal-protocol.md",
];

const SKILL_HEADINGS = [
  "目标",
  "执行协议",
  "输出契约",
  "完成条件",
  "停止条件",
  "权限与边界规则",
  "参考资料",
  "项目记忆",
];
const PRINCIPLE_HEADINGS = [
  "能力索引",
  "专业约束",
];
const PROHIBITED_PRINCIPLE_FIELDS = [
  "决策对象",
  "必需输入",
  "判断方法",
  "实施要求",
  "输出契约",
  "验证证据",
  "专业边界",
  "常见误判",
  "适用场景",
  "选择规则",
  "具体做法",
  "反模式",
  "验收要点",
];
const MEMORY_HEADINGS = ["核心记忆"];
const LEGACY_MEMORY_PATTERNS = [
  ["shared terminal protocol", /terminal-protocol\.md|终态记忆协议/],
  ["terminal-memory wording", /终态记忆|terminal-memory/],
  [
    "admission-gate schema",
    /^(?:##|###)\s+(?:通用入册门禁|动作语义|结果语义)\s*$|^-\s+\*\*(?:入册条件|主题合并键|当前事实写法|变更规则|排除项)\*\*[：:]/m,
  ],
  [
    "memory action or result schema",
    /(?:事实动作|记忆动作|动作(?:仍)?只有|结果优先级|互斥结果|每个\s+Owner.{0,20}结果).{0,160}\b(?:ADD|UPDATE|DELETE|NO_CHANGE|SYNCED|DEFERRED|BLOCKED)\b/s,
  ],
];
const FIXED_ORCHESTRATION_PATTERNS = [
  /(?:必须|应当|需要).{0,24}(?:先|后|再).{0,36}(?:Skill|技能)/,
  /(?:Skill|技能).{0,36}(?:移交|调用|退回|后继|前置)/,
  /下一(?:项|个)?\s*(?:Skill|技能)/,
  /固定技能链/,
  /\b(?:must|required)\b.{0,80}\b(?:invoke|handoff|route to|call)\b/i,
];

const errors = [];

function relative(path) {
  return path.slice(PROJECT_ROOT.length + 1).replaceAll("\\", "/");
}

function fail(path, message) {
  errors.push(`${relative(path)}: ${message}`);
}

function read(path) {
  if (!existsSync(path)) {
    fail(path, "missing required file");
    return "";
  }
  return readFileSync(path, "utf8");
}

function headings(markdown, level) {
  const prefix = "#".repeat(level);
  return [...markdown.matchAll(new RegExp(`^${prefix} (.+)$`, "gm"))].map(
    (match) => match[1].trim(),
  );
}

function assertExactHeadings(path, markdown, expected) {
  const actual = headings(markdown, 2);
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    fail(
      path,
      `level-two headings must be exactly ${expected.join(" | ")}; found ${actual.join(" | ")}`,
    );
  }
}

function frontmatter(markdown) {
  const match = markdown.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  return match?.[1] ?? "";
}

function section(markdown, heading) {
  const lines = markdown.split(/\r?\n/);
  const start = lines.findIndex((line) => line.trim() === `## ${heading}`);
  if (start === -1) return "";
  const endOffset = lines
    .slice(start + 1)
    .findIndex((line) => line.startsWith("## "));
  const end = endOffset === -1 ? lines.length : start + 1 + endOffset;
  return lines.slice(start + 1, end).join("\n");
}

function blocks(markdown, parentHeading) {
  return section(markdown, parentHeading)
    .split(/^### /m)
    .slice(1)
    .map((block) => {
      const newline = block.indexOf("\n");
      return {
        title: (newline === -1 ? block : block.slice(0, newline)).trim(),
        body: newline === -1 ? "" : block.slice(newline + 1),
      };
    });
}

function numberedIndex(markdown, parentHeading) {
  return [...section(markdown, parentHeading).matchAll(/^\d+\.\s+(.+)$/gm)].map(
    (match) => match[1].trim(),
  );
}

function assertConstraintLists(path, entries) {
  if (entries.length < 8 || entries.length > 16) {
    fail(path, `must define 8-16 broad professional constraint categories; found ${entries.length}`);
  }
  for (const entry of entries) {
    const lines = entry.body
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter(Boolean);
    const practices = lines.filter((line) => /^- (?!\*\*)\S/.test(line));
    if (lines.length !== practices.length) {
      fail(path, `constraint category "${entry.title}" must contain only plain bullets`);
    }
    if (practices.length < 4 || practices.length > 8) {
      fail(path, `constraint category "${entry.title}" must contain 4-8 general constraint bullets; found ${practices.length}`);
    }
    for (const practice of practices) {
      if (practice.slice(2).trim().length < 15) {
        fail(path, `constraint category "${entry.title}" contains an underspecified rule: ${practice}`);
      }
    }
  }
}

function assertCoreMemoryLists(path, entries) {
  if (entries.length < 5 || entries.length > 9) {
    fail(path, `must define 5-9 core memory topics; found ${entries.length}`);
  }
  if (new Set(entries.map((entry) => entry.title)).size !== entries.length) {
    fail(path, "core memory topic titles must be unique");
  }
  for (const entry of entries) {
    const lines = entry.body
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter(Boolean);
    const memories = lines.filter((line) => /^- (?!\*\*)\S/.test(line));
    if (lines.length !== memories.length) {
      fail(path, `core memory topic "${entry.title}" must contain only plain bullets`);
    }
    if (memories.length < 1 || memories.length > 3) {
      fail(path, `core memory topic "${entry.title}" must contain 1-3 bullets; found ${memories.length}`);
    }
    for (const memory of memories) {
      if (memory.slice(2).trim().length < 15) {
        fail(path, `core memory topic "${entry.title}" contains an underspecified item: ${memory}`);
      }
      if (!memory.startsWith("- 记住")) {
        fail(path, `core memory topic "${entry.title}" must state what to remember: ${memory}`);
      }
    }
  }
}

function rejectLegacyMemoryContract(path, markdown) {
  for (const [label, pattern] of LEGACY_MEMORY_PATTERNS) {
    if (pattern.test(markdown)) {
      fail(path, `must not retain ${label}`);
    }
  }
}

function assertAutonomousOrchestration(path, markdown, skill) {
  for (const pattern of FIXED_ORCHESTRATION_PATTERNS) {
    if (pattern.test(markdown)) {
      fail(path, `must not encode fixed cross-skill orchestration (${pattern})`);
    }
  }
  for (const match of markdown.matchAll(/\$([a-z][a-z-]+)/g)) {
    if (match[1] !== skill) {
      fail(path, `must not invoke another skill ($${match[1]})`);
    }
  }
  for (const removed of REMOVED_SKILLS) {
    if (markdown.includes(removed)) {
      fail(path, `must not reference removed skill ${removed}`);
    }
  }
}

function validateSkill(skill) {
  const root = join(SKILLS_ROOT, skill);
  const skillPath = join(root, "SKILL.md");
  const principlesPath = join(root, "references", "principles.md");
  const memoryPath = join(root, "references", "memory.md");
  const agentPath = join(root, "agents", "openai.yaml");
  const skillDoc = read(skillPath);
  const principles = read(principlesPath);
  const memory = read(memoryPath);
  const agent = read(agentPath);

  if (!skillDoc || !principles || !memory || !agent) return;

  const metadata = frontmatter(skillDoc);
  if (!new RegExp(`^name:\\s*${skill}$`, "m").test(metadata)) {
    fail(skillPath, `frontmatter name must be ${skill}`);
  }
  if (!/^description:\s*\S.+$/m.test(metadata)) {
    fail(skillPath, "frontmatter must contain a non-empty description");
  }
  assertExactHeadings(skillPath, skillDoc, SKILL_HEADINGS);
  if (/^### /m.test(skillDoc)) {
    fail(skillPath, "SKILL.md must not expand professional capabilities");
  }
  if (PROHIBITED_PRINCIPLE_FIELDS.some((field) => skillDoc.includes(`**${field}**`))) {
    fail(skillPath, "labeled professional capability fields are not allowed");
  }
  const executionSection = section(skillDoc, "执行协议");
  const executionItems = executionSection.match(/^\d+\.\s+.+$/gm) ?? [];
  if (executionItems.length !== 6) {
    fail(skillPath, "execution protocol must contain exactly six ordered contract steps");
  }
  for (const [label, pattern] of [
    ["fact-book identity resolution", /唯一确认目标 Git 根与 `product-id`/],
    ["project memory loading", /阅读.*项目记忆/],
    ["owner fact-book loading", new RegExp(`docs/product-studio/<product-id>/${skill}\\.md`)],
    ["core-memory maintenance", /核心认知.*更新或移除/],
  ]) {
    if (!pattern.test(executionSection)) {
      fail(skillPath, `execution protocol must cover ${label}`);
    }
  }
  for (const token of [
    "references/principles.md",
    "能力索引",
    "references/memory.md",
  ]) {
    if (!skillDoc.includes(token)) {
      fail(skillPath, `execution contract must reference ${token}`);
    }
  }
  const projectMemorySection = section(skillDoc, "项目记忆");
  for (const [label, pattern] of [
    ["fact-book identity resolution", /唯一确认目标 Git 根与 `product-id`/],
    ["unsafe identity boundary", /归属不唯一或名称不安全时不猜测或创建事实册/],
    ["identity evidence", /用户范围.*产品入口与元数据.*相关项目根.*目标代码.*调用链/],
    ["safe single-level product id", /`product-id`.*仓库内唯一、稳定.*安全单级目录名/],
    ["pre-work loading", /工作前读取/],
    ["core-memory definition loading", /读取 `references\/memory\.md` 中本次命中的核心主题/],
    ["owner fact-book locator", new RegExp(`docs/product-studio/<product-id>/${skill}\\.md`)],
    ["current-authority precedence", /以当前权威为准/],
    ["core-memory focus", /持续影响后续判断.*难从局部代码直接看清/],
    ["source-inventory exclusion", /不复制源码、配置或可生成清单/],
    ["stale-memory maintenance", /更新或移除旧内容/],
    ["current-facts only", /只保留当前仍成立的事实/],
    ["write-authority boundary", /不得因本节扩大写入范围/],
    ["secret exclusion", /秘密/],
    ["user-data exclusion", /用户数据/],
    ["task-process exclusion", /任务过程/],
    ["one-off-result exclusion", /一次性结果/],
  ]) {
    if (!pattern.test(projectMemorySection)) {
      fail(skillPath, `project memory prompt must cover ${label}`);
    }
  }
  for (const token of ["非 `.` 或 `..`", "不含 `/` 或 `\\`"]) {
    if (!projectMemorySection.includes(token)) {
      fail(skillPath, `project memory prompt must reject unsafe product-id token: ${token}`);
    }
  }
  rejectLegacyMemoryContract(skillPath, skillDoc);
  assertAutonomousOrchestration(skillPath, skillDoc, skill);

  assertExactHeadings(principlesPath, principles, PRINCIPLE_HEADINGS);
  const principleTitles = headings(principles, 1);
  if (principleTitles.length !== 1 || !principleTitles[0].endsWith("专业约束")) {
    fail(principlesPath, "must contain exactly one level-one title ending in 专业约束");
  }
  const capabilities = blocks(principles, "专业约束");
  assertConstraintLists(principlesPath, capabilities);
  for (const field of PROHIBITED_PRINCIPLE_FIELDS) {
    if (principles.includes(`**${field}**`)) {
      fail(principlesPath, `must not use labeled capability field ${field}`);
    }
  }
  if (
    JSON.stringify(numberedIndex(principles, "能力索引")) !==
    JSON.stringify(capabilities.map((entry) => entry.title))
  ) {
    fail(principlesPath, "capability index must exactly match professional constraint titles");
  }
  assertAutonomousOrchestration(principlesPath, principles, skill);

  assertExactHeadings(memoryPath, memory, MEMORY_HEADINGS);
  const memoryTitles = headings(memory, 1);
  if (memoryTitles.length !== 1 || !memoryTitles[0].endsWith("项目记忆")) {
    fail(memoryPath, "must contain exactly one level-one title ending in 项目记忆");
  }
  const coreMemories = blocks(memory, "核心记忆");
  assertCoreMemoryLists(memoryPath, coreMemories);
  rejectLegacyMemoryContract(memoryPath, memory);
  assertAutonomousOrchestration(memoryPath, memory, skill);

  for (const key of ["interface:", "display_name:", "short_description:", "default_prompt:"]) {
    if (!agent.includes(key)) fail(agentPath, `missing ${key}`);
  }
  if (!agent.includes(`$${skill}`)) {
    fail(agentPath, `default_prompt must invoke $${skill}`);
  }
  if (!/default_prompt:.*读取、维护.*项目核心记忆/.test(agent)) {
    fail(agentPath, "default_prompt must request reading and maintaining core project memory");
  }
  rejectLegacyMemoryContract(agentPath, agent);
}

function validateTopology() {
  const actual = existsSync(SKILLS_ROOT)
    ? readdirSync(SKILLS_ROOT)
        .filter((name) => statSync(join(SKILLS_ROOT, name)).isDirectory())
        .sort()
    : [];
  const expected = [...EXPECTED_SKILLS].sort();
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    fail(
      SKILLS_ROOT,
      `skill directories must be exactly ${expected.join(", ")}; found ${actual.join(", ")}`,
    );
  }
  for (const removed of REMOVED_SKILLS) {
    const path = join(SKILLS_ROOT, removed);
    if (existsSync(path)) fail(path, "removed skill directory must not exist");
  }
  for (const skill of EXPECTED_SKILLS) validateSkill(skill);

  const factRoot = join(PROJECT_ROOT, "docs", "product-studio");
  if (existsSync(factRoot)) {
    const pending = [factRoot];
    while (pending.length > 0) {
      const current = pending.pop();
      for (const entry of readdirSync(current, { withFileTypes: true })) {
        const path = join(current, entry.name);
        if (entry.isDirectory()) pending.push(path);
        if (entry.isFile() && REMOVED_FACT_BOOKS.includes(entry.name)) {
          fail(path, "removed fact locator must not exist");
        }
        if (entry.isFile() && entry.name.endsWith(".md")) {
          const owner = basename(entry.name, ".md");
          if (!EXPECTED_SKILLS.includes(owner)) {
            fail(path, `fact book owner must be one of ${EXPECTED_SKILLS.join(", ")}`);
            continue;
          }
          const productPath = relativePath(factRoot, dirname(path)).replaceAll("\\", "/");
          if (!productPath || productPath.includes("/")) {
            fail(path, "fact book must be directly under docs/product-studio/<product-id>/");
          }
          const factBook = read(path);
          const expectedTitle = `# ${owner} 当前产品事实`;
          if (!factBook.startsWith(`${expectedTitle}\n`) && !factBook.startsWith(`${expectedTitle}\r\n`)) {
            fail(path, `fact book title must be ${expectedTitle}`);
          }
        }
      }
    }
  }
}

function validateRemovedRuntimeAssets() {
  for (const asset of REMOVED_RUNTIME_ASSETS) {
    const path = join(PROJECT_ROOT, asset);
    if (existsSync(path)) fail(path, "removed runtime or shared memory-protocol asset must not exist");
  }
}

function validateDocumentationAndManifests() {
  const readmePath = join(PROJECT_ROOT, "README.md");
  const codexPath = join(PROJECT_ROOT, ".codex-plugin", "plugin.json");
  const claudePath = join(PROJECT_ROOT, ".claude-plugin", "plugin.json");
  const marketplacePath = join(PROJECT_ROOT, ".claude-plugin", "marketplace.json");
  const agentsMarketplacePath = join(PROJECT_ROOT, ".agents", "plugins", "marketplace.json");
  const readme = read(readmePath);
  let codex;
  let claude;
  let marketplace;
  let agentsMarketplace;
  try {
    codex = JSON.parse(read(codexPath));
    claude = JSON.parse(read(claudePath));
    marketplace = JSON.parse(read(marketplacePath));
    agentsMarketplace = JSON.parse(read(agentsMarketplacePath));
  } catch (error) {
    fail(PROJECT_ROOT, `plugin manifest JSON is invalid: ${error.message}`);
    return;
  }

  if (codex.name !== claude.name || codex.version !== claude.version) {
    fail(codexPath, "Codex and Claude manifests must have matching name and version");
  }
  if (codex.skills !== "./skills/" || claude.skills !== "./skills/") {
    fail(codexPath, "both manifests must expose ./skills/");
  }
  for (const [path, manifest] of [
    [codexPath, codex],
    [claudePath, claude],
  ]) {
    if (Object.hasOwn(manifest, "hooks")) {
      fail(path, "plugin manifest must not declare removed Hook assets");
    }
  }
  if (marketplace.plugins?.[0]?.name !== codex.name) {
    fail(marketplacePath, "marketplace plugin name must match plugin manifests");
  }
  if (agentsMarketplace.plugins?.[0]?.name !== codex.name) {
    fail(agentsMarketplacePath, "Codex marketplace plugin name must match plugin manifests");
  }

  for (const skill of EXPECTED_SKILLS) {
    for (const [path, content] of [
      [readmePath, readme],
      [codexPath, JSON.stringify(codex)],
      [claudePath, JSON.stringify(claude)],
    ]) {
      if (!content.includes(skill)) fail(path, `topology must mention ${skill}`);
    }
  }
  for (const removed of REMOVED_SKILLS) {
    for (const [path, content] of [
      [readmePath, readme],
      [codexPath, JSON.stringify(codex)],
      [claudePath, JSON.stringify(claude)],
    ]) {
      if (content.includes(removed)) fail(path, `must not mention removed skill ${removed}`);
    }
  }
  for (const [path, description] of [
    [codexPath, codex.description],
    [claudePath, claude.description],
    [marketplacePath, marketplace.plugins?.[0]?.description],
  ]) {
    if (!description?.includes("十一")) {
      fail(path, "description must identify the eleven-skill topology");
    }
    if (!description?.includes("项目核心记忆")) {
      fail(path, "description must identify core project memory");
    }
  }
  if (!readme.includes("## 项目记忆")) {
    fail(readmePath, "README must describe project memory");
  }
  for (const [path, content] of [
    [readmePath, readme],
    [codexPath, JSON.stringify(codex)],
    [claudePath, JSON.stringify(claude)],
    [marketplacePath, JSON.stringify(marketplace)],
  ]) {
    for (const forbidden of ["terminal-hook", "hooks/hooks.json"]) {
      if (content.includes(forbidden)) {
        fail(path, `must not advertise removed Hook asset ${forbidden}`);
      }
    }
    rejectLegacyMemoryContract(path, content);
  }
}

validateTopology();
validateRemovedRuntimeAssets();
validateDocumentationAndManifests();

if (errors.length > 0) {
  console.error(`Project validation failed with ${errors.length} error(s):`);
  for (const error of errors) console.error(`- ${error}`);
  process.exitCode = 1;
} else {
  console.log(`Project validation passed: ${EXPECTED_SKILLS.length} skills and core project memory contracts are consistent.`);
}
