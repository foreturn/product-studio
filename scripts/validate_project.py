#!/usr/bin/env python3
"""Validate Product Studio's five-skill and current-code-memory contracts."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
import tempfile
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE_BASE_COMMIT = "9efef58ddb3f3a4bebcf856f6c2eef7ca7a53194"
SKILL_ORDER = ("router", "design", "backend", "frontend", "verification")
SKILLS = set(SKILL_ORDER)
MEMORY_OWNERS = ("design", "backend", "frontend", "verification")
MEMORY_FIELDS = (
    "当前实现",
    "源码锚点",
    "关联与消费者",
    "验证证据",
    "重验条件",
)
REFERENCE_SECTIONS = (
    "目录",
    "角色职责",
    "核心能力",
    "常见误判",
)
REFERENCE_SPECS: dict[str, dict[str, tuple[tuple[str, ...], str]]] = {
    "router": {
        "references/delivery-capabilities.md": (
            (
                "意图归类",
                "切片与排程",
                "依赖协调",
                "风险管理",
                "质量门禁",
                "决策与变更控制",
                "交付沟通",
            ),
            "ac34e4102c70f9740260a28fe91caa2c79e33c0b75ee70fc58ff02464c8f953b",
        ),
    },
    "design": {
        "references/architecture-principles.md": (
            (
                "系统建模",
                "边界与契约设计",
                "质量属性权衡",
                "一致性与故障设计",
                "安全与权限边界",
                "可观测与可运行性",
                "演进与迁移",
            ),
            "4bad1430de9a25bbe80fe5343817c542eea81bfe99d45a1a7ef83706501317aa",
        ),
    },
    "backend": {
        "references/backend-design-principles.md": (
            (
                "领域建模",
                "API 与错误契约",
                "数据建模与迁移",
                "权限与安全",
                "一致性与并发",
                "集成与可靠性",
                "性能与可观测性",
                "测试策略",
            ),
            "87892dce9392a8afb4fefc57db6fe7fcee6ffa55db447b187d05f1306d825bed",
        ),
    },
    "frontend": {
        "references/frontend-design-principles.md": (
            (
                "易用性与任务效率",
                "交互设计",
                "信息架构",
                "布局与响应式",
                "视觉协调",
                "可访问性",
                "组件与状态工程",
                "前端性能与视觉验收",
            ),
            "26b01b74338db328ae288c31a040a7b69e21d795efa9a489d52c007c5c135dcb",
        ),
    },
    "verification": {
        "references/verification-principles.md": (
            (
                "需求追溯",
                "风险建模",
                "分层测试设计",
                "用户体验验收",
                "服务端与数据验收",
                "非功能验证",
                "回归分析",
                "证据审计",
            ),
            "16ad4c5f94fcd5f7d68ddf7c379ce78d487f1b8631cd45f50e27026fbccc13d0",
        ),
    },
}
MEMORY_KEY_PATTERNS = {
    "design": re.compile(
        r"^design:(?:product:(?:journey|rule|acceptance)|"
        r"system:(?:boundary|contract|invariant|decision|migration)):"
        r"[a-z0-9][a-z0-9._/{\}-]*$"
    ),
    "backend": re.compile(
        r"^backend:(?:api|schema|auth|event|integration|config):"
        r"[a-z0-9][a-z0-9._/{\}-]*:[a-z0-9/{][a-z0-9._/{\}-]*$"
    ),
    "frontend": re.compile(
        r"^frontend:(?:page|token|component|layout|state|responsive):"
        r"[a-z0-9][a-z0-9._/{\}-]*:[a-z0-9/{][a-z0-9._/{\}-]*$"
    ),
    "verification": re.compile(
        r"^verification:(?:check|coverage|constraint):"
        r"[a-z0-9][a-z0-9._/{\}-]*:[a-z0-9/{][a-z0-9._/{\}-]*$"
    ),
}
TEMPLATE_SKELETONS = {
    "design": "design:system:contract:order-creation",
    "backend": "backend:api:post:/orders",
    "frontend": "frontend:token:default:color-primary",
    "verification": "verification:check:api:order-idempotency",
}
LEGACY_INVOCATION = re.compile(r"\$(?:delivery|discovery|architecture|release)\b")
LEGACY_ROLE_PATH = re.compile(
    r"(?:skills|templates|docs/product-studio)[\\/]"
    r"(?:delivery|discovery|architecture|release)(?:[\\/.]|\b)",
    re.IGNORECASE,
)
FIELD_PATTERN = re.compile(r"(?m)^-\s+\*\*([^*]+)\*\*：\s*(.*)$")
PLACEHOLDER_PATTERN = re.compile(r"<[^>]+>|\b(?:TODO|TBD)\b", re.IGNORECASE)


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def read_text(path: Path, root: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"Cannot read {rel(path, root)}: {exc}")
        return ""


def load_json(path: Path, root: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Invalid JSON {rel(path, root)}: {exc}")
        return None


def parse_frontmatter(
    path: Path, content: str, root: Path, errors: list[str]
) -> dict[str, str]:
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", content, re.DOTALL)
    if not match:
        errors.append(f"Missing YAML frontmatter: {rel(path, root)}")
        return {}
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            errors.append(f"Malformed frontmatter line in {rel(path, root)}: {line}")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if key in values:
            errors.append(f"Duplicate frontmatter key '{key}': {rel(path, root)}")
        values[key] = value
    return values


def headings(content: str, level: int) -> list[str]:
    marks = "#" * level
    return [
        match.group(1).strip()
        for match in re.finditer(rf"(?m)^{re.escape(marks)}\s+(.+?)\s*$", content)
    ]


def markdown_section(content: str, level: int, title: str) -> str | None:
    marks = "#" * level
    start = re.search(rf"(?m)^{re.escape(marks)}\s+{re.escape(title)}\s*$", content)
    if not start:
        return None
    following = re.search(rf"(?m)^#{{1,{level}}}\s+", content[start.end() :])
    end = start.end() + following.start() if following else len(content)
    return content[start.end() : end].strip()


def heading_blocks(content: str, level: int) -> list[tuple[str, str]]:
    marks = "#" * level
    matches = list(re.finditer(rf"(?m)^{re.escape(marks)}\s+(.+?)\s*$", content))
    blocks: list[tuple[str, str]] = []
    for match in matches:
        following = re.search(rf"(?m)^#{{1,{level}}}\s+", content[match.end() :])
        end = match.end() + following.start() if following else len(content)
        blocks.append((match.group(1).strip(), content[match.end() : end].strip()))
    return blocks


def require_terms(
    path: Path,
    content: str,
    terms: tuple[str, ...],
    root: Path,
    errors: list[str],
    contract: str,
) -> None:
    for term in terms:
        if term not in content:
            errors.append(f"Missing {contract} term '{term}': {rel(path, root)}")


def parse_yaml_value(content: str, key: str) -> str | None:
    match = re.search(rf"(?m)^\s*{re.escape(key)}:\s*(.+?)\s*$", content)
    if not match:
        return None
    value = match.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value


def validate_field_block(
    path: Path,
    block: str,
    expected: tuple[str, ...],
    root: Path,
    errors: list[str],
    label: str,
    *,
    allow_placeholders: bool,
) -> dict[str, str]:
    matches = list(FIELD_PATTERN.finditer(block))
    names = tuple(match.group(1).strip() for match in matches)
    if names != expected:
        errors.append(
            f"{label} fields must be exactly {list(expected)}, got {list(names)}: "
            f"{rel(path, root)}"
        )
    values: dict[str, str] = {}
    for match in matches:
        name = match.group(1).strip()
        value = match.group(2).strip()
        values[name] = value
        if not value:
            errors.append(f"Empty field '{name}' in {label}: {rel(path, root)}")
        if not allow_placeholders and PLACEHOLDER_PATTERN.search(value):
            errors.append(f"Placeholder in field '{name}' of {label}: {rel(path, root)}")
    return values


def is_rfc3339_with_offset(value: str) -> bool:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return "T" in value and parsed.tzinfo is not None


def validate_manifests(root: Path, errors: list[str]) -> None:
    codex_path = root / ".codex-plugin" / "plugin.json"
    claude_path = root / ".claude-plugin" / "plugin.json"
    claude_market_path = root / ".claude-plugin" / "marketplace.json"
    codex_market_path = root / ".agents" / "plugins" / "marketplace.json"
    for path in (codex_path, claude_path, claude_market_path, codex_market_path):
        if not path.is_file():
            errors.append(f"Missing required manifest: {rel(path, root)}")
    codex = load_json(codex_path, root, errors)
    claude = load_json(claude_path, root, errors)
    claude_market = load_json(claude_market_path, root, errors)
    codex_market = load_json(codex_market_path, root, errors)
    if isinstance(codex, dict) and isinstance(claude, dict):
        for key in ("name", "version", "description", "author", "keywords", "skills"):
            if codex.get(key) != claude.get(key):
                errors.append(f"Codex and Claude manifest field differs: {key}")
        if codex.get("name") != "product-studio" or codex.get("skills") != "./skills/":
            errors.append("Plugin manifest name or skills path is invalid")
        require_terms(
            codex_path,
            str(codex.get("description", "")),
            ("五个技能", "路由", "产品架构", "后端", "前端", "测试验证"),
            root,
            errors,
            "manifest",
        )
        interface = codex.get("interface")
        author = codex.get("author")
        if not isinstance(interface, dict) or not isinstance(author, dict):
            errors.append("Codex publisher or interface metadata is incomplete")
        elif interface.get("developerName") != author.get("name"):
            errors.append("Codex developerName differs from author")
    if isinstance(claude_market, dict) and isinstance(claude, dict):
        plugins = claude_market.get("plugins")
        plugin = plugins[0] if isinstance(plugins, list) and len(plugins) == 1 else None
        if not isinstance(plugin, dict):
            errors.append("Claude marketplace must contain exactly one plugin")
        else:
            if plugin.get("name") != claude.get("name") or plugin.get("source") != "./":
                errors.append("Claude marketplace plugin identity or source differs")
            if plugin.get("description") != claude.get("description"):
                errors.append("Claude marketplace description differs from manifest")
    if isinstance(codex_market, dict):
        plugins = codex_market.get("plugins")
        plugin = plugins[0] if isinstance(plugins, list) and len(plugins) == 1 else None
        if not isinstance(plugin, dict) or plugin.get("name") != "product-studio":
            errors.append("Codex marketplace must contain the product-studio plugin")
        elif not isinstance(plugin.get("source"), dict) or plugin["source"].get("url") != (
            "https://github.com/foreturn/product-studio.git"
        ):
            errors.append("Codex marketplace source URL is invalid")


def validate_reference(
    root: Path,
    skill: str,
    relative_path: str,
    expected_cards: tuple[str, ...],
    expected_sha256: str,
    errors: list[str],
) -> None:
    path = root / "skills" / skill / relative_path
    if not path.is_file():
        errors.append(f"Missing capability reference: {rel(path, root)}")
        return
    content = read_text(path, root, errors)
    digest = hashlib.sha256(content.replace("\r\n", "\n").encode("utf-8")).hexdigest()
    if digest != expected_sha256:
        errors.append(
            "Capability reference differs from the curated baseline derived from "
            f"{REFERENCE_BASE_COMMIT}: {rel(path, root)}"
        )
    actual_sections = tuple(headings(content, 2))
    if actual_sections != REFERENCE_SECTIONS:
        errors.append(
            f"Capability reference sections must be exactly {list(REFERENCE_SECTIONS)}, "
            f"got {list(actual_sections)}: {rel(path, root)}"
        )
    for section_name in REFERENCE_SECTIONS:
        body = markdown_section(content, 2, section_name)
        if not body:
            errors.append(f"Empty reference section '{section_name}': {rel(path, root)}")
    core = markdown_section(content, 2, "核心能力") or ""
    cards = heading_blocks(core, 3)
    titles = tuple(title for title, _ in cards)
    if titles != expected_cards:
        errors.append(
            f"Professional capability cards differ: expected={list(expected_cards)}, "
            f"got={list(titles)}: {rel(path, root)}"
        )
    for title, body in cards:
        if len(re.findall(r"(?m)^-\s+", body)) < 5:
            errors.append(f"Capability card is too shallow '{title}': {rel(path, root)}")
    if "docs/product-studio/" in content or "templates/" in content:
        errors.append(f"Capability reference contains memory/template rules: {rel(path, root)}")


def validate_memory_skill(
    root: Path, skill: str, content: str, path: Path, errors: list[str]
) -> None:
    require_terms(
        path,
        content,
        (
            "schema 3",
            f"docs/product-studio/{skill}.md",
            f"../../templates/{skill}.md",
            "当前实现",
            "源码锚点",
            "关联与消费者",
            "验证证据",
            "重验条件",
            "superseded",
            "Git",
        ),
        root,
        errors,
        "current-code-memory",
    )


def validate_skill(root: Path, skill: str, errors: list[str]) -> None:
    skill_dir = root / "skills" / skill
    path = skill_dir / "SKILL.md"
    if not path.is_file():
        errors.append(f"Missing SKILL.md: {rel(path, root)}")
        return
    content = read_text(path, root, errors)
    frontmatter = parse_frontmatter(path, content, root, errors)
    if set(frontmatter) != {"name", "description"}:
        errors.append(f"Skill frontmatter must contain only name and description: {rel(path, root)}")
    if frontmatter.get("name") != skill or len(frontmatter.get("description", "")) < 45:
        errors.append(f"Skill name or description is invalid: {rel(path, root)}")
    if len(headings(content, 2)) < 5:
        errors.append(f"Skill workflow is underspecified: {rel(path, root)}")
    expected_refs = REFERENCE_SPECS[skill]
    reference_dir = skill_dir / "references"
    actual_refs = {
        str(item.relative_to(skill_dir)).replace("\\", "/")
        for item in reference_dir.glob("*.md")
    }
    if actual_refs != set(expected_refs):
        errors.append(
            f"Capability reference set differs for {skill}: "
            f"missing={sorted(set(expected_refs) - actual_refs)}, "
            f"extra={sorted(actual_refs - set(expected_refs))}"
        )
    for relative_path, (cards, digest) in expected_refs.items():
        if relative_path not in content:
            errors.append(f"SKILL.md does not load {relative_path}: {rel(path, root)}")
        validate_reference(root, skill, relative_path, cards, digest, errors)
    metadata_path = skill_dir / "agents" / "openai.yaml"
    metadata = read_text(metadata_path, root, errors)
    for key in ("display_name", "short_description", "default_prompt"):
        if not parse_yaml_value(metadata, key):
            errors.append(f"Missing metadata field '{key}': {rel(metadata_path, root)}")
    if f"${skill}" not in (parse_yaml_value(metadata, "default_prompt") or ""):
        errors.append(f"Metadata does not invoke ${skill}: {rel(metadata_path, root)}")
    if skill in MEMORY_OWNERS:
        validate_memory_skill(root, skill, content, path, errors)
    else:
        if re.search(r"docs/product-studio/router\.md|templates/router\.md|memory:\s*router", content):
            errors.append("router must not own project memory or a memory template")
    if skill == "router":
        require_terms(
            path,
            content,
            (
                "明确前端改动",
                "明确后端改动",
                "模糊或跨边界改动",
                "不计作跨领域触发条件",
                "具体 API 契约里程碑",
                "输入快照一致",
                "写集合",
                "代码权限不等于生产操作授权",
            ),
            root,
            errors,
            "router",
        )
    elif skill == "design":
        require_terms(
            path,
            content,
            (
                "只用产品模式",
                "只用系统模式",
                "双模式",
                "跳过本技能",
                "产品模式不加载独立 reference",
                "architecture-principles.md",
                "不属于 `docs/product-studio/` 代码事实记忆",
            ),
            root,
            errors,
            "design mode",
        )
    elif skill == "backend":
        require_terms(path, content, ("API", "Schema", "权限", "并发", "幂等", "$verification", "$router"), root, errors, "backend")
    elif skill == "frontend":
        require_terms(path, content, ("设计令牌", "响应式", "可访问性", "真实浏览器", "$verification"), root, errors, "frontend")
    elif skill == "verification":
        require_terms(path, content, ("需求追溯", "风险", "分层", "真实", "失败", "阻塞", "既有问题", "$router"), root, errors, "verification")


def validate_template(root: Path, owner: str, errors: list[str]) -> None:
    path = root / "templates" / f"{owner}.md"
    content = read_text(path, root, errors)
    fields = parse_frontmatter(path, content, root, errors)
    expected = {
        "schema": "3",
        "memory": owner,
        "scope": "current-project-code",
        "project_root": "",
        "updated_at": "",
    }
    if fields != expected:
        errors.append(f"Schema 3 template frontmatter is invalid: {rel(path, root)}")
    if tuple(headings(content, 2)) != ("事实键", "当前代码事实"):
        errors.append(f"Template sections are invalid: {rel(path, root)}")
    require_terms(path, content, ("首次", "不再次套用模板", "Git"), root, errors, "template")
    current = markdown_section(content, 2, "当前代码事实") or ""
    cards = heading_blocks(current, 3)
    if len(cards) != 1 or cards[0][0] != TEMPLATE_SKELETONS[owner]:
        errors.append(
            f"Template skeleton must be '{TEMPLATE_SKELETONS[owner]}': {rel(path, root)}"
        )
        return
    validate_field_block(
        path,
        cards[0][1],
        MEMORY_FIELDS,
        root,
        errors,
        "template fact skeleton",
        allow_placeholders=True,
    )


def validate_source_anchor(
    root: Path, memory_path: Path, key: str, anchor: str, errors: list[str]
) -> bool:
    source_path, separator, fragment = anchor.partition("#")
    if not source_path or "://" in source_path:
        return False
    candidate = root / source_path
    if not candidate.exists():
        errors.append(f"Missing source anchor '{source_path}' in fact '{key}': {rel(memory_path, root)}")
        return False
    if not separator or not fragment:
        errors.append(f"Source anchor needs '#precise-location' in fact '{key}': {anchor}")
        return True
    if candidate.suffix.lower() == ".md" and fragment not in [
        title for level in range(1, 7) for title in headings(candidate.read_text(encoding="utf-8"), level)
    ]:
        errors.append(f"Missing Markdown heading '#{fragment}' for fact '{key}': {anchor}")
    if candidate.suffix.lower() == ".py" and not re.search(
        rf"(?m)^(?:def|class)\s+{re.escape(fragment)}\b", candidate.read_text(encoding="utf-8")
    ):
        errors.append(f"Missing Python symbol '#{fragment}' for fact '{key}': {anchor}")
    return True


def validate_memory_file(
    root: Path,
    owner: str,
    path: Path,
    all_keys: dict[str, Path],
    pending_refs: list[tuple[Path, str]],
    errors: list[str],
) -> None:
    content = read_text(path, root, errors)
    fields = parse_frontmatter(path, content, root, errors)
    if set(fields) != {"schema", "memory", "scope", "project_root", "updated_at"}:
        errors.append(f"Code-memory frontmatter fields are invalid: {rel(path, root)}")
    if fields.get("schema") != "3" or fields.get("memory") != owner:
        errors.append(f"Code-memory schema or owner is invalid: {rel(path, root)}")
    if fields.get("scope") != "current-project-code" or not fields.get("project_root"):
        errors.append(f"Code-memory scope or project_root is invalid: {rel(path, root)}")
    if not is_rfc3339_with_offset(fields.get("updated_at", "")):
        errors.append(f"Code-memory updated_at needs RFC3339 offset: {rel(path, root)}")
    if "<!--" in content or PLACEHOLDER_PATTERN.search(content):
        errors.append(f"Template guidance or placeholder remains: {rel(path, root)}")
    for forbidden in ("## 事实键", "任务摘要", "恢复摘要", "动作队列", "取代关系", "superseded", "置信度", "过程日志"):
        if forbidden in content:
            errors.append(f"Historical/process memory term '{forbidden}' remains: {rel(path, root)}")
    if tuple(headings(content, 2)) != ("当前代码事实",):
        errors.append(f"Instantiated memory must contain only 当前代码事实: {rel(path, root)}")
    cards = heading_blocks(markdown_section(content, 2, "当前代码事实") or "", 3)
    if not cards:
        errors.append(f"Empty code-memory file must not exist: {rel(path, root)}")
    for key, block in cards:
        if not MEMORY_KEY_PATTERNS[owner].fullmatch(key):
            errors.append(f"Invalid {owner} semantic fact key '{key}': {rel(path, root)}")
        if key in all_keys:
            errors.append(f"Duplicate fact key '{key}': {rel(path, root)}")
        all_keys[key] = path
        values = validate_field_block(path, block, MEMORY_FIELDS, root, errors, f"code fact '{key}'", allow_placeholders=False)
        for field in MEMORY_FIELDS:
            value = values.get(field, "")
            if field == "关联与消费者" and value == "无":
                continue
            if len(value) < 12:
                errors.append(f"Code fact '{key}' field '{field}' is too terse: {rel(path, root)}")
        anchors = re.findall(r"`([^`]+)`", values.get("源码锚点", ""))
        resolved_anchors = [
            validate_source_anchor(root, path, key, anchor, errors) for anchor in anchors
        ]
        if not any(resolved_anchors):
            errors.append(f"Code fact '{key}' needs a repository source anchor: {rel(path, root)}")
        for linked in re.findall(
            r"`((?:design|backend|frontend|verification):[a-z0-9:._/{\}-]+)`",
            values.get("关联与消费者", ""),
        ):
            pending_refs.append((path, linked))


def validate_readme(root: Path, errors: list[str]) -> None:
    path = root / "README.md"
    content = read_text(path, root, errors)
    require_terms(
        path,
        content,
        (
            "五个 Skill",
            "`router`",
            "`design`",
            "`backend`",
            "`frontend`",
            "`verification`",
            "9efef58ddb3f3a4bebcf856f6c2eef7ca7a53194",
            "目录—角色职责—核心能力—常见误判",
            "当前代码事实",
            "router` 不拥有记忆",
        ),
        root,
        errors,
        "README",
    )


def validate_legacy_surfaces(root: Path, errors: list[str]) -> None:
    surfaces = (root / "README.md", root / "skills", root / "templates", root / "docs" / "product-studio", root / ".codex-plugin", root / ".claude-plugin", root / ".agents")
    for surface in surfaces:
        paths = [surface] if surface.is_file() else surface.rglob("*") if surface.exists() else []
        for path in paths:
            if not path.is_file():
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for pattern, label in ((LEGACY_INVOCATION, "legacy skill invocation"), (LEGACY_ROLE_PATH, "legacy role path")):
                match = pattern.search(content)
                if match:
                    errors.append(f"{label} '{match.group(0)}' remains: {rel(path, root)}")


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    skills_dir = root / "skills"
    templates_dir = root / "templates"
    docs_dir = root / "docs" / "product-studio"
    actual_skills = {path.name for path in skills_dir.iterdir() if path.is_dir()}
    if actual_skills != SKILLS:
        errors.append(f"Skill directories must be exactly {list(SKILL_ORDER)}")
    expected_templates = {f"{owner}.md" for owner in MEMORY_OWNERS}
    if {path.name for path in templates_dir.glob("*.md")} != expected_templates:
        errors.append("Code-memory templates do not match the four memory owners")
    root_refs = root / "references"
    if root_refs.exists() and any(path.is_file() for path in root_refs.rglob("*")):
        errors.append("Root-level references are not an active capability source")
    validate_manifests(root, errors)
    for skill in SKILL_ORDER:
        validate_skill(root, skill, errors)
    for owner in MEMORY_OWNERS:
        validate_template(root, owner, errors)
    allowed_memories = {f"{owner}.md" for owner in MEMORY_OWNERS}
    actual_memories = {path.name for path in docs_dir.glob("*.md")} if docs_dir.exists() else set()
    if not actual_memories <= allowed_memories:
        errors.append(f"Unknown project memory files: {sorted(actual_memories - allowed_memories)}")
    all_keys: dict[str, Path] = {}
    pending_refs: list[tuple[Path, str]] = []
    for filename in sorted(actual_memories):
        owner = filename.removesuffix(".md")
        validate_memory_file(root, owner, docs_dir / filename, all_keys, pending_refs, errors)
    for source, linked in pending_refs:
        if linked not in all_keys:
            errors.append(f"Dangling fact-key reference '{linked}': {rel(source, root)}")
    validate_readme(root, errors)
    validate_legacy_surfaces(root, errors)
    for path in root.rglob("*"):
        if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts:
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if "[" + "TODO:" in content:
                errors.append(f"TODO placeholder remains: {rel(path, root)}")
    return errors


def run_negative_self_tests() -> list[str]:
    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="product-studio-validator-") as temp_dir:
        baseline = Path(temp_dir) / "baseline"
        shutil.copytree(ROOT, baseline, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
        baseline_errors = validate(baseline)
        if baseline_errors:
            return ["negative-test baseline differs from the real tree: " + baseline_errors[0]]

        def run_case(name: str, mutate: object) -> None:
            case_root = Path(temp_dir) / name
            shutil.copytree(baseline, case_root)
            mutate(case_root)  # type: ignore[operator]
            if not validate(case_root):
                failures.append(f"validator accepted negative case: {name}")

        def add_sixth_skill(root: Path) -> None:
            shutil.copytree(root / "skills" / "backend", root / "skills" / "release")

        def add_router_memory(root: Path) -> None:
            shutil.copy2(root / "templates" / "backend.md", root / "templates" / "router.md")

        def remove_design_reference(root: Path) -> None:
            (root / "skills" / "design" / "references" / "architecture-principles.md").unlink()

        def add_unexpected_reference(root: Path) -> None:
            (root / "skills" / "router" / "references" / "extra.md").write_text("# extra\n", encoding="utf-8")

        def modify_reference(root: Path) -> None:
            path = root / "skills" / "backend" / "references" / "backend-design-principles.md"
            path.write_text(path.read_text(encoding="utf-8").replace("领域建模", "领域模型", 1), encoding="utf-8")

        def corrupt_memory_field(root: Path) -> None:
            path = root / "docs" / "product-studio" / "design.md"
            path.write_text(path.read_text(encoding="utf-8").replace("**重验条件**", "**复查条件**", 1), encoding="utf-8")

        def duplicate_memory_key(root: Path) -> None:
            path = root / "docs" / "product-studio" / "design.md"
            content = path.read_text(encoding="utf-8")
            card = re.search(r"(?ms)^### design:system:boundary:skill-topology\s*$.*?(?=^### |\Z)", content)
            if card:
                path.write_text(content.rstrip() + "\n\n" + card.group(0).rstrip() + "\n", encoding="utf-8")

        def malformed_memory_key(root: Path) -> None:
            path = root / "docs" / "product-studio" / "design.md"
            path.write_text(path.read_text(encoding="utf-8").replace("design:system:boundary:skill-topology", "design:system:boundary", 1), encoding="utf-8")

        def imprecise_anchor(root: Path) -> None:
            path = root / "docs" / "product-studio" / "design.md"
            path.write_text(path.read_text(encoding="utf-8").replace("`skills/router/SKILL.md#直达与触发`", "`skills/router/SKILL.md`", 1), encoding="utf-8")

        def invalid_template_skeleton(root: Path) -> None:
            path = root / "templates" / "backend.md"
            path.write_text(path.read_text(encoding="utf-8").replace("backend:api:post:/orders", "backend:api:orders", 1), encoding="utf-8")

        def legacy_invocation(root: Path) -> None:
            path = root / "README.md"
            path.write_text(path.read_text(encoding="utf-8") + "\n$" + "delivery\n", encoding="utf-8")

        def overroute_verification(root: Path) -> None:
            path = root / "skills" / "router" / "SKILL.md"
            path.write_text(path.read_text(encoding="utf-8").replace("不计作跨领域触发条件", "计作跨领域触发条件", 1), encoding="utf-8")

        def remove_api_milestone(root: Path) -> None:
            path = root / "skills" / "router" / "SKILL.md"
            path.write_text(path.read_text(encoding="utf-8").replace("具体 API 契约里程碑", "接口约定", 1), encoding="utf-8")

        cases = (
            ("sixth-skill", add_sixth_skill),
            ("router-memory", add_router_memory),
            ("missing-design-reference", remove_design_reference),
            ("unexpected-reference", add_unexpected_reference),
            ("modified-reference-content", modify_reference),
            ("invalid-memory-field", corrupt_memory_field),
            ("duplicate-memory-key", duplicate_memory_key),
            ("malformed-memory-key", malformed_memory_key),
            ("imprecise-source-anchor", imprecise_anchor),
            ("invalid-template-skeleton", invalid_template_skeleton),
            ("legacy-invocation", legacy_invocation),
            ("overrouted-terminal-verification", overroute_verification),
            ("missing-api-contract-milestone", remove_api_milestone),
        )
        declared = f"{len(cases)} 类退化"
        for path in (ROOT / "scripts" / "README.md", ROOT / "docs" / "product-studio" / "verification.md"):
            if declared not in path.read_text(encoding="utf-8"):
                failures.append(f"negative self-test count is not synchronized: expected '{declared}'")
        for name, mutation in cases:
            run_case(name, mutation)
    return failures


def main() -> int:
    errors = validate(ROOT)
    if not errors and "--self-test" in sys.argv[1:]:
        errors.extend(run_negative_self_tests())
    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        return 1
    suffix = ", negative regressions rejected" if "--self-test" in sys.argv[1:] else ""
    reference_count = sum(len(references) for references in REFERENCE_SPECS.values())
    print(f"[OK] Product Studio: {len(SKILL_ORDER)} skills, {reference_count} curated capability references, {len(MEMORY_OWNERS)} code-memory templates{suffix}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
