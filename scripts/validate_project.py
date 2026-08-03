#!/usr/bin/env python3
"""Validate Product Studio's six-skill and current-code-memory contracts."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE_BASE_COMMIT = "9efef58ddb3f3a4bebcf856f6c2eef7ca7a53194"
SKILL_ORDER = ("router", "design", "architecture", "backend", "frontend", "verification")
SKILLS = set(SKILL_ORDER)
MEMORY_OWNERS = ("design", "architecture", "backend", "frontend", "verification")
MEMORY_FIELDS = (
    "当前事实",
    "代码定位",
    "影响范围",
    "验证入口",
)
MEMORY_REFERENCE = "references/memory.md"
MEMORY_REFERENCE_SECTIONS = (
    "收录门槛",
    "实例格式",
    "终态同步",
    "禁止内容",
)
REFERENCE_SECTIONS = (
    "目录",
    "角色职责",
    "核心能力",
    "常见误判",
)
REFERENCE_SPECS: dict[str, dict[str, tuple[tuple[str, ...], str]]] = {
    "router": {
        "references/principles.md": (
            (
                "意图归类",
                "切片与排程",
                "依赖协调",
                "风险管理",
                "质量门禁",
                "决策与变更控制",
                "交付沟通",
            ),
            "c103483eabdd691f50f862f646ad30c1cd4b8a77a3841b35e45e07149ababa2b",
        ),
    },
    "design": {
        "references/principles.md": (
            (
                "问题定义",
                "用户与任务建模",
                "证据化联想",
                "旅程与状态设计",
                "范围与优先级",
                "成功衡量",
                "澄清沟通",
            ),
            "a95bca7105a835bb3a5bac4b7495326c769ebdc8239db24e66fa4c8219bb7f6a",
        ),
    },
    "architecture": {
        "references/principles.md": (
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
        "references/principles.md": (
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
        "references/principles.md": (
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
        "references/principles.md": (
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
FORMAL_FACT_KEY_PATTERN = re.compile(
    r"^(?:design|architecture|backend|frontend|verification):[a-z]+:[a-z0-9][a-z0-9-]*$"
)
PROCESS_TOPIC_PATTERN = re.compile(
    r"(?:迁移|重构|改造|改名|替换|升级|变更)(?:阶段|进度|记录|过程)?"
    r"|(?:migration|refactor|migrate|change)(?:[-_:/]|$)",
    re.IGNORECASE,
)
PROCESS_FACT_PATTERN = re.compile(
    r"(?:本次|本轮|此次).{0,24}(?:迁移|重构|改造|改名|替换|升级|变更)"
    r"|从\s*[^，。；]{1,40}\s*(?:迁移|改为|重构|替换)\s*(?:到|为)"
    r"|(?:迁移|重构|改造|改名|替换|升级|变更)(?:阶段|进度|记录)",
    re.IGNORECASE,
)
LEGACY_INVOCATION = re.compile(r"\$(?:delivery|discovery|release)\b")
LEGACY_ROLE_PATH = re.compile(
    r"(?:skills|templates|docs/product-studio)[\\/]"
    r"(?:delivery|discovery|release)(?:[\\/.]|\b)",
    re.IGNORECASE,
)
LEGACY_MEMORY_PATH = re.compile(
    r"(?:\.\./\.\./)?references/project-memory\.md"
    r"|(?:\.\./\.\./)?templates/(?:design|architecture|backend|frontend|verification|router)\.md"
)
FIELD_LINE_PATTERN = re.compile(r"^-\s+\*\*([^*]+)\*\*：\s*(.*)$")
PLACEHOLDER_PATTERN = re.compile(r"<[^>]+>|\b(?:TODO|TBD)\b", re.IGNORECASE)
SESSION_SUMMARY_PATTERN = re.compile(r"^(?:本次|本轮|此次)(?:任务|修改|开发|编码|已)?")
SECRET_PATTERN = re.compile(
    r"(?ix)(?:"
    r"\b(?:password|passwd|pwd|secret|api[_-]?key|access[_-]?token|"
    r"refresh[_-]?token|private[_-]?key)\b\s*[:=]\s*[^\s,;]+"
    r"|\b(?:sk|ghp|github_pat)-?[A-Za-z0-9_]{16,}\b"
    r"|\bAKIA[A-Z0-9]{16}\b"
    r")"
)
MEMORY_SYNC_DENIAL_PATTERN = re.compile(
    r"(?m)^[ \t]*(?:[-*]\s+)?(?:"
    r"(?:无需|不必|不再|拒绝).{0,8}(?:同步|更新).{0,12}(?:事实|记忆)"
    r"|(?:不得|禁止).{0,8}(?:同步|更新)(?:任何|全部|所有).{0,12}(?:事实|记忆)"
    r"|(?:不得|禁止).{0,8}(?:记忆同步|事实更新)"
    r")"
)
EXTERNAL_WRITE_PERMISSION_PATTERN = re.compile(
    r"(?<!不)(?<!不应)(?<!不得)(?:允许|可以|可在)"
    r".{0,24}(?:生产环境|外部环境)"
    r".{0,24}(?:外部写入|环境写入|环境操作|生产写入)"
)


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


def mask_fenced_code(content: str) -> str:
    masked: list[str] = []
    fence_char: str | None = None
    fence_length = 0
    for line in content.splitlines(keepends=True):
        if fence_char is None:
            opening = re.match(r"^\s*(`{3,}|~{3,})", line)
            if not opening:
                masked.append(line)
                continue
            marker = opening.group(1)
            fence_char = marker[0]
            fence_length = len(marker)
        else:
            closing = re.match(
                rf"^\s*{re.escape(fence_char)}{{{fence_length},}}[ \t]*(?:\r?\n)?$",
                line,
            )
            if closing:
                fence_char = None
                fence_length = 0
        masked.append("".join(char if char in "\r\n" else " " for char in line))
    return "".join(masked)


def headings(content: str, level: int) -> list[str]:
    visible = mask_fenced_code(content)
    marks = "#" * level
    return [
        match.group(1).strip()
        for match in re.finditer(rf"(?m)^{re.escape(marks)}\s+(.+?)\s*$", visible)
    ]


def markdown_section(content: str, level: int, title: str) -> str | None:
    visible = mask_fenced_code(content)
    marks = "#" * level
    start = re.search(rf"(?m)^{re.escape(marks)}\s+{re.escape(title)}\s*$", visible)
    if not start:
        return None
    following = re.search(rf"(?m)^#{{1,{level}}}\s+", visible[start.end() :])
    end = start.end() + following.start() if following else len(content)
    return content[start.end() : end].strip()


def heading_blocks(content: str, level: int) -> list[tuple[str, str]]:
    visible = mask_fenced_code(content)
    marks = "#" * level
    matches = list(re.finditer(rf"(?m)^{re.escape(marks)}\s+(.+?)\s*$", visible))
    blocks: list[tuple[str, str]] = []
    for match in matches:
        following = re.search(rf"(?m)^#{{1,{level}}}\s+", visible[match.end() :])
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
    matches: list[re.Match[str]] = []
    for line in (item.strip() for item in block.splitlines() if item.strip()):
        match = FIELD_LINE_PATTERN.fullmatch(line)
        if not match:
            errors.append(f"Unexpected content in {label}: {rel(path, root)}")
            continue
        matches.append(match)
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
            ("六个技能", "路由", "产品设计", "架构设计", "后端编码", "前端编码", "测试验证"),
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
    common = markdown_section(content, 2, "常见误判") or ""
    common_lines = [line.strip() for line in common.splitlines() if line.strip()]
    if len(common_lines) < 5 or any(not line.startswith("- ") for line in common_lines):
        errors.append(
            f"Common-misjudgment section must be a flat bullet list: {rel(path, root)}"
        )
    if any(
        term in content
        for term in (
            "docs/product-studio/",
            "templates/",
            "references/memory.md",
        )
    ):
        errors.append(f"Capability reference contains memory/template rules: {rel(path, root)}")


def validate_memory_reference(root: Path, owner: str, errors: list[str]) -> None:
    path = root / "skills" / owner / MEMORY_REFERENCE
    if not path.is_file():
        errors.append(f"Missing skill-owned memory reference: {rel(path, root)}")
        return
    content = read_text(path, root, errors)
    if tuple(headings(content, 2)) != MEMORY_REFERENCE_SECTIONS:
        errors.append(
            f"{owner} memory reference sections must be exactly "
            f"{list(MEMORY_REFERENCE_SECTIONS)}: {rel(path, root)}"
        )

    require_terms(
        path,
        content,
        (
            "唯一规则与实例格式",
            f"docs/product-studio/{owner}.md",
            f"只由 `{owner}` 维护",
        ),
        root,
        errors,
        f"{owner} memory reference",
    )
    section_terms = {
        "收录门槛": (
            "最终代码",
            "当前",
            "预计后续",
            "不按任务",
            "重构",
            "迁移",
            "不得成为主题或事实正文",
        ),
        "实例格式": (
            "稳定事实主题",
            "不含 Owner",
            *MEMORY_FIELDS,
        ),
        "终态同步": (
            "最终差异",
            "原位改写",
            "memory: 0 facts changed",
            "最后一个主题删除后移除整册",
            "项目校验",
        ),
        "禁止内容": (
            "任务摘要",
            "前后对比",
            "过程事实",
            "单轮通过",
            "其他项目事实",
            "密钥",
            "Git",
            "静态校验只能证明",
            "语义新鲜度",
        ),
    }
    for section_name, terms in section_terms.items():
        body = markdown_section(content, 2, section_name)
        if not body:
            errors.append(f"Empty {owner} memory section '{section_name}': {rel(path, root)}")
            continue
        require_terms(path, body, terms, root, errors, f"{owner} memory {section_name}")

    for other_owner in MEMORY_OWNERS:
        if other_owner != owner and f"docs/product-studio/{other_owner}.md" in content:
            errors.append(
                f"{owner} memory reference contains foreign owner '{other_owner}': "
                f"{rel(path, root)}"
            )

    format_section = markdown_section(content, 2, "实例格式") or ""
    skeletons = re.findall(
        r"(?ms)^```markdown[ \t]*\n(.*?)^```[ \t]*$", format_section
    )
    if len(skeletons) != 1:
        errors.append(
            f"{owner} memory reference must contain exactly one Markdown format: "
            f"{rel(path, root)}"
        )
    else:
        skeleton = skeletons[0]
        if re.match(r"\A---\s*$", skeleton, re.MULTILINE):
            errors.append(f"Memory format must not contain frontmatter: {rel(path, root)}")
        if tuple(headings(skeleton, 1)) != (f"{owner} 当前代码事实",):
            errors.append(f"Memory format title is invalid for {owner}: {rel(path, root)}")
        cards = heading_blocks(skeleton, 2)
        if len(cards) != 1 or cards[0][0] != "<稳定事实主题>":
            errors.append(
                f"Memory format topic must be '<稳定事实主题>': {rel(path, root)}"
            )
        else:
            validate_field_block(
                path,
                cards[0][1],
                MEMORY_FIELDS,
                root,
                errors,
                f"{owner} memory format",
                allow_placeholders=True,
            )
    if MEMORY_SYNC_DENIAL_PATTERN.search(content):
        errors.append(f"Contradictory memory sync rule: {rel(path, root)}")


def validate_memory_skill(
    root: Path, skill: str, content: str, path: Path, errors: list[str]
) -> None:
    require_terms(
        path,
        content,
        (
            f"docs/product-studio/{skill}.md",
            f"[{skill} 记忆规则与实例格式](references/memory.md)",
            f"仅按最终代码同步 `{skill}` 自己的事实册",
            "首次确有事实时使用其中格式",
            "不得预建空册",
            "重构、迁移",
            "不入册",
            "memory: 0 facts changed",
        ),
        root,
        errors,
        "current-code-memory",
    )
    if "../../references/project-memory.md" in content or "../../templates/" in content:
        errors.append(f"Legacy root memory path remains: {rel(path, root)}")
    if MEMORY_SYNC_DENIAL_PATTERN.search(content):
        errors.append(f"Contradictory memory sync rule: {rel(path, root)}")


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
        for item in reference_dir.rglob("*")
        if item.is_file()
    }
    expected_ref_set = set(expected_refs)
    if skill in MEMORY_OWNERS:
        expected_ref_set.add(MEMORY_REFERENCE)
    if actual_refs != expected_ref_set:
        errors.append(
            f"Skill reference set differs for {skill}: "
            f"missing={sorted(expected_ref_set - actual_refs)}, "
            f"extra={sorted(actual_refs - expected_ref_set)}"
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
        validate_memory_reference(root, skill, errors)
        validate_memory_skill(root, skill, content, path, errors)
    else:
        if (reference_dir / "memory.md").is_file() or re.search(
            r"docs/product-studio/router\.md|templates/router\.md|memory:\s*router", content
        ):
            errors.append("router must not own a project memory reference or fact store")
    if skill == "router":
        require_terms(
            path,
            content,
            (
                "明确架构设计",
                "明确后端编码",
                "明确前端编码",
                "明确测试验收",
                "系统或技术边界未定",
                "不计作跨领域触发条件",
                "架构契约里程碑",
                "具体 API 契约里程碑",
                "输入快照一致",
                "写集合",
                "里程碑解锁条件",
                "停止编排",
                "最终结果由 `$verification` 独立裁决",
                "事实同步由实际命中的专业 Skill 各自完成",
                "代码权限不等于生产操作授权",
            ),
            root,
            errors,
            "router",
        )
        for forbidden in (
            "## 终态收口",
            "终态类别",
            "`部分完成`",
            "references/memory.md",
            "memory: 0 facts changed",
        ):
            if forbidden in content:
                errors.append(
                    f"Router must not own terminal closure or memory synchronization term "
                    f"'{forbidden}': {rel(path, root)}"
                )
    elif skill == "design":
        require_terms(
            path,
            content,
            (
                "产品设计能力准则",
                "references/principles.md",
                "问题定义",
                "用户与任务建模",
                "证据化联想",
                "旅程与状态设计",
                "范围与优先级",
                "成功衡量",
                "澄清沟通",
                "业务闭环",
                "交互与信息",
                "跳过本技能",
                "$architecture",
                "$backend",
                "$frontend",
                "$verification",
                "纯设计产物",
                "不入册",
            ),
            root,
            errors,
            "product design",
        )
        for forbidden in ("系统模式", "双模式", "负责系统架构"):
            if forbidden in content:
                errors.append(
                    f"Design must not own system architecture term '{forbidden}': "
                    f"{rel(path, root)}"
                )
    elif skill == "architecture":
        require_terms(
            path,
            content,
            (
                "references/principles.md",
                "系统架构",
                "数据所有权",
                "共享不变量",
                "跨边界契约",
                "质量属性",
                "故障",
                "演进",
                "$design",
                "$backend",
                "$frontend",
                "$verification",
                "$router",
                "不得擅自进入代码实现",
            ),
            root,
            errors,
            "system architecture",
        )
    elif skill == "backend":
        require_terms(
            path,
            content,
            (
                "references/principles.md",
                "API",
                "Schema",
                "权限",
                "并发",
                "幂等",
                "$design",
                "$architecture",
                "$verification",
                "$router",
            ),
            root,
            errors,
            "backend implementation",
        )
        if "负责系统架构" in content:
            errors.append(f"Backend must not own system architecture: {rel(path, root)}")
    elif skill == "frontend":
        require_terms(path, content, ("设计令牌", "响应式", "可访问性", "真实浏览器", "$architecture", "$backend", "$verification"), root, errors, "frontend")
    elif skill == "verification":
        require_terms(
            path,
            content,
            (
                "需求追溯",
                "风险",
                "分层",
                "真实",
                "失败",
                "阻塞",
                "既有问题",
                "$router",
                "$architecture",
                "测试用例",
                "不执行外部环境写入或环境操作",
            ),
            root,
            errors,
            "verification",
        )
        if EXTERNAL_WRITE_PERMISSION_PATTERN.search(content):
            errors.append(f"External write permission contradicts verification boundary: {rel(path, root)}")


def validate_source_anchor(
    root: Path, memory_path: Path, key: str, anchor: str, errors: list[str]
) -> bool:
    source_path, separator, fragment = anchor.partition("#")
    if not source_path or "://" in source_path:
        return False
    if Path(source_path).is_absolute() or re.match(r"^[A-Za-z]:[\\/]", source_path):
        errors.append(
            f"Source anchor must be repository-relative in fact '{key}': {anchor}"
        )
        return False
    if ".." in re.split(r"[\\/]", source_path):
        errors.append(f"Source anchor escapes project root in fact '{key}': {anchor}")
        return False
    candidate = (root / source_path).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        errors.append(f"Source anchor escapes project root in fact '{key}': {anchor}")
        return False
    if not candidate.is_file():
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
        rf"(?m)^(?:(?:async\s+)?def|class)\s+{re.escape(fragment)}\b",
        candidate.read_text(encoding="utf-8"),
    ):
        errors.append(f"Missing Python symbol '#{fragment}' for fact '{key}': {anchor}")
    return True


def validate_memory_file(
    root: Path,
    owner: str,
    path: Path,
    errors: list[str],
) -> None:
    content = read_text(path, root, errors)
    body = content.strip()
    if re.match(r"\A---\s*$", body, re.MULTILINE):
        errors.append(f"Frontmatter is forbidden in final code memory: {rel(path, root)}")
    if "<!--" in content or PLACEHOLDER_PATTERN.search(content):
        errors.append(f"Template guidance or placeholder remains: {rel(path, root)}")
    if SECRET_PATTERN.search(content):
        errors.append(f"Possible secret value in code-memory file: {rel(path, root)}")
    for forbidden in (
        "## 事实键",
        "任务摘要",
        "修改文件列表",
        "恢复摘要",
        "动作队列",
        "取代关系",
        "迁移进度",
        "迁移阶段",
        "重构记录",
        "变更记录",
        "superseded",
        "置信度",
        "过程日志",
        "命令流水",
        "本轮通过",
        "commit SHA",
    ):
        if forbidden in content:
            errors.append(f"Historical/process memory term '{forbidden}' remains: {rel(path, root)}")
    if "```" in content:
        errors.append(f"Code fence is forbidden in code-memory file: {rel(path, root)}")
    if tuple(headings(body, 1)) != (f"{owner} 当前代码事实",):
        errors.append(f"Instantiated memory title is invalid: {rel(path, root)}")
    body_match = re.fullmatch(
        rf"# {re.escape(owner)} 当前代码事实[ \t]*\r?\n"
        r"(?:[ \t]*\r?\n)*"
        r"(?P<facts>## [\s\S]+)",
        body,
    )
    if not body_match:
        errors.append(f"Instantiated memory body structure is invalid: {rel(path, root)}")
    current_facts = (
        body_match.group("facts").strip()
        if body_match
        else body
    )
    first_card = re.search(r"(?m)^##\s+", current_facts)
    if first_card and current_facts[: first_card.start()].strip():
        errors.append(f"Unexpected content before first code fact: {rel(path, root)}")
    if headings(body, 3):
        errors.append(f"Nested sections are forbidden in code-memory file: {rel(path, root)}")
    cards = heading_blocks(current_facts, 2)
    if not cards:
        errors.append(f"Empty code-memory file must not exist: {rel(path, root)}")
    seen_topics: set[str] = set()
    for topic, block in cards:
        if topic in seen_topics:
            errors.append(f"Duplicate fact topic '{topic}': {rel(path, root)}")
        seen_topics.add(topic)
        if FORMAL_FACT_KEY_PATTERN.fullmatch(topic):
            errors.append(f"Formal fact key is forbidden as topic '{topic}': {rel(path, root)}")
        if PROCESS_TOPIC_PATTERN.search(topic):
            errors.append(f"Process/change topic is forbidden '{topic}': {rel(path, root)}")
        if len(topic) > 48 or "`" in topic or "/" in topic or "\\" in topic:
            errors.append(f"Fact topic must be concise human-readable semantics '{topic}': {rel(path, root)}")
        values = validate_field_block(
            path,
            block,
            MEMORY_FIELDS,
            root,
            errors,
            f"code fact topic '{topic}'",
            allow_placeholders=False,
        )
        for field in MEMORY_FIELDS:
            value = values.get(field, "")
            if field == "影响范围" and value == "无":
                continue
            if len(value) < 12:
                errors.append(f"Code fact topic '{topic}' field '{field}' is too terse: {rel(path, root)}")
        current_fact = values.get("当前事实", "")
        if len(current_fact) > 600:
            errors.append(f"Code fact topic '{topic}' is not concise: {rel(path, root)}")
        if SESSION_SUMMARY_PATTERN.match(current_fact):
            errors.append(f"Code fact topic '{topic}' contains a session summary: {rel(path, root)}")
        if PROCESS_FACT_PATTERN.search(current_fact):
            errors.append(f"Code fact topic '{topic}' contains migration/refactor history: {rel(path, root)}")
        anchors = re.findall(r"`([^`]+)`", values.get("代码定位", ""))
        if len(anchors) > 3:
            errors.append(f"Code fact topic '{topic}' has more than three code anchors: {rel(path, root)}")
        resolved_anchors = [
            validate_source_anchor(root, path, topic, anchor, errors) for anchor in anchors
        ]
        if not any(resolved_anchors):
            errors.append(f"Code fact topic '{topic}' needs a repository source anchor: {rel(path, root)}")
        validation_entry = values.get("验证入口", "")
        if SESSION_SUMMARY_PATTERN.match(validation_entry):
            errors.append(f"Code fact topic '{topic}' contains transient validation evidence: {rel(path, root)}")


def validate_readme(root: Path, errors: list[str]) -> None:
    path = root / "README.md"
    content = read_text(path, root, errors)
    require_terms(
        path,
        content,
        (
            "六个 Skill",
            "`router`",
            "`design`",
            "`architecture`",
            "`backend`",
            "`frontend`",
            "`verification`",
            "9efef58ddb3f3a4bebcf856f6c2eef7ca7a53194",
            "目录—角色职责—核心能力—常见误判",
            "当前代码事实",
            "router` 不拥有记忆",
            "格式版本号",
            "人类可读主题",
            "当前事实、代码定位、影响范围和验证入口",
            "重构、迁移、改名和实现变更",
            "memory: 0 facts changed",
            "技能自有",
            "`references/memory.md`",
        ),
        root,
        errors,
        "README",
    )


def validate_legacy_surfaces(root: Path, errors: list[str]) -> None:
    surfaces = (
        root / "README.md",
        root / "skills",
        root / "references",
        root / "templates",
        root / "docs" / "product-studio",
        root / ".codex-plugin",
        root / ".claude-plugin",
        root / ".agents",
    )
    for surface in surfaces:
        paths = [surface] if surface.is_file() else surface.rglob("*") if surface.exists() else []
        for path in paths:
            if not path.is_file():
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for pattern, label in (
                (LEGACY_INVOCATION, "legacy skill invocation"),
                (LEGACY_ROLE_PATH, "legacy role path"),
                (LEGACY_MEMORY_PATH, "legacy memory path"),
            ):
                match = pattern.search(content)
                if match:
                    errors.append(f"{label} '{match.group(0)}' remains: {rel(path, root)}")


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    skills_dir = root / "skills"
    docs_dir = root / "docs" / "product-studio"
    actual_skills = {path.name for path in skills_dir.iterdir() if path.is_dir()}
    if actual_skills != SKILLS:
        errors.append(f"Skill directories must be exactly {list(SKILL_ORDER)}")
    legacy_root_resources = sorted(
        str(path.relative_to(root)).replace("\\", "/")
        for directory in (root / "references", root / "templates")
        if directory.exists()
        for path in directory.rglob("*")
        if path.is_file()
    )
    if legacy_root_resources:
        errors.append(
            "Root-level memory resources must not exist: "
            f"got={legacy_root_resources}"
        )
    validate_manifests(root, errors)
    for skill in SKILL_ORDER:
        validate_skill(root, skill, errors)
    allowed_memories = {f"{owner}.md" for owner in MEMORY_OWNERS}
    actual_memory_paths = (
        {
            str(path.relative_to(docs_dir)).replace("\\", "/")
            for path in docs_dir.rglob("*")
            if path.is_file()
        }
        if docs_dir.exists()
        else set()
    )
    unknown_memories = actual_memory_paths - allowed_memories
    if unknown_memories:
        errors.append(f"Unknown project memory files: {sorted(unknown_memories)}")
    actual_memories = actual_memory_paths & allowed_memories
    for filename in sorted(actual_memories):
        owner = filename.removesuffix(".md")
        validate_memory_file(root, owner, docs_dir / filename, errors)
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
    fence_probe = (
        "## A\r\n"
        "````markdown\r\n"
        "````python\r\n"
        "## 隐藏\r\n"
        "````\r\n"
        "## B\r\n"
    )
    if headings(fence_probe, 2) != ["A", "B"] or len(mask_fenced_code(fence_probe)) != len(
        fence_probe
    ):
        failures.append("fenced-heading parser exposes content behind a false closing fence")
    with tempfile.TemporaryDirectory(prefix="product-studio-validator-") as temp_dir:
        baseline = Path(temp_dir) / "baseline"
        shutil.copytree(ROOT, baseline, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
        baseline_errors = validate(baseline)
        if baseline_errors:
            return ["negative-test baseline differs from the real tree: " + baseline_errors[0]]

        memoryless_baseline = Path(temp_dir) / "memoryless-baseline"
        shutil.copytree(baseline, memoryless_baseline)
        memory_dir = memoryless_baseline / "docs" / "product-studio"
        if memory_dir.exists():
            for memory_path in memory_dir.glob("*.md"):
                memory_path.unlink()
        memoryless_errors = validate(memoryless_baseline)
        if memoryless_errors:
            return [
                "optional-memory baseline must remain valid: " + memoryless_errors[0]
            ]

        valid_rule_variants = Path(temp_dir) / "valid-rule-variants"
        shutil.copytree(memoryless_baseline, valid_rule_variants)
        backend_skill = valid_rule_variants / "skills" / "backend" / "SKILL.md"
        backend_skill.write_text(
            backend_skill.read_text(encoding="utf-8").rstrip()
            + "\n\n没有最终差异时，不得更新任何事实或记忆。\n",
            encoding="utf-8",
        )
        verification_skill = valid_rule_variants / "skills" / "verification" / "SKILL.md"
        verification_skill.write_text(
            verification_skill.read_text(encoding="utf-8").rstrip()
            + "\n\n本技能不允许在生产环境执行外部写入。\n",
            encoding="utf-8",
        )
        valid_rule_errors = validate(valid_rule_variants)
        if valid_rule_errors:
            failures.append(
                "legitimate memory or external-write prohibition was rejected: "
                + valid_rule_errors[0]
            )

        def ensure_design_memory(root: Path) -> Path:
            path = root / "docs" / "product-studio" / "design.md"
            if path.is_file():
                return path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                """# design 当前代码事实

## 插件职责边界

- **当前事实**：插件文档定义六个技能的固定拓扑，并由静态校验守住该边界。
- **代码定位**：`README.md#六个 Skill`
- **影响范围**：插件清单、技能路由和项目静态校验均依赖这项职责边界。
- **验证入口**：运行项目静态校验并断言六个技能目录与插件清单保持一致。
""",
                encoding="utf-8",
            )
            return path

        def run_case(name: str, mutate: object, expected_error: str) -> None:
            case_root = Path(temp_dir) / name
            shutil.copytree(memoryless_baseline, case_root)
            mutate(case_root)  # type: ignore[operator]
            diagnostics = validate(case_root)
            if not any(expected_error in diagnostic for diagnostic in diagnostics):
                observed = diagnostics[0] if diagnostics else "no validation error"
                failures.append(
                    f"negative case '{name}' missed expected diagnostic "
                    f"'{expected_error}'; observed: {observed}"
                )

        def add_seventh_skill(root: Path) -> None:
            shutil.copytree(root / "skills" / "backend", root / "skills" / "release")

        def add_router_memory(root: Path) -> None:
            shutil.copy2(
                root / "skills" / "backend" / "references" / "memory.md",
                root / "skills" / "router" / "references" / "memory.md",
            )

        def add_nested_router_reference(root: Path) -> None:
            path = root / "skills" / "router" / "references" / "private" / "memory.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# hidden router memory\n", encoding="utf-8")

        def add_nested_router_project_memory(root: Path) -> None:
            path = root / "docs" / "product-studio" / "router" / "memory.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# hidden router fact store\n", encoding="utf-8")

        def remove_architecture_reference(root: Path) -> None:
            (root / "skills" / "architecture" / "references" / "principles.md").unlink()

        def remove_design_reference(root: Path) -> None:
            (root / "skills" / "design" / "references" / "principles.md").unlink()

        def claim_backend_architecture_ownership(root: Path) -> None:
            path = root / "skills" / "backend" / "SKILL.md"
            path.write_text(
                path.read_text(encoding="utf-8").rstrip()
                + "\n\n负责系统架构并裁定系统边界。\n",
                encoding="utf-8",
            )

        def restore_design_system_mode(root: Path) -> None:
            path = root / "skills" / "design" / "SKILL.md"
            path.write_text(
                path.read_text(encoding="utf-8").rstrip()
                + "\n\n## 系统模式\n\n负责系统架构并裁定系统边界。\n",
                encoding="utf-8",
            )

        def add_unexpected_reference(root: Path) -> None:
            (root / "skills" / "router" / "references" / "extra.md").write_text("# extra\n", encoding="utf-8")

        def modify_reference(root: Path) -> None:
            path = root / "skills" / "backend" / "references" / "principles.md"
            path.write_text(path.read_text(encoding="utf-8").replace("领域建模", "领域模型", 1), encoding="utf-8")

        def corrupt_memory_field(root: Path) -> None:
            path = ensure_design_memory(root)
            path.write_text(path.read_text(encoding="utf-8").replace("**影响范围**", "**依赖范围**", 1), encoding="utf-8")

        def duplicate_memory_topic(root: Path) -> None:
            path = ensure_design_memory(root)
            content = path.read_text(encoding="utf-8")
            card = re.search(r"(?ms)^## 插件职责边界\s*$.*?(?=^## |\Z)", content)
            if card:
                path.write_text(content.rstrip() + "\n\n" + card.group(0).rstrip() + "\n", encoding="utf-8")

        def add_formal_fact_key(root: Path) -> None:
            path = ensure_design_memory(root)
            path.write_text(
                re.sub(
                    r"(?m)^## 插件职责边界$",
                    "## design:migration:memory-template",
                    path.read_text(encoding="utf-8"),
                    count=1,
                ),
                encoding="utf-8",
            )

        def escaping_anchor(root: Path) -> None:
            path = ensure_design_memory(root)
            path.write_text(
                re.sub(
                    r"(?m)^(- \*\*代码定位\*\*：)`[^`]+`",
                    r"\1`../outside.md#scope`",
                    path.read_text(encoding="utf-8"),
                    count=1,
                ),
                encoding="utf-8",
            )

        def absolute_anchor(root: Path) -> None:
            path = ensure_design_memory(root)
            absolute = root / "README.md"
            path.write_text(
                re.sub(
                    r"(?m)^(- \*\*代码定位\*\*：)`[^`]+`",
                    lambda match: f"{match.group(1)}`{absolute}#六个 Skill`",
                    path.read_text(encoding="utf-8"),
                    count=1,
                ),
                encoding="utf-8",
            )

        def invalid_memory_skeleton(root: Path) -> None:
            path = root / "skills" / "backend" / "references" / "memory.md"
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "## <稳定事实主题>", "## backend:migration:orders", 1
                ),
                encoding="utf-8",
            )

        def remove_backend_memory_reference(root: Path) -> None:
            (root / "skills" / "backend" / "references" / "memory.md").unlink()

        def add_session_summary(root: Path) -> None:
            path = ensure_design_memory(root)
            content = path.read_text(encoding="utf-8")
            path.write_text(
                re.sub(
                    r"(?m)^- \*\*当前事实\*\*：.*$",
                    "- **当前事实**：本轮完成了技能拓扑与记忆模板重构，并修改了相关文件。",
                    content,
                    count=1,
                ),
                encoding="utf-8",
            )

        def add_extra_memory_content(root: Path) -> None:
            path = ensure_design_memory(root)
            path.write_text(
                path.read_text(encoding="utf-8").rstrip()
                + "\n\n- 附记：此项不属于当前代码事实格式。\n",
                encoding="utf-8",
            )

        def fence_memory_card(root: Path) -> None:
            path = ensure_design_memory(root)
            content = path.read_text(encoding="utf-8")
            content = content.replace(
                "## 插件职责边界",
                "```markdown\n## 插件职责边界",
                1,
            )
            path.write_text(content, encoding="utf-8")

        def add_memory_preface(root: Path) -> None:
            path = ensure_design_memory(root)
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "# design 当前代码事实\n\n",
                    "# design 当前代码事实\n\n此段游离正文不属于任何事实主题。\n\n",
                    1,
                ),
                encoding="utf-8",
            )

        def add_nested_memory_section(root: Path) -> None:
            path = ensure_design_memory(root)
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "- **验证入口**：运行项目静态校验并断言六个技能目录与插件清单保持一致。",
                    "- **验证入口**：运行项目静态校验并断言六个技能目录与插件清单保持一致。\n\n### 过程附记",
                    1,
                ),
                encoding="utf-8",
            )

        def add_memory_trailing_section(root: Path) -> None:
            path = ensure_design_memory(root)
            path.write_text(
                path.read_text(encoding="utf-8").rstrip()
                + "\n\n# 过程附记\n\n本段不属于当前代码事实。\n",
                encoding="utf-8",
            )

        def add_process_topic(root: Path) -> None:
            path = ensure_design_memory(root)
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "## 插件职责边界", "## 记忆模板迁移阶段", 1
                ),
                encoding="utf-8",
            )

        def add_legacy_frontmatter(root: Path) -> None:
            path = ensure_design_memory(root)
            path.write_text(
                "---\nmemory: design\nproject_root: \".\"\n---\n\n"
                + path.read_text(encoding="utf-8"),
                encoding="utf-8",
            )

        def add_migration_history(root: Path) -> None:
            path = ensure_design_memory(root)
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "插件文档定义六个技能的固定拓扑",
                    "本轮完成了从共享模板迁移到技能自有记忆卷",
                    1,
                ),
                encoding="utf-8",
            )

        def add_secret_value(root: Path) -> None:
            path = ensure_design_memory(root)
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "插件文档定义六个技能的固定拓扑",
                    "插件文档定义六个技能的固定拓扑，password=synthetic-secret-123",
                    1,
                ),
                encoding="utf-8",
            )

        def empty_backend_memory_section(root: Path) -> None:
            path = root / "skills" / "backend" / "references" / "memory.md"
            path.write_text(
                re.sub(
                    r"(?ms)(^## 收录门槛\s*$).*?(?=^## )",
                    r"\1\n\n",
                    path.read_text(encoding="utf-8"),
                    count=1,
                ),
                encoding="utf-8",
            )

        def add_legacy_root_contract(root: Path) -> None:
            path = root / "references" / "project-memory.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# legacy shared memory contract\n", encoding="utf-8")

        def add_legacy_root_template(root: Path) -> None:
            path = root / "templates" / "backend.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# legacy backend memory template\n", encoding="utf-8")

        def cross_owner_memory_link(root: Path) -> None:
            path = root / "skills" / "backend" / "SKILL.md"
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "[backend 记忆规则与实例格式](references/memory.md)",
                    "[design 记忆规则与实例格式](../design/references/memory.md)",
                    1,
                ),
                encoding="utf-8",
            )

        def remove_final_state_rule(root: Path) -> None:
            path = root / "skills" / "backend" / "references" / "memory.md"
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "不得成为主题或事实正文",
                    "可以作为主题或事实正文",
                    1,
                ),
                encoding="utf-8",
            )

        def contradict_memory_sync(root: Path) -> None:
            path = root / "skills" / "backend" / "SKILL.md"
            path.write_text(
                path.read_text(encoding="utf-8").rstrip()
                + "\n\n不得同步任何 backend 事实。\n",
                encoding="utf-8",
            )

        def permit_external_writes(root: Path) -> None:
            path = root / "skills" / "verification" / "SKILL.md"
            path.write_text(
                path.read_text(encoding="utf-8").rstrip()
                + "\n\n前述边界作废，可在生产环境执行外部写入。\n",
                encoding="utf-8",
            )

        def legacy_invocation(root: Path) -> None:
            path = root / "README.md"
            path.write_text(path.read_text(encoding="utf-8") + "\n$" + "delivery\n", encoding="utf-8")

        def overroute_verification(root: Path) -> None:
            path = root / "skills" / "router" / "SKILL.md"
            path.write_text(path.read_text(encoding="utf-8").replace("不计作跨领域触发条件", "计作跨领域触发条件", 1), encoding="utf-8")

        def restore_router_terminal_closure(root: Path) -> None:
            path = root / "skills" / "router" / "SKILL.md"
            path.write_text(
                path.read_text(encoding="utf-8").rstrip()
                + "\n\n## 终态收口\n\n由 router 判定完成、部分完成、阻塞或失败。\n",
                encoding="utf-8",
            )

        def remove_api_milestone(root: Path) -> None:
            path = root / "skills" / "router" / "SKILL.md"
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "具体 API 契约里程碑", "接口约定"
                ),
                encoding="utf-8",
            )

        def remove_architecture_milestone(root: Path) -> None:
            path = root / "skills" / "router" / "SKILL.md"
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "架构契约里程碑", "架构约定", 1
                ),
                encoding="utf-8",
            )

        cases = (
            ("seventh-skill", add_seventh_skill, "Skill directories must be exactly"),
            ("router-memory", add_router_memory, "Skill reference set differs for router"),
            ("nested-router-reference", add_nested_router_reference, "Skill reference set differs for router"),
            ("nested-router-project-memory", add_nested_router_project_memory, "Unknown project memory files"),
            ("missing-architecture-reference", remove_architecture_reference, "Skill reference set differs for architecture"),
            ("missing-design-reference", remove_design_reference, "Skill reference set differs for design"),
            ("backend-architecture-overreach", claim_backend_architecture_ownership, "Backend must not own system architecture"),
            ("design-system-mode-overreach", restore_design_system_mode, "Design must not own system architecture term"),
            ("unexpected-reference", add_unexpected_reference, "Skill reference set differs for router"),
            ("modified-reference-content", modify_reference, "Capability reference differs from the curated baseline"),
            ("invalid-memory-field", corrupt_memory_field, "fields must be exactly"),
            ("duplicate-memory-topic", duplicate_memory_topic, "Duplicate fact topic"),
            ("formal-fact-key", add_formal_fact_key, "Formal fact key is forbidden"),
            ("escaping-source-anchor", escaping_anchor, "Source anchor escapes project root"),
            ("absolute-source-anchor", absolute_anchor, "Source anchor must be repository-relative"),
            ("invalid-memory-format", invalid_memory_skeleton, "Memory format topic must be"),
            ("missing-owner-memory", remove_backend_memory_reference, "Skill reference set differs for backend"),
            ("session-summary-memory", add_session_summary, "contains a session summary"),
            ("extra-memory-content", add_extra_memory_content, "Unexpected content in code fact"),
            ("fenced-memory-card", fence_memory_card, "Code fence is forbidden"),
            ("prefaced-memory-card", add_memory_preface, "Unexpected content before first code fact"),
            ("nested-memory-section", add_nested_memory_section, "Nested sections are forbidden"),
            ("memory-trailing-section", add_memory_trailing_section, "Instantiated memory title is invalid"),
            ("legacy-memory-frontmatter", add_legacy_frontmatter, "Frontmatter is forbidden"),
            ("process-memory-topic", add_process_topic, "Process/change topic is forbidden"),
            ("migration-history-memory", add_migration_history, "contains a session summary"),
            ("secret-in-memory", add_secret_value, "Possible secret value"),
            ("empty-owner-memory-section", empty_backend_memory_section, "Empty backend memory section"),
            ("contradictory-memory-sync", contradict_memory_sync, "Contradictory memory sync rule"),
            ("external-write-overreach", permit_external_writes, "External write permission contradicts"),
            ("legacy-invocation", legacy_invocation, "legacy skill invocation"),
            ("overrouted-terminal-verification", overroute_verification, "Missing router term '不计作跨领域触发条件'"),
            ("router-terminal-closure", restore_router_terminal_closure, "Router must not own terminal closure"),
            ("missing-api-contract-milestone", remove_api_milestone, "Missing router term '具体 API 契约里程碑'"),
            ("missing-architecture-contract-milestone", remove_architecture_milestone, "Missing router term '架构契约里程碑'"),
            ("legacy-root-contract", add_legacy_root_contract, "Root-level memory resources must not exist"),
            ("legacy-root-template", add_legacy_root_template, "Root-level memory resources must not exist"),
            ("cross-owner-memory-link", cross_owner_memory_link, "Missing current-code-memory term '[backend 记忆规则与实例格式](references/memory.md)'"),
            ("missing-final-state-rule", remove_final_state_rule, "Missing backend memory 收录门槛 term '不得成为主题或事实正文'"),
        )
        declared = f"{len(cases)} 类退化"
        declared_paths = [ROOT / "scripts" / "README.md"]
        verification_memory = ROOT / "docs" / "product-studio" / "verification.md"
        if verification_memory.is_file():
            declared_paths.append(verification_memory)
        for path in declared_paths:
            if declared not in path.read_text(encoding="utf-8"):
                failures.append(f"negative self-test count is not synchronized: expected '{declared}'")
        for name, mutation, expected_error in cases:
            run_case(name, mutation, expected_error)
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
    print(
        f"[OK] Product Studio: {len(SKILL_ORDER)} skills, "
        f"{reference_count} curated capability references, "
        f"{len(MEMORY_OWNERS)} skill-owned memory references{suffix}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
