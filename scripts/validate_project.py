#!/usr/bin/env python3
"""Validate the shared Product Studio plugin without external dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
CORE_SKILL_ORDER = (
    "delivery",
    "discovery",
    "architecture",
    "frontend",
    "backend",
    "verification",
    "release",
)
CORE_SKILLS = set(CORE_SKILL_ORDER)
SKILL_ROLE_IDENTITIES = {
    "delivery": "产品交付负责人",
    "discovery": "产品经理",
    "architecture": "系统架构师",
    "frontend": "前端与体验负责人",
    "backend": "后端负责人",
    "verification": "独立验收负责人",
    "release": "发布与运行负责人",
}
COMMON_SKILL_SECTIONS = (
    "## 角色定位",
    "## 输入契约",
    "## 调用方式",
    "## 专业能力来源",
    "## 项目记忆",
    "## 执行流程",
    "## 输出契约",
    "## 交接门禁",
    "## 边界",
)
SKILL_REFERENCE_ONLY_SECTIONS = (
    "## 职责",
    "## 核心能力",
    "## 专业决策顺序",
)
REFERENCE_CAPABILITY_TERMS = {
    "delivery": ("意图归类", "切片与排程", "依赖协调", "风险管理", "决策与变更控制", "质量门禁", "交付沟通"),
    "discovery": ("问题定义", "用户与任务建模", "证据化联想", "旅程与状态设计", "范围与优先级", "成功衡量", "澄清沟通"),
    "architecture": ("系统建模", "边界与契约设计", "质量属性权衡", "一致性与故障设计", "安全与权限边界", "可观测与可运行性", "演进与迁移"),
    "frontend": ("易用性与任务效率", "交互设计", "信息架构", "布局与响应式", "视觉协调", "可访问性", "组件与状态工程", "前端性能与视觉验收"),
    "backend": ("领域建模", "API 与错误契约", "数据建模与迁移", "权限与安全", "一致性与并发", "集成与可靠性", "性能与可观测性", "测试策略"),
    "verification": ("需求追溯", "风险建模", "分层测试设计", "用户体验验收", "服务端与数据验收", "非功能验证", "回归分析", "证据审计"),
    "release": ("发布策略", "制品与配置治理", "迁移编排", "可观测与健康判断", "风险控制与回滚", "事故处置", "反馈闭环"),
}
SKILL_BOUNDARY_TERMS = {
    "delivery": ("本角色主责是编排角色",),
    "discovery": ("具体实现方案归架构及实现角色",),
    "architecture": ("具体前端和后端实现归相应实现角色",),
    "frontend": ("产品范围、业务规则、权限模型与接口兼容策略由对应产品或后端契约确定",),
    "backend": ("用户体验与用户可见文案归产品和前端角色",),
    "verification": ("验收标准独立于实现结果",),
    "release": ("外部状态变更以绑定当前制品、环境、范围与动作的明确授权为前置条件",),
}
SKILL_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9]*$")
SKILL_MEMORY_FILES = {name: f"{name}.md" for name in CORE_SKILL_ORDER}
SKILL_INVOCATION_TERM_GROUPS = (
    ("按需直调",),
    ("并行协作",),
    ("并发收口",),
    ("上游门禁",),
    ("输入快照一致",),
    ("依赖独立",),
    ("写入不冲突",),
    ("固定责任角色", "只由本角色"),
    ("串行",),
)
PROJECT_MEMORY_TERM_GROUPS = (
    ("当前项目根",),
    ("docs/product-studio/",),
    ("跨会话",),
    ("当前项目事实基线",),
    ("用户显式提供",),
    ("外部参考",),
    ("核验适用性",),
    ("不会自动成为当前项目事实",),
    ("只读",),
    ("不授权写入", "不自动授权写入", "不授权创建或更新"),
    ("氛围编程完成前",),
    ("动态更新", "动态收口"),
    ("同名",),
    ("精确来源", "精确依据"),
    ("失效条件",),
    ("时间戳记录核验时点",),
    ("不单独构成新证据",),
)
PROJECT_MEMORY_REFERENCE_SECTION_TERMS = {
    "## 定义与位置": (
        "<当前项目根>/docs/product-studio/",
        "产品名称只作为文档元数据保存",
        "不是项目事实的持久化位置",
    ),
    "## 作用域与隔离": (
        "当前项目根是事实归属与持久化隔离键",
        "不同仓库中的同名 `docs/product-studio/` 分别描述各自项目",
        "不再为其增加路径层级",
        "带来源与适用范围的显式引用完成交接",
    ),
    "## 信息来源与适用性": (
        "当前项目事实基线",
        "用户显式提供的链接、页面、截图、设计稿、文档或其他项目材料",
        "外部参考",
        "不会自动成为当前项目事实",
        "精确来源、提取特征、用途、时间与置信度",
        "当前用户确认、当前仓库实现、权威 Schema、运行证据或本项目验证",
        "信息读取与持久化写入是两条独立边界",
        "参考材料可以进入分析上下文",
    ),
    "## 命名与寻址": (
        "七个 Skill 使用单个小写英文单词",
        "templates/<skill>.md",
        "docs/product-studio/<skill>.md",
        "活跃寻址使用这一条同名路径",
        "旧名称与旧文件只作为迁移历史保留",
    ),
    "## 读取与更新": (
        "当前用户指令与当前仓库事实优先于旧记忆",
        "只读任务不授权创建或更新项目记忆",
        "凭据、令牌、私钥、会话密钥及其他秘密不属于记忆正文",
    ),
    "## AI 记忆结构": (
        "verified_revision",
        "稳定 ID 与精确来源",
        "动作队列",
        "交接与失效条件",
        "时间戳本身不是更新证据",
    ),
    "## 动态收口": (
        "每次获准的氛围编程完成前",
        "每个参与或受影响角色必须复核并动态更新",
        "已复核、无变化",
        "氛围编程仍处于未收口状态",
    ),
    "## 角色与记忆文件": (),
}
TEMPLATE_ROLE_OWNERS = {f"{name}.md": name for name in CORE_SKILL_ORDER}
CAPABILITY_REFERENCES = {
    "delivery": ("references/delivery-capabilities.md", ()),
    "discovery": ("references/product-design-principles.md", ()),
    "architecture": ("references/architecture-principles.md", ()),
    "frontend": ("references/frontend-design-principles.md", ()),
    "backend": ("references/backend-design-principles.md", ()),
    "verification": ("references/verification-principles.md", ()),
    "release": ("references/release-principles.md", ()),
}
CAPABILITY_REFERENCE_SECTIONS = (
    "## 角色职责",
    "## 核心能力",
    "## 专业决策顺序",
    "## 交付证据",
    "## 常见误判",
)
COMMON_MEMORY_SECTIONS = (
    "## 恢复摘要",
    "## 依据账本",
    "## 动作队列",
    "## 当前验证",
    "## 交接与失效",
)
TEMPLATE_ROLE_SECTIONS = {
    "delivery": (
        "## 原始意图与范围",
        "## 角色链与依赖",
        "## 交付切片",
        "## 风险与阻塞",
        "## 角色记忆收口",
    ),
    "discovery": (
        "## 原始意图",
        "## 用户问题与目标结果",
        "## 核心旅程与状态",
        "## 范围与非目标",
        "## 假设与开放问题",
        "## 验收标准",
        "## 决策记录",
    ),
    "architecture": (
        "## 架构上下文",
        "## 不变量与质量属性",
        "## 边界与所有权",
        "## 决策索引",
        "## 候选方案与权衡",
        "## 失败模式",
        "## 迁移与回滚",
    ),
    "frontend": (
        "## 输入来源与适用性",
        "## 用户任务与流程",
        "## 界面状态矩阵",
        "## 交互与可访问性",
        "## 实现映射",
        "## 真实渲染证据",
    ),
    "backend": (
        "## 输入来源与适用性",
        "## 领域与数据不变量",
        "## 接口与错误契约",
        "## 权限与安全",
        "## 一致性与失败恢复",
        "## 兼容与迁移",
        "## 调用方交接",
    ),
    "verification": (
        "## 验收对象",
        "## 要求与证据矩阵",
        "## 核心旅程与状态证据",
        "## 失败与恢复证据",
        "## 回归与非功能",
        "## 失败分类",
        "## 最终结论",
    ),
    "release": (
        "## 发布对象与授权",
        "## 发布前门禁",
        "## 部署与迁移步骤",
        "## 健康与业务信号",
        "## 停止与回滚",
        "## 执行记录",
        "## 上线后验证",
        "## 反馈回流",
        "## 最终结论",
    ),
}
TEMPLATE_SECTIONS = {
    f"{name}.md": COMMON_MEMORY_SECTIONS + TEMPLATE_ROLE_SECTIONS[name]
    for name in CORE_SKILL_ORDER
}
MEMORY_FRONTMATTER_FIELDS = (
    "schema",
    "memory",
    "scope",
    "project_root",
    "status",
    "updated_at",
    "verified_at",
    "verified_revision",
    "confidence",
    "supersedes",
)
TEMPLATE_AI_TERMS = (
    "AI 写入规则",
    "AI 恢复顺序",
    "verified_revision",
    "confidence",
    "supersedes",
    "精确来源",
    "失效条件",
    "外部参考",
    "适用性",
    "外部参考不会自动成为当前项目事实",
)
FINAL_MEMORY_STATUS = {
    "delivery": "done",
    "discovery": "done",
    "architecture": "done",
    "frontend": "done",
    "backend": "done",
    "verification": "done",
    "release": "not_applicable",
}
LEGACY_TERMS = tuple(
    "-".join(parts)
    for parts in (
        ("product", "delivery"),
        ("product", "discovery"),
        ("system", "design"),
        ("frontend", "experience"),
        ("backend", "contract"),
        ("delivery", "verification"),
        ("release", "operations"),
    )
) + tuple(
    "-".join(parts) + ".md"
    for parts in (
        ("delivery", "state"),
        ("product", "brief"),
        ("architecture", "decision"),
        ("architecture", "decisions"),
        ("feature", "spec"),
        ("api", "contract"),
        ("acceptance", "report"),
        ("release", "plan"),
    )
)
OVERRESTRICTIVE_SOURCE_TERMS = (
    "只" + "读取当前项目根",
    "只能" + "读取当前项目",
    "仅限" + "读取当前项目",
    "不得" + "从其他仓库、项目或产品继承",
    "严禁" + "跨仓库、项目或产品继承",
    "严禁" + "自动跨仓库、项目或产品继承",
    "不搜索" + "或复制父目录",
    "事实必须" + "指向用户指令或仓库证据",
    "旧报告和其他项目结果" + "不得充作当前证据",
    "不得把其他仓库或产品的交付状态" + "并入当前项目",
)


def load_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Invalid JSON {path.relative_to(ROOT)}: {exc}")
        return None


def base_version(value: str) -> str:
    return value.split("+", 1)[0]


def require_terms(
    path: Path,
    content: str,
    terms: tuple[str, ...] | set[str],
    errors: list[str],
) -> None:
    for term in terms:
        if term not in content:
            errors.append(f"Missing required contract '{term}': {path.relative_to(ROOT)}")


def markdown_section(content: str, heading: str) -> str | None:
    """Return one level-two Markdown section without matching other sections."""
    lines = content.splitlines()
    start: int | None = None
    in_fence = False
    for index, line in enumerate(lines):
        if re.match(r"^\s*(?:```|~~~)", line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if start is None:
            if line.strip() == heading:
                start = index + 1
            continue
        if re.match(r"^##(?!#)\s+", line):
            return "\n".join(lines[start:index]).strip()
    if start is None:
        return None
    return "\n".join(lines[start:]).strip()


def require_section(
    path: Path,
    content: str,
    heading: str,
    errors: list[str],
) -> str | None:
    section = markdown_section(content, heading)
    if section is None:
        errors.append(f"Missing required section '{heading}': {path.relative_to(ROOT)}")
        return None
    if not section:
        errors.append(f"Empty required section '{heading}': {path.relative_to(ROOT)}")
        return None
    return section


def require_term_groups(
    path: Path,
    content: str,
    term_groups: tuple[tuple[str, ...], ...],
    errors: list[str],
    context: str,
) -> None:
    for alternatives in term_groups:
        if not any(term in content for term in alternatives):
            expected = " / ".join(alternatives)
            errors.append(
                f"Missing required {context} contract '{expected}': "
                f"{path.relative_to(ROOT)}"
            )


def parse_yaml_scalar(
    path: Path,
    content: str,
    key: str,
    errors: list[str],
) -> str | None:
    matches = re.findall(
        rf"^\s*{re.escape(key)}\s*:\s*(.*?)\s*$",
        content,
        re.MULTILINE,
    )
    if len(matches) != 1:
        errors.append(
            f"Expected exactly one YAML field '{key}': {path.relative_to(ROOT)}"
        )
        return None

    value = matches[0].strip()
    if len(value) >= 2 and value[0] in {'"', "'"} and value[-1] == value[0]:
        value = value[1:-1]
    if not value:
        errors.append(f"Empty YAML field '{key}': {path.relative_to(ROOT)}")
        return None
    return value


def parse_frontmatter(path: Path, errors: list[str]) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        errors.append(f"Missing frontmatter start: {path.relative_to(ROOT)}")
        return {}
    try:
        end = lines.index("---", 1)
    except ValueError:
        errors.append(f"Missing frontmatter end: {path.relative_to(ROOT)}")
        return {}

    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" in line:
            key, value = line.split(":", 1)
            value = value.strip()
            if len(value) >= 2 and value[0] in {'"', "'"} and value[-1] == value[0]:
                value = value[1:-1]
            fields[key.strip()] = value
    return fields


def validate_memory_frontmatter(
    path: Path,
    expected_memory: str,
    errors: list[str],
    *,
    require_current_values: bool,
) -> dict[str, str]:
    fields = parse_frontmatter(path, errors)
    for field in MEMORY_FRONTMATTER_FIELDS:
        if field not in fields:
            errors.append(
                f"Missing memory frontmatter field '{field}': {path.relative_to(ROOT)}"
            )
    if fields.get("schema") != "1":
        errors.append(f"Memory schema must be 1: {path.relative_to(ROOT)}")
    if fields.get("memory") != expected_memory:
        errors.append(
            f"Memory name must match skill '{expected_memory}': {path.relative_to(ROOT)}"
        )
    if fields.get("scope") != "current-project":
        errors.append(f"Memory scope must be current-project: {path.relative_to(ROOT)}")

    if require_current_values:
        expected_status = FINAL_MEMORY_STATUS[expected_memory]
        if fields.get("status") != expected_status:
            errors.append(
                f"Project memory status must be '{expected_status}': "
                f"{path.relative_to(ROOT)}"
            )
        for field in ("project_root", "updated_at", "verified_at", "verified_revision"):
            if not fields.get(field):
                errors.append(
                    f"Empty current memory field '{field}': {path.relative_to(ROOT)}"
                )
        if fields.get("confidence") not in {"high", "medium", "low"}:
            errors.append(
                f"Invalid current memory confidence: {path.relative_to(ROOT)}"
            )
    return fields


def validate_instantiated_memory(path: Path, content: str, errors: list[str]) -> None:
    for line_number, line in enumerate(content.splitlines(), 1):
        if re.fullmatch(r"\s*(?:-|\d+\.)\s*", line):
            errors.append(
                f"Empty memory placeholder at {path.relative_to(ROOT)}:{line_number}"
            )
        if line.lstrip().startswith("|"):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if cells and all(not cell for cell in cells):
                errors.append(
                    f"Empty memory table row at {path.relative_to(ROOT)}:{line_number}"
                )


def main() -> int:
    errors: list[str] = []
    for name in CORE_SKILLS:
        if not SKILL_NAME_PATTERN.fullmatch(name):
            errors.append(f"Core skill name is not one lowercase word: {name}")
    for contract_name, contract in (
        ("role identities", SKILL_ROLE_IDENTITIES),
        ("boundary terms", SKILL_BOUNDARY_TERMS),
        ("memory files", SKILL_MEMORY_FILES),
    ):
        missing = CORE_SKILLS - set(contract)
        extra = set(contract) - CORE_SKILLS
        if missing or extra:
            errors.append(
                f"Validator {contract_name} mapping does not match core skills: "
                f"missing={sorted(missing)}, extra={sorted(extra)}"
            )

    if set(TEMPLATE_ROLE_OWNERS) != set(TEMPLATE_SECTIONS):
        errors.append("Validator template owner mapping does not match templates")
    if set(TEMPLATE_ROLE_OWNERS.values()) != CORE_SKILLS:
        errors.append("Validator template owners do not match core skills")

    codex_manifest = ROOT / ".codex-plugin" / "plugin.json"
    claude_manifest = ROOT / ".claude-plugin" / "plugin.json"
    claude_marketplace_manifest = ROOT / ".claude-plugin" / "marketplace.json"
    marketplace_manifest = ROOT / ".agents" / "plugins" / "marketplace.json"
    product_docs = ROOT / "docs" / "product-studio"
    project_memory_reference = ROOT / "references" / "project-memory.md"
    skill_dirs = {path.name for path in SKILLS.iterdir() if path.is_dir()}
    template_files = {path.name for path in (ROOT / "templates").glob("*.md")}
    project_memory_files = {path.name for path in product_docs.glob("*.md")}
    expected_memory_files = set(SKILL_MEMORY_FILES.values())
    if skill_dirs != CORE_SKILLS:
        errors.append(
            f"Skill directories do not match one-word core skills: "
            f"missing={sorted(CORE_SKILLS - skill_dirs)}, "
            f"extra={sorted(skill_dirs - CORE_SKILLS)}"
        )
    if template_files != expected_memory_files:
        errors.append(
            f"Template filenames must exactly match skills: "
            f"missing={sorted(expected_memory_files - template_files)}, "
            f"extra={sorted(template_files - expected_memory_files)}"
        )
    if project_memory_files != expected_memory_files:
        errors.append(
            f"Project memory filenames must exactly match skills: "
            f"missing={sorted(expected_memory_files - project_memory_files)}, "
            f"extra={sorted(project_memory_files - expected_memory_files)}"
        )
    required = [
        codex_manifest,
        claude_manifest,
        claude_marketplace_manifest,
        marketplace_manifest,
        project_memory_reference,
    ]
    required.extend(ROOT / "templates" / filename for filename in sorted(expected_memory_files))
    required.extend(product_docs / filename for filename in sorted(expected_memory_files))
    for path in required:
        if not path.is_file():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")

    codex = load_json(codex_manifest, errors)
    claude = load_json(claude_manifest, errors)
    claude_marketplace = load_json(claude_marketplace_manifest, errors)
    marketplace = load_json(marketplace_manifest, errors)
    if isinstance(codex, dict) and isinstance(claude, dict):
        for field in ("name", "description", "keywords", "skills"):
            if codex.get(field) != claude.get(field):
                errors.append(f"Manifest field differs: {field}")
        if base_version(str(codex.get("version", ""))) != base_version(
            str(claude.get("version", ""))
        ):
            errors.append("Manifest base versions differ")

        author = codex.get("author")
        interface = codex.get("interface")
        if not isinstance(author, dict) or not isinstance(interface, dict):
            errors.append("Codex manifest publisher metadata is incomplete")
        elif author.get("name") != interface.get("developerName"):
            errors.append("Codex author name and developer name differ")

    if isinstance(claude, dict) and isinstance(claude_marketplace, dict):
        if claude_marketplace.get("name") != "foreturn":
            errors.append("Claude marketplace name must be foreturn")
        if not claude_marketplace.get("description"):
            errors.append("Claude marketplace description is missing")

        owner = claude_marketplace.get("owner")
        author = claude.get("author")
        if not isinstance(owner, dict) or not isinstance(author, dict):
            errors.append("Claude marketplace publisher metadata is incomplete")
        elif owner.get("name") != author.get("name"):
            errors.append("Claude marketplace owner and plugin author differ")

        plugins = claude_marketplace.get("plugins")
        plugin = plugins[0] if isinstance(plugins, list) and len(plugins) == 1 else None
        if not isinstance(plugin, dict):
            errors.append("Claude marketplace must contain exactly one plugin")
        else:
            if plugin.get("name") != claude.get("name"):
                errors.append("Claude marketplace plugin name differs from manifest")
            if plugin.get("source") != "./":
                errors.append("Claude marketplace plugin source must be the repository root")
            if plugin.get("description") != claude.get("description"):
                errors.append("Claude marketplace description differs from manifest")

    if isinstance(codex, dict) and isinstance(marketplace, dict):
        if marketplace.get("name") != "foreturn":
            errors.append("Marketplace name must be foreturn")

        plugins = marketplace.get("plugins")
        plugin = plugins[0] if isinstance(plugins, list) and len(plugins) == 1 else None
        if not isinstance(plugin, dict):
            errors.append("Marketplace must contain exactly one plugin")
        else:
            if plugin.get("name") != codex.get("name"):
                errors.append("Marketplace plugin name differs from Codex manifest")
            source = plugin.get("source")
            if not isinstance(source, dict) or source.get("source") != "url":
                errors.append("Marketplace plugin must use a URL source")
            elif source.get("url") != "https://github.com/foreturn/product-studio.git":
                errors.append("Marketplace plugin URL is incorrect")
            policy = plugin.get("policy")
            if not isinstance(policy, dict) or policy.get("installation") != "AVAILABLE":
                errors.append("Marketplace installation policy must be AVAILABLE")
            if not isinstance(policy, dict) or policy.get("authentication") != "ON_INSTALL":
                errors.append("Marketplace authentication policy must be ON_INSTALL")
            if plugin.get("category") != "Productivity":
                errors.append("Marketplace category must be Productivity")

    codex_source = codex_manifest.read_text(encoding="utf-8")
    if re.search(r"\\u[0-9a-fA-F]{4}", codex_source):
        errors.append("Codex manifest contains escaped Chinese Unicode text")

    skill_names: set[str] = set()
    for skill_dir in sorted(path for path in SKILLS.iterdir() if path.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"Missing SKILL.md: {skill_dir.relative_to(ROOT)}")
            continue
        fields = parse_frontmatter(skill_file, errors)
        name = fields.get("name", "")
        description = fields.get("description", "")
        if name != skill_dir.name:
            errors.append(f"Skill name mismatch: {skill_dir.name} != {name}")
        if not SKILL_NAME_PATTERN.fullmatch(name):
            errors.append(f"Skill name is not one lowercase word: {skill_dir.name}")
        if set(fields) != {"name", "description"}:
            errors.append(
                f"Skill frontmatter must contain only name and description: "
                f"{skill_file.relative_to(ROOT)}"
            )
        if not description:
            errors.append(f"Missing skill description: {skill_dir.name}")
        skill_names.add(name)

        content = skill_file.read_text(encoding="utf-8")
        sections = {
            heading: require_section(skill_file, content, heading, errors)
            for heading in COMMON_SKILL_SECTIONS
        }

        role_identity = SKILL_ROLE_IDENTITIES.get(name)
        role_section = sections.get("## 角色定位")
        if role_identity and role_section:
            require_terms(skill_file, role_section, (role_identity,), errors)

        for heading in SKILL_REFERENCE_ONLY_SECTIONS:
            if markdown_section(content, heading) is not None:
                errors.append(
                    f"Detailed role capability section must live in references "
                    f"('{heading}'): {skill_file.relative_to(ROOT)}"
                )

        capability_reference = CAPABILITY_REFERENCES.get(name)
        capability_source_section = sections.get("## 专业能力来源")
        if capability_reference and capability_source_section:
            ref_name, _ = capability_reference
            require_terms(
                skill_file,
                capability_source_section,
                (
                    ref_name,
                    "职责、核心能力、专业决策顺序",
                    "交付证据",
                    "常见误判",
                    "唯一详细定义",
                ),
                errors,
            )

        invocation_section = sections.get("## 调用方式")
        if invocation_section:
            require_term_groups(
                skill_file,
                invocation_section,
                SKILL_INVOCATION_TERM_GROUPS,
                errors,
                "invocation section",
            )
            require_terms(skill_file, invocation_section, (f"${name}",), errors)

        boundary_terms = SKILL_BOUNDARY_TERMS.get(name)
        boundary_section = sections.get("## 边界")
        if boundary_terms and boundary_section:
            require_terms(skill_file, boundary_section, boundary_terms, errors)

        memory_file = SKILL_MEMORY_FILES.get(name)
        memory_section = sections.get("## 项目记忆")
        if memory_section:
            require_term_groups(
                skill_file,
                memory_section,
                PROJECT_MEMORY_TERM_GROUPS,
                errors,
                "project-memory section",
            )
            if memory_file:
                require_terms(
                    skill_file,
                    memory_section,
                    (memory_file, f"../../templates/{memory_file}"),
                    errors,
                )

        if capability_reference:
            ref_name, ref_terms = capability_reference
            ref_path = skill_dir / ref_name
            if not ref_path.is_file():
                errors.append(f"Missing capability reference: {ref_path.relative_to(ROOT)}")
            else:
                ref_content = ref_path.read_text(encoding="utf-8")
                for heading in CAPABILITY_REFERENCE_SECTIONS:
                    require_section(ref_path, ref_content, heading, errors)
                require_terms(
                    ref_path,
                    ref_content,
                    (*ref_terms, *REFERENCE_CAPABILITY_TERMS[name]),
                    errors,
                )

        agent_metadata = skill_dir / "agents" / "openai.yaml"
        if not agent_metadata.is_file():
            errors.append(f"Missing Codex skill metadata: {agent_metadata.relative_to(ROOT)}")
        else:
            metadata = agent_metadata.read_text(encoding="utf-8")
            default_prompt = parse_yaml_scalar(
                agent_metadata,
                metadata,
                "default_prompt",
                errors,
            )
            if default_prompt is not None:
                if f"${name}" not in default_prompt:
                    errors.append(
                        f"Codex default prompt does not invoke ${name}: "
                        f"{agent_metadata.relative_to(ROOT)}"
                    )
                if role_identity and role_identity not in default_prompt:
                    errors.append(
                        f"Codex default prompt does not adopt role '{role_identity}': "
                        f"{agent_metadata.relative_to(ROOT)}"
                    )

        for ref in re.findall(r"`((?:\.\./)+templates/[A-Za-z0-9_.-]+)`", content):
            if not (skill_dir / ref).resolve().is_file():
                errors.append(f"Broken template reference in {skill_dir.name}: {ref}")
        for ref in re.findall(r"`(references/[A-Za-z0-9_.-]+)`", content):
            if not (skill_dir / ref).is_file():
                errors.append(f"Broken capability reference in {skill_dir.name}: {ref}")

    for missing_skill in sorted(CORE_SKILLS - skill_names):
        errors.append(f"Missing core lifecycle skill: {missing_skill}")
    if skill_names != CORE_SKILLS:
        errors.append(
            f"Skill frontmatter names do not match core skills: "
            f"missing={sorted(CORE_SKILLS - skill_names)}, "
            f"extra={sorted(skill_names - CORE_SKILLS)}"
        )

    if project_memory_reference.is_file():
        project_memory_content = project_memory_reference.read_text(encoding="utf-8")
        reference_sections = {
            heading: require_section(
                project_memory_reference,
                project_memory_content,
                heading,
                errors,
            )
            for heading in PROJECT_MEMORY_REFERENCE_SECTION_TERMS
        }
        for heading, terms in PROJECT_MEMORY_REFERENCE_SECTION_TERMS.items():
            section = reference_sections.get(heading)
            if section:
                require_terms(project_memory_reference, section, terms, errors)

        role_mapping_section = reference_sections.get("## 角色与记忆文件")
        if role_mapping_section:
            for skill_name, memory_file in SKILL_MEMORY_FILES.items():
                require_terms(
                    project_memory_reference,
                    role_mapping_section,
                    (skill_name, memory_file),
                    errors,
                )

    delivery_skill = (SKILLS / "delivery" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    require_terms(
        SKILLS / "delivery" / "SKILL.md",
        delivery_skill,
        CORE_SKILLS - {"delivery"},
        errors,
    )

    discovery_skill = (SKILLS / "discovery" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    require_terms(
        SKILLS / "discovery" / "SKILL.md",
        discovery_skill,
        (
            "原始意图",
            "仓库事实",
            "必须确认",
            "记录假设后继续",
            "自行查明",
            "不虚构",
        ),
        errors,
    )

    verification_skill = (SKILLS / "verification" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    require_terms(
        SKILLS / "verification" / "SKILL.md",
        verification_skill,
        ("失败", "阻塞", "既有问题", "剩余风险"),
        errors,
    )

    for template_name, sections in TEMPLATE_SECTIONS.items():
        template_path = ROOT / "templates" / template_name
        if template_path.is_file():
            template_content = template_path.read_text(encoding="utf-8")
            owner = TEMPLATE_ROLE_OWNERS.get(template_name)
            if owner:
                validate_memory_frontmatter(
                    template_path,
                    owner,
                    errors,
                    require_current_values=False,
                )
                require_terms(
                    template_path,
                    template_content,
                    (
                        f"# {owner}",
                        f"固定责任角色：`{owner}`",
                        f"docs/product-studio/{owner}.md",
                        *TEMPLATE_AI_TERMS,
                    ),
                    errors,
                )
            for heading in sections:
                require_section(template_path, template_content, heading, errors)

    for skill_name, memory_file in SKILL_MEMORY_FILES.items():
        memory_path = product_docs / memory_file
        if not memory_path.is_file():
            continue
        memory_content = memory_path.read_text(encoding="utf-8")
        validate_memory_frontmatter(
            memory_path,
            skill_name,
            errors,
            require_current_values=True,
        )
        require_terms(
            memory_path,
            memory_content,
            (
                f"# {skill_name}",
                f"固定责任角色：`{skill_name}`",
                f"docs/product-studio/{skill_name}.md",
                "verified_revision",
                "失效条件",
            ),
            errors,
        )
        for heading in COMMON_MEMORY_SECTIONS:
            require_section(memory_path, memory_content, heading, errors)
        validate_instantiated_memory(memory_path, memory_content, errors)
        if re.search(r"\|\s*pending\s*\|", memory_content):
            errors.append(f"Pending memory table status remains: {memory_path.relative_to(ROOT)}")

    delivery_path = product_docs / "delivery.md"
    if delivery_path.is_file():
        delivery_content = delivery_path.read_text(encoding="utf-8")
        require_section(
            delivery_path,
            delivery_content,
            "## 角色记忆收口",
            errors,
        )
        for skill_name, memory_file in SKILL_MEMORY_FILES.items():
            require_terms(
                delivery_path,
                delivery_content,
                (skill_name, memory_file),
                errors,
            )

    discovery_path = product_docs / "discovery.md"
    if discovery_path.is_file():
        discovery_content = discovery_path.read_text(encoding="utf-8")
        for heading in ("## 原始意图", "## 验收标准", "## 决策记录"):
            require_section(discovery_path, discovery_content, heading, errors)
        require_terms(
            discovery_path,
            discovery_content,
            ("AC-001", "AC-006"),
            errors,
        )

    verification_path = product_docs / "verification.md"
    verification_passed = False
    if verification_path.is_file():
        verification_content = verification_path.read_text(encoding="utf-8")
        for heading in ("## 验收对象", "## 要求与证据矩阵", "## 最终结论"):
            require_section(verification_path, verification_content, heading, errors)
        verification_passed = "- 结论：通过" in verification_content
        if not verification_passed:
            errors.append("Product Studio verification memory is not marked as passed")

    release_path = product_docs / "release.md"
    if verification_passed and release_path.is_file():
        release_content = release_path.read_text(encoding="utf-8")
        require_terms(
            release_path,
            release_content,
            (
                "对应验收修订：`verification.md` 已",
                "下一责任角色：无",
            ),
            errors,
        )
        for stale_term in (
            "待 `verification.md` 本轮通过",
            "下一责任角色：`verification` 完成源码验收",
        ):
            if stale_term in release_content:
                errors.append(
                    f"Release memory contradicts passed verification with "
                    f"'{stale_term}': {release_path.relative_to(ROOT)}"
                )

    active_legacy_paths = (
        ROOT / "README.md",
        ROOT / "references",
        ROOT / "scripts",
        ROOT / "skills",
        ROOT / "templates",
        product_docs,
        ROOT / ".codex-plugin",
        ROOT / ".claude-plugin",
        ROOT / ".agents",
    )
    for root_path in active_legacy_paths:
        paths = [root_path] if root_path.is_file() else root_path.rglob("*")
        for path in paths:
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for legacy_term in LEGACY_TERMS:
                if legacy_term in content:
                    errors.append(
                        f"Legacy skill or memory name '{legacy_term}' remains: "
                        f"{path.relative_to(ROOT)}"
                    )
            for source_term in OVERRESTRICTIVE_SOURCE_TERMS:
                if source_term in content:
                    errors.append(
                        f"Overrestrictive source boundary '{source_term}' remains: "
                        f"{path.relative_to(ROOT)}"
                    )

    for path in ROOT.rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            placeholder = "[" + "TODO:"
            if placeholder in text:
                errors.append(f"Placeholder remains: {path.relative_to(ROOT)}")

    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        return 1

    print(
        f"[OK] Product Studio: {len(skill_names)} skills, "
        f"{len(TEMPLATE_SECTIONS)} lifecycle templates"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
