#!/usr/bin/env python3
"""Validate the shared Product Studio plugin without external dependencies."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
ROOT_REFERENCES = ROOT / "references"
ROOT_REFERENCE_LINK_PATTERN = re.compile(
    r"(?:^|[\s`(\"'=])(?P<link>(?:(?:\.\.[\\/])+|[\\/])references"
    r"(?:[\\/]|(?=$|[\s`)\]>'\"])))",
    re.IGNORECASE | re.MULTILINE,
)
README_ROOT_REFERENCE_LINK_PATTERN = re.compile(
    r"(?:^|[\s`(\"'=])(?P<link>references[\\/]"
    r"[^\s`)\]>'\"]+)",
    re.IGNORECASE | re.MULTILINE,
)
TEMPLATE_CAPABILITY_LINK_PATTERN = re.compile(
    r"\.\./skills/[a-z0-9]+/references/[A-Za-z0-9_.-]+\.md",
    re.IGNORECASE,
)
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
    "## 角色职责",
    "## 核心能力",
    "## 专业决策顺序",
    "## 能力组合",
    "## 完成判据",
    "## 交付证据",
    "## 常见误判",
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
ROLE_MEMORY_TERM_GROUPS = (
    ("docs/product-studio/",),
    ("事实卡",),
    ("当前仍成立", "已经成立"),
    ("本角色",),
    ("角色专属细节",),
    ("精确定位",),
    ("成立证据",),
    ("关联事实",),
    ("下游约束",),
    ("外部参考",),
    ("不会自动成为当前项目事实",),
    ("当前用户确认", "仓库实现", "本项目验证"),
    ("只读",),
    ("过程阶段",),
    ("任务终态", "可复核终态"),
    ("适用验证完成后", "全部适用验证结束后"),
    ("无需再次单独询问",),
    ("事实增量",),
    ("稳定 ID",),
    ("状态与置信度",),
    ("取代关系",),
    ("重验条件", "失效条件"),
    ("不得全量覆盖", "不全量覆盖", "原样边界"),
    ("未受影响", "前后差分"),
    ("无事实增量",),
    ("schema 2",),
    ("模板仅用于首次创建",),
    ("既有 schema 2 新增事实时",),
    ("不再读取或套用模板",),
    ("本角色只拥有",),
    ("只增量合并本角色", "各拥有者只增量合并自己"),
)
ROLE_MEMORY_FORBIDDEN_TERMS = (
    "过程阶段允许写",
    "过程阶段可以写",
    "过程阶段可写",
    "所有角色共同改写",
    "所有角色都可改写",
    "允许" + "全量覆盖",
    "可以" + "全量覆盖",
)
ROLE_MEMORY_FORBIDDEN_PATTERNS = (
    re.compile(
        r"过程阶段.{0,16}(?:允许|可以|可|能够|应当|应该|须|必须)"
        r".{0,12}(?:写入|更新|创建|改写|编辑)"
    ),
    re.compile(
        r"(?:所有|全部|各)(?:受影响)?角色.{0,16}"
        r"(?:共同|均可|都可|可以共同|可共同).{0,16}"
        r"(?:改写|编辑|更新|写入|维护)"
    ),
)
DELIVERY_MEMORY_ROUTING_TERM_GROUPS = (
    ("跨角色总路由",),
    ("受影响角色",),
    ("产品／架构", "产品/架构"),
    ("前端",),
    ("后端",),
    ("`verification`",),
    ("`release`",),
    ("`delivery`",),
    ("各拥有者",),
    ("只增量合并自己",),
    ("`delivery` 不代写专项事实",),
    ("任一写入失败",),
    ("不反向改变", "不倒改"),
    ("不得制造悬空引用",),
)
DELIVERY_MEMORY_ROUTE_SEQUENCE = (
    "产品／架构",
    "前端",
    "后端",
    "`verification`",
    "`release`",
    "`delivery`",
)
DELIVERY_MEMORY_FORBIDDEN_TERMS = (
    "`delivery` 可代写专项事实",
    "由 `delivery` 代写专项事实",
    "`delivery` 代写专项事实",
)
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
    "## 能力目录",
    "## 核心能力",
    "## 能力组合",
    "## 完成判据",
)
LEGACY_CAPABILITY_REFERENCE_SECTIONS = (
    "## 角色职责",
    "## 专业决策顺序",
    "## 交付证据",
    "## 常见误判",
)
CAPABILITY_CARD_FIELDS = (
    "**启用**",
    "**输入**",
    "**执行**",
    "**裁决**",
    "**产出**",
    "**验证**",
    "**完成**",
    "**边界**",
)
TEMPLATE_SECTIONS = {
    f"{name}.md": ("## 事实家族", "## 现行事实")
    for name in CORE_SKILL_ORDER
}
SCHEMA_1_FRONTMATTER_FIELDS = (
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
SCHEMA_2_FRONTMATTER_FIELDS = (
    "schema",
    "memory",
    "scope",
    "project_root",
    "updated_at",
)
TEMPLATE_AI_TERM_GROUPS = (
    ("本模板仅用于首次创建",),
    ("角色能力", "能力手册"),
    ("一个独立语义一张卡",),
    ("从 `001` 递增", "从 001 递增"),
    ("只生成有证据", "仅生成有证据", "只保留有依据"),
    ("实例化时",),
    ("删除本说明",),
    ("既有 schema 1 或 schema 2",),
    ("不得读取或套用本模板", "不再读取或套用模板"),
)
FACT_CARD_FIELDS = (
    "事实类型",
    "已成立事实",
    "角色专属细节",
    "适用范围",
    "精确定位",
    "成立证据",
    "核验基线",
    "关联事实",
    "下游约束",
    "状态",
    "置信度",
    "取代关系",
    "失效条件",
)
FACT_ID_PREFIXES = {
    "delivery": ("DEL-",),
    "discovery": ("DISC-",),
    "architecture": ("ARCH-", "ADR-"),
    "frontend": ("FE-",),
    "backend": ("BE-",),
    "verification": ("VER-",),
    "release": ("RLS-",),
}
TEMPLATE_FACT_ID_FAMILIES = {
    "delivery": (
        "DEL-SCOPE-*",
        "DEL-CAP-*",
        "DEL-REL-*",
        "DEL-INTEGRATION-*",
        "DEL-DEP-*",
        "DEL-RISK-*",
        "DEL-OUTCOME-*",
    ),
    "discovery": (
        "DISC-USER-*",
        "DISC-OUTCOME-*",
        "DISC-RULE-*",
        "DISC-JOURNEY-*",
        "DISC-SCOPE-*",
        "DISC-AC-*",
        "DISC-DEC-*",
        "DISC-LIMIT-*",
    ),
    "architecture": (
        "ARCH-TOPO-*",
        "ARCH-BOUND-*",
        "ARCH-INV-*",
        "ARCH-FLOW-*",
        "ARCH-ADR-*",
        "ARCH-REL-*",
        "ARCH-EVO-*",
        "ARCH-LIMIT-*",
    ),
    "frontend": (
        "FE-SURFACE-*",
        "FE-FLOW-*",
        "FE-STATE-*",
        "FE-IMPL-*",
        "FE-A11Y-*",
        "FE-RESP-*",
        "FE-RENDER-*",
        "FE-LIMIT-*",
    ),
    "backend": (
        "BE-DOMAIN-*",
        "BE-SCHEMA-*",
        "BE-API-*",
        "BE-AUTH-*",
        "BE-CONSIST-*",
        "BE-INT-*",
        "BE-OBS-*",
        "BE-COMPAT-*",
        "BE-LIMIT-*",
    ),
    "verification": (
        "VER-BASE-*",
        "VER-AC-*",
        "VER-JOURNEY-*",
        "VER-REC-*",
        "VER-NFR-*",
        "VER-DEFECT-*",
        "VER-CONCLUSION-*",
    ),
    "release": (
        "RLS-ENV-*",
        "RLS-ART-*",
        "RLS-AUTH-*",
        "RLS-GATE-*",
        "RLS-DEPLOY-*",
        "RLS-SIGNAL-*",
        "RLS-ROLLBACK-*",
        "RLS-LIMIT-*",
    ),
}
TEMPLATE_FACT_SKELETON_PREFIXES = {
    "delivery": "DEL",
    "discovery": "DISC",
    "architecture": "ARCH",
    "frontend": "FE",
    "backend": "BE",
    "verification": "VER",
    "release": "RLS",
}
LEGACY_PROCESS_TEMPLATE_HEADINGS = (
    "## 恢复摘要",
    "## 依据账本",
    "## 动作队列",
    "## 当前验证",
    "## 交接与失效",
    "## 角色记忆收口",
    "## 执行记录",
)
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
LEGACY_MEMORY_LIFECYCLE_TERMS = (
    "氛围编程" + "完成前",
    "动态" + "收口",
    "动态" + "更新其记忆",
    "动态" + "更新自己拥有的记忆",
)
FULL_REPLACEMENT_MEMORY_TERMS = (
    "原地" + "覆盖上一快照",
    "一次性" + "原地覆盖",
    "原地" + "覆盖本角色文件",
    "原地" + "覆盖各自最后事实",
    "保持" + "旧快照",
    "当前有效" + "编排快照",
    "上一已闭合任务的" + "最后事实",
    "从模板" + "重建已有记忆",
    "允许" + "全量覆盖",
    "可以" + "全量覆盖",
    "允许" + "整文件重建",
    "允许套用本模板" + "重建",
)
TEMPLATE_REUSE_MEMORY_TERMS = (
    "模板用于首次创建，也供" + "已有",
    "模板既供首次创建，也供" + "已有",
    "模板用于首次创建及" + "已有",
    "定义新记忆首次创建及" + "已有",
    "新增事实卡时只读匹配 ID 家族的字段" + "提示",
    "新增事实时只读取同名" + "模板",
    "新增事实时，只读取同名" + "模板",
    "已有 schema 2 记忆需要新增事实卡时，也应只读同名" + "模板",
    "已有 schema 2 新增事实时，只读取同名" + "模板",
    "既有 schema 2 新增事实时，只读取同名" + "模板",
    "只读匹配 ID 家族的" + "模板卡",
)
SCHEMA_1_FINAL_STATUSES = {
    "done",
    "failed",
    "blocked",
    "not_applicable",
}
VERIFICATION_CONCLUSIONS = {
    "通过",
    "失败",
    "阻塞",
    "不适用",
}


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


def markdown_heading_block(content: str, heading: str) -> str | None:
    """Return one Markdown heading block until the next same-or-higher heading."""
    heading_match = re.match(r"^(#{1,6})\s+", heading)
    if heading_match is None:
        return None
    heading_level = len(heading_match.group(1))
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
        next_heading = re.match(r"^(#{1,6})\s+", line)
        if next_heading and len(next_heading.group(1)) <= heading_level:
            return "\n".join(lines[start:index]).strip()
    if start is None:
        return None
    return "\n".join(lines[start:]).strip()


def markdown_headings(content: str, level: int) -> list[str]:
    """Return headings at one exact level, excluding fenced code blocks."""
    prefix = "#" * level
    pattern = re.compile(rf"^{re.escape(prefix)}(?!#)\s+.+")
    headings: list[str] = []
    in_fence = False
    for line in content.splitlines():
        if re.match(r"^\s*(?:```|~~~)", line):
            in_fence = not in_fence
            continue
        if not in_fence and pattern.match(line):
            headings.append(line.strip())
    return headings


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


def require_unique_sections(
    path: Path,
    content: str,
    headings: tuple[str, ...],
    errors: list[str],
) -> None:
    actual_headings = markdown_headings(content, 2)
    for heading in headings:
        count = actual_headings.count(heading)
        if count != 1:
            errors.append(
                f"Required section must appear exactly once ('{heading}', got {count}): "
                f"{path.relative_to(ROOT)}"
            )


def require_ordered_terms(
    path: Path,
    content: str,
    terms: tuple[str, ...],
    errors: list[str],
    context: str,
) -> None:
    cursor = 0
    for term in terms:
        position = content.find(term, cursor)
        if position < 0:
            errors.append(
                f"Missing or out-of-order {context} term '{term}': "
                f"{path.relative_to(ROOT)}"
            )
            return
        cursor = position + len(term)


def reject_terms(
    path: Path,
    content: str,
    terms: tuple[str, ...],
    errors: list[str],
    context: str,
) -> None:
    for term in terms:
        if term in content:
            errors.append(
                f"Forbidden {context} contract '{term}': {path.relative_to(ROOT)}"
            )


def reject_patterns(
    path: Path,
    content: str,
    patterns: tuple[re.Pattern[str], ...],
    errors: list[str],
    context: str,
) -> None:
    for pattern in patterns:
        match = pattern.search(content)
        if match:
            errors.append(
                f"Forbidden {context} contract '{match.group(0)}': "
                f"{path.relative_to(ROOT)}"
            )


def require_single_line_containing(
    path: Path,
    content: str,
    marker: str,
    errors: list[str],
) -> str | None:
    matches = [line.strip() for line in content.splitlines() if marker in line]
    if len(matches) != 1:
        errors.append(
            f"Expected exactly one line containing '{marker}', got {len(matches)}: "
            f"{path.relative_to(ROOT)}"
        )
        return None
    return matches[0]


def reject_removed_root_reference_links(
    path: Path,
    content: str,
    errors: list[str],
) -> None:
    matches = {
        match.group("link")
        for match in ROOT_REFERENCE_LINK_PATTERN.finditer(content)
    }
    normalized_content = content.replace("\\", "/").lower()
    normalized_root_references = str(ROOT_REFERENCES.resolve()).replace(
        "\\", "/"
    ).lower()
    if normalized_root_references in normalized_content:
        matches.add(str(ROOT_REFERENCES.resolve()))
    if path == ROOT / "README.md":
        matches.update(
            match.group("link")
            for match in README_ROOT_REFERENCE_LINK_PATTERN.finditer(content)
        )
    for match in sorted(matches, key=str.lower):
        errors.append(
            f"Root-level reference link '{match}' is not allowed: "
            f"{path.relative_to(ROOT)}"
        )


def validate_template_capability_link(
    path: Path,
    content: str,
    owner: str,
    errors: list[str],
) -> None:
    expected = f"../skills/{owner}/{CAPABILITY_REFERENCES[owner][0]}"
    actual = TEMPLATE_CAPABILITY_LINK_PATTERN.findall(content)
    if actual != [expected]:
        errors.append(
            f"Template must load exactly its owning role capability reference: "
            f"{path.relative_to(ROOT)} expected={expected}, got={actual}"
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
    template: bool,
) -> dict[str, str]:
    fields = parse_frontmatter(path, errors)
    schema = fields.get("schema")
    if schema not in {"1", "2"}:
        errors.append(f"Memory schema must be 1 or 2: {path.relative_to(ROOT)}")
        return fields
    if template and schema != "2":
        errors.append(f"Memory template schema must be 2: {path.relative_to(ROOT)}")

    expected_fields = (
        SCHEMA_1_FRONTMATTER_FIELDS if schema == "1" else SCHEMA_2_FRONTMATTER_FIELDS
    )
    for field in expected_fields:
        if field not in fields:
            errors.append(
                f"Missing memory frontmatter field '{field}': {path.relative_to(ROOT)}"
            )
    if schema == "2" and set(fields) != set(expected_fields):
        errors.append(
            f"Schema 2 memory frontmatter must contain only {expected_fields}: "
            f"{path.relative_to(ROOT)} has {tuple(fields)}"
        )
    if fields.get("memory") != expected_memory:
        errors.append(
            f"Memory name must match skill '{expected_memory}': {path.relative_to(ROOT)}"
        )
    if fields.get("scope") != "current-project":
        errors.append(f"Memory scope must be current-project: {path.relative_to(ROOT)}")

    if template:
        for field in ("project_root", "updated_at"):
            if fields.get(field):
                errors.append(
                    f"Reusable memory template field '{field}' must be empty: "
                    f"{path.relative_to(ROOT)}"
                )

    if not template:
        required_values = (
            ("project_root", "updated_at", "verified_at", "verified_revision")
            if schema == "1"
            else ("project_root", "updated_at")
        )
        for field in required_values:
            if not fields.get(field):
                errors.append(
                    f"Empty current memory field '{field}': {path.relative_to(ROOT)}"
                )
        updated_at = fields.get("updated_at", "")
        if updated_at and not is_rfc3339_with_offset(updated_at):
            errors.append(
                f"Current memory updated_at must be RFC 3339 with a timezone "
                f"offset: {path.relative_to(ROOT)}"
            )
        if schema == "1" and fields.get("confidence") not in {"high", "medium", "low"}:
            errors.append(
                f"Invalid current memory confidence: {path.relative_to(ROOT)}"
            )
        if schema == "1" and fields.get("status") not in SCHEMA_1_FINAL_STATUSES:
            errors.append(
                f"Schema 1 memory status must be terminal, got "
                f"'{fields.get('status', '')}': {path.relative_to(ROOT)}"
            )
    return fields


FACT_HEADING_PATTERN = re.compile(
    r"^###\s+([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d{3})\s+[—｜]\s+(.+)$"
)
RFC3339_WITH_OFFSET_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)
TERMINAL_RESULT_PATTERN = re.compile(
    r"^(?:(?:当前|本次)?[^；。]{0,24}?(?:结论|结果)(?:为|是|：)\s*)?"
    r"(通过|失败|阻塞|不适用)(?=[：；。，,\s]|$)"
)
UNCERTAIN_RESULT_PATTERN = re.compile(
    r"(?:尚未|未能|无法|不能)(?:确定|确认|判断)|待定|"
    r"(?:仍待|尚待|有待|待后续|需后续)[^；。]{0,12}"
    r"(?:确定|确认|判断|验证|核验|取证)"
)


def is_unresolved_placeholder(value: str) -> bool:
    return re.fullmatch(r"<[^<>\r\n]+>", value.strip()) is not None


def is_rfc3339_with_offset(value: str) -> bool:
    if RFC3339_WITH_OFFSET_PATTERN.fullmatch(value) is None:
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def validate_fact_cards(
    path: Path,
    content: str,
    owner: str,
    errors: list[str],
    *,
    template: bool,
) -> None:
    headings = markdown_headings(content, 3)
    cards: list[tuple[str, str, str]] = []
    if template:
        expected_heading = (
            f"### {TEMPLATE_FACT_SKELETON_PREFIXES[owner]}-<FAMILY>-001 "
            f"— <可独立理解的事实标题>"
        )
        if headings != [expected_heading]:
            errors.append(
                f"Fact template must contain exactly one generic fact-card skeleton "
                f"'{expected_heading}': {path.relative_to(ROOT)} has {headings}"
            )
            return
        cards.append(
            (
                f"{TEMPLATE_FACT_SKELETON_PREFIXES[owner]}-<FAMILY>-001",
                expected_heading,
                markdown_heading_block(content, expected_heading) or "",
            )
        )
    else:
        for heading in headings:
            match = FACT_HEADING_PATTERN.match(heading)
            if match is None:
                errors.append(
                    f"Fact-card heading must contain a stable ID and readable title: "
                    f"{path.relative_to(ROOT)} has '{heading}'"
                )
                continue
            fact_id = match.group(1)
            if is_unresolved_placeholder(match.group(2)):
                errors.append(
                    f"Unresolved fact title in '{heading}': {path.relative_to(ROOT)}"
                )
            block = markdown_heading_block(content, heading)
            cards.append((fact_id, heading, block or ""))

    if not cards:
        errors.append(f"No fact cards found: {path.relative_to(ROOT)}")
        return

    ids = [fact_id for fact_id, _, _ in cards]
    duplicate_ids = sorted({fact_id for fact_id in ids if ids.count(fact_id) > 1})
    if duplicate_ids:
        errors.append(
            f"Duplicate fact IDs {duplicate_ids}: {path.relative_to(ROOT)}"
        )

    allowed_prefixes = FACT_ID_PREFIXES[owner]
    allowed_family_prefixes = tuple(
        family.removesuffix("*") for family in TEMPLATE_FACT_ID_FAMILIES[owner]
    )
    for fact_id, heading, block in cards:
        if not fact_id.startswith(allowed_prefixes):
            errors.append(
                f"Fact ID '{fact_id}' does not belong to {owner}: "
                f"{path.relative_to(ROOT)}"
            )
        if not template and not fact_id.startswith(allowed_family_prefixes):
            errors.append(
                f"Fact ID '{fact_id}' does not belong to a declared {owner} fact "
                f"family: {path.relative_to(ROOT)}"
            )
        actual_fields = re.findall(
            r"(?m)^-\s+\*\*([^*\r\n]+)\*\*：\s*.*$",
            block,
        )
        if actual_fields != list(FACT_CARD_FIELDS):
            errors.append(
                f"Fact card '{heading}' must contain exactly the thirteen declared "
                f"fields in order: {path.relative_to(ROOT)} has {actual_fields}"
            )
        field_values: dict[str, str] = {}
        field_positions: list[int] = []
        for field in FACT_CARD_FIELDS:
            matches = list(
                re.finditer(
                    rf"(?m)^-\s+\*\*{re.escape(field)}\*\*：\s*(.*)$",
                    block,
                )
            )
            if len(matches) != 1:
                errors.append(
                    f"Fact card '{heading}' must contain exactly one '{field}' field: "
                    f"{path.relative_to(ROOT)}"
                )
                continue
            field_positions.append(matches[0].start())
            field_values[field] = matches[0].group(1).strip()
        if len(field_positions) == len(FACT_CARD_FIELDS) and (
            field_positions != sorted(field_positions)
        ):
            errors.append(
                f"Fact-card fields are out of order in '{heading}': "
                f"{path.relative_to(ROOT)}"
            )
        if not template:
            for field, value in field_values.items():
                if not value or is_unresolved_placeholder(value):
                    errors.append(
                        f"Unresolved fact value '{field}' in '{heading}': "
                        f"{path.relative_to(ROOT)}"
                    )
            if field_values.get("状态") not in {
                "current",
                "conditional",
                "stale",
                "superseded",
            }:
                errors.append(
                    f"Invalid fact status in '{heading}': {path.relative_to(ROOT)}"
                )
            if field_values.get("置信度") not in {"high", "medium", "low"}:
                errors.append(
                    f"Invalid fact confidence in '{heading}': {path.relative_to(ROOT)}"
                )


def validate_template_family_index(
    path: Path,
    content: str,
    owner: str,
    errors: list[str],
) -> None:
    section = markdown_section(content, "## 事实家族") or ""
    bullet_lines = [
        line.strip()
        for line in section.splitlines()
        if re.match(r"^\s*-\s+", line)
    ]
    family_pattern = re.compile(
        r"^-\s+`([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+-\*)`：\s*(\S.*)$"
    )
    matches: list[tuple[str, str]] = []
    for line in bullet_lines:
        match = family_pattern.fullmatch(line)
        if match is None:
            errors.append(
                f"Malformed template fact-family entry '{line}': "
                f"{path.relative_to(ROOT)}"
            )
            continue
        matches.append((match.group(1), match.group(2)))

    family_ids = [family_id for family_id, _ in matches]
    duplicate_ids = sorted(
        {family_id for family_id in family_ids if family_ids.count(family_id) > 1}
    )
    if duplicate_ids:
        errors.append(
            f"Duplicate template fact families {duplicate_ids}: "
            f"{path.relative_to(ROOT)}"
        )
    expected_families = list(TEMPLATE_FACT_ID_FAMILIES[owner])
    if family_ids != expected_families:
        errors.append(
            f"Template fact-family index differs from its skill contract: "
            f"{path.relative_to(ROOT)} expected={expected_families}, "
            f"got={family_ids}"
        )
    for family_id, description in matches:
        if "<" in description or ">" in description:
            errors.append(
                f"Template fact family '{family_id}' needs a concrete description: "
                f"{path.relative_to(ROOT)}"
            )


def validate_template_sections(
    path: Path,
    content: str,
    expected_sections: tuple[str, ...],
    errors: list[str],
) -> None:
    level_two_headings = markdown_headings(content, 2)
    if level_two_headings != list(expected_sections):
        errors.append(
            f"Fact template must contain exactly these level-two sections in order: "
            f"{path.relative_to(ROOT)} expected={list(expected_sections)}, "
            f"got={level_two_headings}"
        )
    for heading in LEGACY_PROCESS_TEMPLATE_HEADINGS:
        if heading in level_two_headings:
            errors.append(
                f"Process-log section '{heading}' remains in fact template: "
                f"{path.relative_to(ROOT)}"
            )


def validate_schema2_memory_sections(
    path: Path,
    content: str,
    errors: list[str],
) -> None:
    level_two_headings = markdown_headings(content, 2)
    if level_two_headings.count("## 现行事实") != 1:
        errors.append(
            f"Schema 2 memory must contain exactly one '## 现行事实' section: "
            f"{path.relative_to(ROOT)}"
        )
    forbidden_headings = ("## 事实家族",) + LEGACY_PROCESS_TEMPLATE_HEADINGS
    for heading in forbidden_headings:
        if heading in level_two_headings:
            errors.append(
                f"Instantiated schema 2 memory contains template or process section "
                f"'{heading}': {path.relative_to(ROOT)}"
            )


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


def validate_verification_conclusion(
    path: Path,
    content: str,
    errors: list[str],
) -> None:
    headings = [
        heading
        for heading in markdown_headings(content, 2)
        if heading == "## 最终结论"
    ]
    if len(headings) != 1:
        errors.append(
            f"Verification memory must contain exactly one current final-conclusion "
            f"section: {path.relative_to(ROOT)}"
        )
        return

    section = markdown_section(content, "## 最终结论") or ""
    matches = re.findall(
        r"(?m)^-\s*结论：\s*(通过|失败|阻塞|不适用)(?=[；。\s]|$)",
        section,
    )
    if len(matches) != 1 or matches[0] not in VERIFICATION_CONCLUSIONS:
        errors.append(
            f"Verification memory final-conclusion section must contain exactly one "
            f"terminal '- 结论：' line: {path.relative_to(ROOT)}"
        )


def validate_schema2_verification_conclusion(
    path: Path,
    content: str,
    errors: list[str],
) -> None:
    current_cards: list[tuple[str, str]] = []
    for heading in markdown_headings(content, 3):
        match = FACT_HEADING_PATTERN.match(heading)
        if match is None or not match.group(1).startswith("VER-CONCLUSION-"):
            continue
        block = markdown_heading_block(content, heading) or ""
        status_match = re.search(r"(?m)^-\s+\*\*状态\*\*：\s*(\S+)\s*$", block)
        fact_match = re.search(r"(?m)^-\s+\*\*已成立事实\*\*：\s*(.+)$", block)
        if status_match and status_match.group(1) == "current":
            current_cards.append(
                (match.group(1), fact_match.group(1).strip() if fact_match else "")
            )

    if len(current_cards) != 1:
        errors.append(
            f"Schema 2 verification memory must contain exactly one current "
            f"VER-CONCLUSION fact card: {path.relative_to(ROOT)}"
        )
        return

    fact_id, conclusion = current_cards[0]
    if (
        TERMINAL_RESULT_PATTERN.match(conclusion) is None
        or UNCERTAIN_RESULT_PATTERN.search(conclusion) is not None
    ):
        errors.append(
            f"Current verification conclusion '{fact_id}' must state one terminal "
            f"result ({', '.join(sorted(VERIFICATION_CONCLUSIONS))}): "
            f"{path.relative_to(ROOT)}"
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
        ("fact ID families", TEMPLATE_FACT_ID_FAMILIES),
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
    unexpected_memory_files = project_memory_files - expected_memory_files
    if unexpected_memory_files:
        errors.append(
            f"Project memory filenames must map to known skills: "
            f"extra={sorted(unexpected_memory_files)}"
        )
    required = [
        codex_manifest,
        claude_manifest,
        claude_marketplace_manifest,
        marketplace_manifest,
    ]
    required.extend(ROOT / "templates" / filename for filename in sorted(expected_memory_files))
    for path in required:
        if not path.is_file():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")
    if ROOT_REFERENCES.exists():
        for path in sorted(item for item in ROOT_REFERENCES.rglob("*") if item.is_file()):
            errors.append(
                f"Root-level references are not part of the skill architecture: "
                f"{path.relative_to(ROOT)}"
            )

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
        require_unique_sections(
            skill_file,
            content,
            COMMON_SKILL_SECTIONS,
            errors,
        )
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
                    "能力目录",
                    "适用的能力卡",
                    "完整读取",
                    "目录摘要不得代替能力卡正文",
                    "输入、执行、裁决、产出、验证、完成与边界",
                    "能力组合",
                    "完成判据",
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
                ROLE_MEMORY_TERM_GROUPS,
                errors,
                "role-memory section",
            )
            if memory_file:
                require_terms(
                    skill_file,
                    memory_section,
                    (
                        f"<当前项目根>/docs/product-studio/{memory_file}",
                        f"../../templates/{memory_file}",
                    ),
                    errors,
                )
            reject_terms(
                skill_file,
                memory_section,
                ROLE_MEMORY_FORBIDDEN_TERMS,
                errors,
                "role-memory",
            )
            reject_patterns(
                skill_file,
                memory_section,
                ROLE_MEMORY_FORBIDDEN_PATTERNS,
                errors,
                "role-memory",
            )
            declared_families = set(
                re.findall(
                    r"`([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+-\*)`",
                    memory_section,
                )
            )
            expected_families = set(TEMPLATE_FACT_ID_FAMILIES[name])
            if declared_families != expected_families:
                errors.append(
                    f"Skill fact-ID families must match its template: "
                    f"{skill_file.relative_to(ROOT)} expected="
                    f"{sorted(expected_families)}, got={sorted(declared_families)}"
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
                reference_sections = markdown_headings(ref_content, 2)
                expected_reference_sections = list(CAPABILITY_REFERENCE_SECTIONS)
                if reference_sections != expected_reference_sections:
                    errors.append(
                        f"Capability reference sections must exactly be "
                        f"{expected_reference_sections}: {ref_path.relative_to(ROOT)} "
                        f"has {reference_sections}"
                    )
                for heading in LEGACY_CAPABILITY_REFERENCE_SECTIONS:
                    if markdown_section(ref_content, heading) is not None:
                        errors.append(
                            f"Legacy capability section must be replaced by ability cards "
                            f"('{heading}'): {ref_path.relative_to(ROOT)}"
                        )
                require_terms(ref_path, ref_content, ref_terms, errors)
                expected_capability_headings = [
                    f"### {capability}"
                    for capability in REFERENCE_CAPABILITY_TERMS[name]
                ]
                capability_section = markdown_section(
                    ref_content,
                    "## 核心能力",
                )
                capability_headings = (
                    markdown_headings(capability_section, 3)
                    if capability_section is not None
                    else []
                )
                if (
                    len(capability_headings) != len(expected_capability_headings)
                    or set(capability_headings) != set(expected_capability_headings)
                ):
                    errors.append(
                        f"Capability cards must exactly be "
                        f"{expected_capability_headings}: {ref_path.relative_to(ROOT)} "
                        f"has {capability_headings}"
                    )
                for capability in REFERENCE_CAPABILITY_TERMS[name]:
                    capability_heading = f"### {capability}"
                    capability_card = markdown_heading_block(
                        ref_content,
                        capability_heading,
                    )
                    if capability_card is None:
                        errors.append(
                            f"Missing capability card '{capability_heading}': "
                            f"{ref_path.relative_to(ROOT)}"
                        )
                        continue
                    if not capability_card:
                        errors.append(
                            f"Empty capability card '{capability_heading}': "
                            f"{ref_path.relative_to(ROOT)}"
                        )
                        continue
                    require_terms(
                        ref_path,
                        capability_card,
                        CAPABILITY_CARD_FIELDS,
                        errors,
                    )
                    field_positions: list[int] = []
                    for field in CAPABILITY_CARD_FIELDS:
                        matches = list(
                            re.finditer(
                                rf"(?m)^-\s+{re.escape(field)}：",
                                capability_card,
                            )
                        )
                        if len(matches) != 1:
                            errors.append(
                                f"Capability card '{capability_heading}' must contain "
                                f"exactly one list field '{field}：': "
                                f"{ref_path.relative_to(ROOT)}"
                            )
                            continue
                        field_positions.append(matches[0].start())
                    if len(field_positions) == len(CAPABILITY_CARD_FIELDS) and (
                        field_positions != sorted(field_positions)
                    ):
                        errors.append(
                            f"Capability card fields are out of order in "
                            f"'{capability_heading}': {ref_path.relative_to(ROOT)}"
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

    delivery_skill = (SKILLS / "delivery" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    require_terms(
        SKILLS / "delivery" / "SKILL.md",
        delivery_skill,
        CORE_SKILLS - {"delivery"},
        errors,
    )
    delivery_memory_section = markdown_section(delivery_skill, "## 项目记忆")
    if delivery_memory_section:
        delivery_path = SKILLS / "delivery" / "SKILL.md"
        route_line = require_single_line_containing(
            delivery_path,
            delivery_memory_section,
            "跨角色总路由",
            errors,
        )
        if route_line:
            require_term_groups(
                delivery_path,
                route_line,
                DELIVERY_MEMORY_ROUTING_TERM_GROUPS,
                errors,
                "cross-role memory routing",
            )
            require_ordered_terms(
                delivery_path,
                route_line,
                DELIVERY_MEMORY_ROUTE_SEQUENCE,
                errors,
                "cross-role memory route",
            )
        reject_terms(
            delivery_path,
            delivery_memory_section,
            DELIVERY_MEMORY_FORBIDDEN_TERMS,
            errors,
            "delivery memory ownership",
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
                    template=True,
                )
                require_terms(
                    template_path,
                    template_content,
                    (
                        f"# {owner}",
                        f"../skills/{owner}/{CAPABILITY_REFERENCES[owner][0]}",
                    ),
                    errors,
                )
                validate_template_capability_link(
                    template_path,
                    template_content,
                    owner,
                    errors,
                )
                require_term_groups(
                    template_path,
                    template_content,
                    TEMPLATE_AI_TERM_GROUPS,
                    errors,
                    "fact-template lifecycle",
                )
                validate_fact_cards(
                    template_path,
                    template_content,
                    owner,
                    errors,
                    template=True,
                )
                validate_template_family_index(
                    template_path,
                    template_content,
                    owner,
                    errors,
                )
                validate_template_sections(
                    template_path,
                    template_content,
                    sections,
                    errors,
                )
            for heading in sections:
                require_section(template_path, template_content, heading, errors)

    for skill_name, memory_file in SKILL_MEMORY_FILES.items():
        memory_path = product_docs / memory_file
        if not memory_path.is_file():
            continue
        memory_content = memory_path.read_text(encoding="utf-8")
        fields = validate_memory_frontmatter(
            memory_path,
            skill_name,
            errors,
            template=False,
        )
        require_terms(memory_path, memory_content, (f"# {skill_name}",), errors)
        if fields.get("schema") == "2":
            validate_fact_cards(
                memory_path,
                memory_content,
                skill_name,
                errors,
                template=False,
            )
            validate_schema2_memory_sections(
                memory_path,
                memory_content,
                errors,
            )
            if "<!--" in memory_content or "<" + "事实" in memory_content:
                errors.append(
                    f"Instantiated schema 2 memory still contains template guidance or "
                    f"placeholders: {memory_path.relative_to(ROOT)}"
                )
            if skill_name == "verification":
                validate_schema2_verification_conclusion(
                    memory_path,
                    memory_content,
                    errors,
                )
        validate_instantiated_memory(memory_path, memory_content, errors)
        if skill_name == "verification" and fields.get("schema") == "1":
            validate_verification_conclusion(memory_path, memory_content, errors)

    active_legacy_paths = (
        ROOT / "README.md",
        ROOT / "references",
        ROOT / "scripts",
        ROOT / "skills",
        ROOT / "templates",
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
            reject_removed_root_reference_links(path, content, errors)
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
            for lifecycle_term in LEGACY_MEMORY_LIFECYCLE_TERMS:
                if lifecycle_term in content:
                    errors.append(
                        f"Legacy process-memory lifecycle '{lifecycle_term}' remains: "
                        f"{path.relative_to(ROOT)}"
                    )
            for replacement_term in FULL_REPLACEMENT_MEMORY_TERMS:
                if replacement_term in content:
                    errors.append(
                        f"Full-replacement memory lifecycle '{replacement_term}' remains: "
                        f"{path.relative_to(ROOT)}"
                    )
            for reuse_term in TEMPLATE_REUSE_MEMORY_TERMS:
                if reuse_term in content:
                    errors.append(
                        f"Existing memory must not reuse first-creation template "
                        f"'{reuse_term}': {path.relative_to(ROOT)}"
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
