#!/usr/bin/env python3
"""Validate the shared Product Studio plugin without external dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
CORE_SKILLS = {
    "backend-contract",
    "delivery-verification",
    "frontend-experience",
    "product-delivery",
    "product-discovery",
    "release-operations",
    "system-design",
}
COMMON_SKILL_SECTIONS = (
    "## 输入契约",
    "## 核心能力",
    "## 输出契约",
    "## 交接门禁",
    "## 边界",
)
SKILL_CAPABILITY_TERMS = {
    "product-delivery": ("意图归类", "切片与排程", "依赖协调", "风险管理", "决策与变更控制", "质量门禁"),
    "product-discovery": ("问题定义", "用户与任务建模", "证据化联想", "旅程与状态设计", "范围与优先级", "成功衡量"),
    "system-design": ("系统建模", "边界与契约设计", "质量属性权衡", "一致性与故障设计", "安全与权限边界", "可观测与可运行性"),
    "frontend-experience": ("易用性与任务效率", "交互设计", "信息架构", "布局与响应式", "视觉协调", "可访问性", "前端性能与视觉验收"),
    "backend-contract": ("领域建模", "API 与错误契约", "数据建模与迁移", "权限与安全", "一致性与并发", "性能与可观测性", "测试策略"),
    "delivery-verification": ("需求追溯", "风险建模", "分层测试设计", "用户体验验收", "服务端与数据验收", "非功能验证", "证据审计"),
    "release-operations": ("发布策略", "制品与配置治理", "迁移编排", "可观测与健康判断", "风险控制与回滚", "事故处置", "反馈闭环"),
}
CAPABILITY_REFERENCES = {
    "product-delivery": ("references/delivery-capabilities.md", ("纵向切片", "关键路径", "风险", "阶段门禁", "状态汇报")),
    "product-discovery": ("references/product-design-principles.md", ("底层问题", "置信度", "最短完整旅程", "范围与优先级", "成功指标")),
    "system-design": ("references/architecture-principles.md", ("领域边界", "质量属性", "故障、一致性与恢复", "安全与隐私", "可观测性", "架构决策")),
    "frontend-experience": ("references/frontend-design-principles.md", ("合理默认值", "渐进披露", "撤销", "布局与响应式", "状态色", "对比度", "可访问性", "状态建模", "真实验收")),
    "backend-contract": ("references/backend-design-principles.md", ("领域模型", "API 与错误设计", "数据建模与迁移", "权限与安全", "事务、并发与幂等", "性能与可观测性", "测试策略")),
    "delivery-verification": ("references/verification-principles.md", ("要求追溯与风险建模", "分层测试策略", "前端与体验验收", "后端、数据与集成验收", "非功能与发布就绪", "证据与结论纪律")),
    "release-operations": ("references/release-principles.md", ("发布策略", "制品", "配置", "数据与迁移", "可观测性", "回滚", "反馈与迭代")),
}
TEMPLATE_SECTIONS = {
    "product-brief.md": (
        "## 原始意图",
        "## 证据与推断",
        "## 核心旅程",
        "## 范围",
        "## 验收标准",
    ),
    "feature-spec.md": (
        "## 用户流程",
        "## 验收标准",
        "## 验证方案",
        "## 未解决项与交接",
    ),
    "architecture-decision.md": (
        "## 不变量与失败模式",
        "## 候选方案",
        "## 迁移与回滚",
        "## 重审条件",
    ),
    "api-contract.md": (
        "## 错误响应",
        "## 不变量",
        "## 兼容与迁移",
        "## 调用方交接",
    ),
    "acceptance-report.md": (
        "## 要求与证据矩阵",
        "## 用户旅程证据",
        "## 失败与恢复证据",
        "## 最终结论",
    ),
    "release-plan.md": (
        "## 发布前门禁",
        "## 技术健康与业务成功信号",
        "## 停止条件与回滚",
        "## 反馈与下一轮迭代",
    ),
    "memory.md": (
        "## 关注事实",
        "## 关键决策",
        "## 约定与偏好",
        "## 待续事项",
        "## 最近变更",
    ),
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
            fields[key.strip()] = value.strip()
    return fields


def main() -> int:
    errors: list[str] = []
    codex_manifest = ROOT / ".codex-plugin" / "plugin.json"
    claude_manifest = ROOT / ".claude-plugin" / "plugin.json"
    claude_marketplace_manifest = ROOT / ".claude-plugin" / "marketplace.json"
    marketplace_manifest = ROOT / ".agents" / "plugins" / "marketplace.json"
    product_docs = ROOT / "docs" / "product" / "product-studio"
    required = [
        codex_manifest,
        claude_manifest,
        claude_marketplace_manifest,
        marketplace_manifest,
        ROOT / "templates" / "product-brief.md",
        ROOT / "templates" / "feature-spec.md",
        ROOT / "templates" / "architecture-decision.md",
        ROOT / "templates" / "api-contract.md",
        ROOT / "templates" / "acceptance-report.md",
        ROOT / "templates" / "release-plan.md",
        ROOT / "templates" / "memory.md",
        product_docs / "product-brief.md",
        product_docs / "feature-spec.md",
        product_docs / "architecture-decisions.md",
        product_docs / "acceptance-report.md",
    ]
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

    hooks_manifest = ROOT / "hooks" / "hooks.json"
    if not hooks_manifest.is_file():
        errors.append("Missing hooks/hooks.json")
    elif "SessionStart" not in hooks_manifest.read_text(encoding="utf-8"):
        errors.append("hooks/hooks.json must register a SessionStart hook")
    hooks_loader = ROOT / "hooks" / "scripts" / "load_role_memories.py"
    if not hooks_loader.is_file():
        errors.append("Missing hooks/scripts/load_role_memories.py")

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
        if not description:
            errors.append(f"Missing skill description: {skill_dir.name}")
        skill_names.add(name)

        content = skill_file.read_text(encoding="utf-8")
        require_terms(skill_file, content, COMMON_SKILL_SECTIONS, errors)
        if f"docs/memory/{name}.md" not in content:
            errors.append(
                f"Missing role memory reference docs/memory/{name}.md: {skill_dir.name}"
            )
        capability_terms = SKILL_CAPABILITY_TERMS.get(name)
        if capability_terms:
            require_terms(skill_file, content, capability_terms, errors)

        capability_reference = CAPABILITY_REFERENCES.get(name)
        if capability_reference:
            ref_name, ref_terms = capability_reference
            ref_path = skill_dir / ref_name
            if not ref_path.is_file():
                errors.append(f"Missing capability reference: {ref_path.relative_to(ROOT)}")
            else:
                require_terms(
                    ref_path,
                    ref_path.read_text(encoding="utf-8"),
                    ref_terms,
                    errors,
                )

        agent_metadata = skill_dir / "agents" / "openai.yaml"
        if not agent_metadata.is_file():
            errors.append(f"Missing Codex skill metadata: {agent_metadata.relative_to(ROOT)}")
        else:
            metadata = agent_metadata.read_text(encoding="utf-8")
            if f"${name}" not in metadata:
                errors.append(f"Codex default prompt does not invoke ${name}")

        for ref in re.findall(r"`((?:\.\./)+templates/[A-Za-z0-9_.-]+)`", content):
            if not (skill_dir / ref).resolve().is_file():
                errors.append(f"Broken template reference in {skill_dir.name}: {ref}")
        for ref in re.findall(r"`(references/[A-Za-z0-9_.-]+)`", content):
            if not (skill_dir / ref).is_file():
                errors.append(f"Broken capability reference in {skill_dir.name}: {ref}")

    for missing_skill in sorted(CORE_SKILLS - skill_names):
        errors.append(f"Missing core lifecycle skill: {missing_skill}")

    delivery_skill = (SKILLS / "product-delivery" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    require_terms(
        SKILLS / "product-delivery" / "SKILL.md",
        delivery_skill,
        CORE_SKILLS - {"product-delivery"},
        errors,
    )
    require_terms(
        SKILLS / "product-delivery" / "SKILL.md",
        delivery_skill,
        ("角色记忆", "docs/memory/"),
        errors,
    )

    discovery_skill = (SKILLS / "product-discovery" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    require_terms(
        SKILLS / "product-discovery" / "SKILL.md",
        discovery_skill,
        (
            "原始意图",
            "已确认事实",
            "仓库事实",
            "推断需求",
            "必须确认",
            "记录假设后继续",
            "自行查明",
        ),
        errors,
    )

    verification_skill = (SKILLS / "delivery-verification" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    require_terms(
        SKILLS / "delivery-verification" / "SKILL.md",
        verification_skill,
        ("要求—实现—证据—结论", "失败", "阻塞", "既有问题", "剩余风险"),
        errors,
    )

    for template_name, sections in TEMPLATE_SECTIONS.items():
        template_path = ROOT / "templates" / template_name
        if template_path.is_file():
            require_terms(
                template_path,
                template_path.read_text(encoding="utf-8"),
                sections,
                errors,
            )

    for contract_name in ("product-brief.md", "feature-spec.md"):
        contract_path = product_docs / contract_name
        if contract_path.is_file() and re.search(
            r"^- \[ \]", contract_path.read_text(encoding="utf-8"), re.MULTILINE
        ):
            errors.append(f"Unchecked acceptance criteria: {contract_path.relative_to(ROOT)}")

    acceptance_path = product_docs / "acceptance-report.md"
    if acceptance_path.is_file() and "- 结果：通过" not in acceptance_path.read_text(
        encoding="utf-8"
    ):
        errors.append("Product Studio acceptance report is not marked as passed")

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
