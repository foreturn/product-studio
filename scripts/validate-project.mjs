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

const SKILL_HEADINGS = [
  "目标",
  "执行协议",
  "输出契约",
  "完成条件",
  "停止条件",
  "权限与边界规则",
  "参考资料",
  "终态协议",
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
const MEMORY_HEADINGS = [
  "所有权与稳定位置",
  "事实类型索引",
  "通用入册门禁",
  "主题表达规则",
  "动作语义",
  "事实类型",
  "全册安全与删除规则",
];
const FACT_FIELDS = [
  "入册条件",
  "主题合并键",
  "当前事实写法",
  "权威依据",
  "影响边界",
  "复核入口",
  "变更规则",
  "排除项",
];
const MEMORY_ADMISSION_CONCEPTS = [
  ["current terminal state", /当前|终态/],
  ["stability", /稳定|长期/],
  ["non-obviousness", /非显然|不能.*(?:直接|低成本).*(?:推导|生成|重建)/],
  ["decision relevance", /决策|判断/],
  ["rediscovery cost", /重查|重新发现|重新推导|重建.*成本|推导.*代价/],
  ["unique owner", /唯一\s*Owner|唯一所有者/],
  ["authoritative revalidation", /权威.*(?:复核|支撑)|复核.*权威/],
  ["safe content", /秘密|密钥|凭据|令牌/],
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

function levelTwoBlocks(markdown) {
  return markdown
    .split(/^## /m)
    .slice(1)
    .map((block) => {
      const newline = block.indexOf("\n");
      return {
        title: (newline === -1 ? block : block.slice(0, newline)).trim(),
        body: newline === -1 ? "" : block.slice(newline + 1),
      };
    });
}

function assertFields(path, kind, entries, expectedFields) {
  if (entries.length === 0) {
    fail(path, `must define at least one ${kind}`);
    return;
  }
  for (const entry of entries) {
    const found = [
      ...entry.body.matchAll(/^- \*\*([^*]+)\*\*[：:]\s*/gm),
    ].map((match) => match[1].trim());
    if (JSON.stringify(found) !== JSON.stringify(expectedFields)) {
      fail(
        path,
        `${kind} "${entry.title}" fields must be exactly ${expectedFields.join(" | ")}; found ${found.join(" | ")}`,
      );
    }
  }
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
    ["indexed fact loading", /事实.*(?:类型)?索引|类型索引/],
    ["hit-only fact loading", /只读.*命中|命中.*主题/],
    ["authority revalidation", /权威.*复核|沿.*权威/],
    ["full admission-gate closure", /全部入册门禁|逐项检查.*(?:稳定|非显然)/],
  ]) {
    if (!pattern.test(executionSection)) {
      fail(skillPath, `execution protocol must cover ${label}`);
    }
  }
  for (const token of [
    "references/principles.md",
    "能力索引",
    "references/memory.md",
    "../../references/terminal-protocol.md",
  ]) {
    if (!skillDoc.includes(token)) {
      fail(skillPath, `execution contract must reference ${token}`);
    }
  }
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
  const factTypes = blocks(memory, "事实类型");
  if (factTypes.length < 5 || factTypes.length > 9) {
    fail(memoryPath, `must define 5-9 semantic terminal fact types; found ${factTypes.length}`);
  }
  assertFields(
    memoryPath,
    "fact type",
    factTypes,
    FACT_FIELDS,
  );
  if (
    JSON.stringify(numberedIndex(memory, "事实类型索引")) !==
    JSON.stringify(factTypes.map((entry) => entry.title))
  ) {
    fail(memoryPath, "fact-type index must exactly match fact-type titles");
  }
  const actionSection = section(memory, "动作语义");
  for (const action of ["ADD", "UPDATE", "DELETE", "NO_CHANGE"]) {
    if (!actionSection.includes(action)) {
      fail(memoryPath, `action semantics must define ${action}`);
    }
  }
  const admissionSection = section(memory, "通用入册门禁");
  for (const [label, pattern] of MEMORY_ADMISSION_CONCEPTS) {
    if (!pattern.test(admissionSection)) {
      fail(memoryPath, `common admission gate must cover ${label}`);
    }
  }
  const safetySection = section(memory, "全册安全与删除规则");
  const safetyConcepts = [
    ["secrets or credentials", /秘密|密钥|凭据|密码|令牌|签名材料/],
    ["personal or user data", /用户数据|个人数据|客户数据|生产数据|生产样本/],
    ["deletion", /删除|DELETE/],
  ];
  for (const [label, pattern] of safetyConcepts) {
    if (!pattern.test(safetySection)) {
      fail(memoryPath, `whole-book safety rules must cover ${label}`);
    }
  }
  assertAutonomousOrchestration(memoryPath, memory, skill);
  const locator = `docs/product-studio/<product-id>/${skill}.md`;
  if (!memory.includes(locator)) {
    fail(memoryPath, `must declare owner locator ${locator}`);
  }

  for (const key of ["interface:", "display_name:", "short_description:", "default_prompt:"]) {
    if (!agent.includes(key)) fail(agentPath, `missing ${key}`);
  }
  if (!agent.includes(`$${skill}`)) {
    fail(agentPath, `default_prompt must invoke $${skill}`);
  }
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

function validateHookAssets() {
  const hooksPath = join(PROJECT_ROOT, "hooks", "hooks.json");
  const scriptPath = join(PROJECT_ROOT, "scripts", "terminal-hook.mjs");
  const protocolPath = join(PROJECT_ROOT, "references", "terminal-protocol.md");
  const fixturePath = join(PROJECT_ROOT, "tests", "fixtures", "terminal-envelope.json");
  const hooksText = read(hooksPath);
  read(scriptPath);
  const protocolText = read(protocolPath);
  const fixtureText = read(fixturePath);
  if (!hooksText) return;
  try {
    const hooks = JSON.parse(hooksText).hooks ?? {};
    for (const event of ["UserPromptSubmit", "PreToolUse", "PostToolUse", "Stop"]) {
      if (!Array.isArray(hooks[event]) || hooks[event].length === 0) {
        fail(hooksPath, `must configure ${event}`);
        continue;
      }
      const handlers = hooks[event].flatMap((entry) =>
        Array.isArray(entry?.hooks) ? entry.hooks : [],
      );
      if (handlers.length === 0) {
        fail(hooksPath, `${event} must contain at least one hook handler`);
        continue;
      }
      for (const [index, handler] of handlers.entries()) {
        if (handler?.type !== "command") {
          fail(hooksPath, `${event} handler ${index} must use type=command`);
        }
        if (
          typeof handler?.command !== "string" ||
          !handler.command.includes("${CLAUDE_PLUGIN_ROOT}") ||
          !handler.command.includes("terminal-hook.mjs")
        ) {
          fail(
            hooksPath,
            `${event} handler ${index} must invoke terminal-hook.mjs through \${CLAUDE_PLUGIN_ROOT}`,
          );
        }
        if (!Number.isFinite(handler?.timeout) || handler.timeout < 180) {
          fail(hooksPath, `${event} handler ${index} timeout must be at least 180 seconds`);
        }
      }
      if (
        ["PreToolUse", "PostToolUse"].includes(event) &&
        !hooks[event].some(
          (entry) =>
            typeof entry?.matcher === "string" &&
            entry.matcher.includes("Bash") &&
            entry.matcher.includes("exec_command") &&
            entry.matcher.includes("shell_command"),
        )
      ) {
        fail(hooksPath, `${event} must observe Bash, exec_command, and shell_command`);
      }
    }
  } catch (error) {
    fail(hooksPath, `invalid JSON: ${error.message}`);
  }

  for (const token of [
    "--data-dir",
    "--session",
    "sessionId",
    "toolUseId",
    "inputDigest",
    "commandHash",
    "expectedExitCodes",
    "productId",
    "factBookPath",
    "envelopePath",
    "guardrail",
  ]) {
    if (!protocolText.includes(token)) {
      fail(protocolPath, `terminal protocol must describe ${token}`);
    }
  }
  if (!fixtureText) return;
  try {
    const fixture = JSON.parse(fixtureText);
    if (fixture.schemaVersion !== 2 || typeof fixture.sessionId !== "string") {
      fail(fixturePath, "terminal fixture must use schemaVersion 2 and include sessionId");
    }
    for (const [index, evidence] of (fixture.validationEvidence ?? []).entries()) {
      if (!Array.isArray(evidence.expectedExitCodes) || evidence.expectedExitCodes.length === 0) {
        fail(fixturePath, `validationEvidence[${index}] must include expectedExitCodes`);
      }
      for (const field of ["toolUseId", "inputDigest", "commandHash"]) {
        if (typeof evidence[field] !== "string" || evidence[field].length === 0) {
          fail(fixturePath, `validationEvidence[${index}] must include ${field}`);
        }
      }
      if ("command" in evidence || "exitCode" in evidence) {
        fail(fixturePath, `validationEvidence[${index}] must not self-report command or exitCode`);
      }
    }
    for (const [index, owner] of (fixture.checkedOwners ?? []).entries()) {
      if (
        typeof owner.productId !== "string" ||
        owner.factBookPath !==
          `docs/product-studio/${owner.productId}/${owner.owner}.md`
      ) {
        fail(
          fixturePath,
          `checkedOwners[${index}] must bind productId, owner, and factBookPath`,
        );
      }
    }
  } catch (error) {
    fail(fixturePath, `invalid terminal fixture JSON: ${error.message}`);
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
  }
}

validateTopology();
validateHookAssets();
validateDocumentationAndManifests();

if (errors.length > 0) {
  console.error(`Project validation failed with ${errors.length} error(s):`);
  for (const error of errors) console.error(`- ${error}`);
  process.exitCode = 1;
} else {
  console.log(`Project validation passed: ${EXPECTED_SKILLS.length} skills and terminal hook assets are consistent.`);
}
