#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Product Studio 静态契约与规范校验脚本。
验证内容：
1. 十一项技能的目录规范、必要文件完整性、Frontmatter 元数据、执行契约标题规范及 openai.yaml 模式结构。
2. principles/ 与 memory/ 之间能力簇分卷的双射映射（Bijective mapping）。
3. 相对链接的有效性（principles.md 等）。
4. 各平台插件清单（plugin.json, .claude-plugin, .codex-plugin, opencode.json, package.json, marketplace）版本与描述一致性、技能路径解析。
5. 自身事实册（docs/product-studio/product-studio/）拓扑规范、Owner 归属与标题首行契约。
"""

import os
import sys
import json
import re
import yaml

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def check_skills():
    skills_dir = os.path.join(ROOT_DIR, "skills")
    if not os.path.isdir(skills_dir):
        print("[FAIL] 缺少 skills/ 目录")
        return False

    skills = sorted([d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))])
    if len(skills) != 11:
        print(f"[FAIL] 技能数量异常：期望 11 项，实际发现 {len(skills)} 项")
        return False

    has_error = False
    print(f"[*] 开始检查 {len(skills)} 项专业技能内部契约与元数据...")

    for skill in skills:
        skill_path = os.path.join(skills_dir, skill)
        
        # 1. 基础文件完整性
        required_files = [
            "SKILL.md",
            os.path.join("agents", "openai.yaml"),
            os.path.join("references", "principles.md"),
        ]
        for rf in required_files:
            fp = os.path.join(skill_path, rf)
            if not os.path.isfile(fp):
                print(f"  [ERROR] {skill}: 缺失必要文件 {rf}")
                has_error = True

        # 2. SKILL.md Frontmatter 元数据与 H1 契约标题
        skill_md_path = os.path.join(skill_path, "SKILL.md")
        if os.path.isfile(skill_md_path):
            with open(skill_md_path, "r", encoding="utf-8") as f:
                content = f.read()

            fm_match = re.match(r"^---\r?\n(.*?)\r?\n---", content, re.DOTALL)
            if not fm_match:
                print(f"  [ERROR] {skill}: SKILL.md 缺失 YAML Frontmatter")
                has_error = True
            else:
                try:
                    fm = yaml.safe_load(fm_match.group(1))
                    if not isinstance(fm, dict):
                        print(f"  [ERROR] {skill}: SKILL.md Frontmatter 格式异常")
                        has_error = True
                    else:
                        if fm.get("name") != skill:
                            print(f"  [ERROR] {skill}: SKILL.md name ({fm.get('name')}) 与目录名不匹配")
                            has_error = True
                        if not fm.get("description") or not str(fm.get("description")).strip():
                            print(f"  [ERROR] {skill}: SKILL.md 缺少有效 description")
                            has_error = True
                except Exception as e:
                    print(f"  [ERROR] {skill}: 解析 SKILL.md Frontmatter 失败: {e}")
                    has_error = True

            # 校验 H1 标题必须统一为“执行契约”规制
            h1_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            if not h1_match:
                print(f"  [ERROR] {skill}: SKILL.md 缺少一级标题")
                has_error = True
            else:
                h1_title = h1_match.group(1).strip()
                if not h1_title.endswith("执行契约"):
                    print(f"  [ERROR] {skill}: SKILL.md 一级标题未以'执行契约'结尾: '{h1_title}'")
                    has_error = True

        # 3. agents/openai.yaml 模式校验
        openai_yaml_path = os.path.join(skill_path, "agents", "openai.yaml")
        if os.path.isfile(openai_yaml_path):
            try:
                with open(openai_yaml_path, "r", encoding="utf-8") as f:
                    oy = yaml.safe_load(f)
                iface = oy.get("interface") if isinstance(oy, dict) else None
                if not isinstance(iface, dict):
                    print(f"  [ERROR] {skill}: openai.yaml 缺失 interface 字典")
                    has_error = True
                else:
                    for field in ["display_name", "short_description", "default_prompt"]:
                        val = iface.get(field)
                        if not val or not str(val).strip():
                            print(f"  [ERROR] {skill}: openai.yaml 缺失有效 interface.{field}")
                            has_error = True
            except Exception as e:
                print(f"  [ERROR] {skill}: 解析 agents/openai.yaml 失败: {e}")
                has_error = True

        # 4. principles/ 与 memory/ 双射映射
        p_dir = os.path.join(skill_path, "references", "principles")
        m_dir = os.path.join(skill_path, "references", "memory")

        p_files = set(os.listdir(p_dir)) if os.path.isdir(p_dir) else set()
        m_files = set(os.listdir(m_dir)) if os.path.isdir(m_dir) else set()

        if p_files != m_files:
            has_error = True
            diff_p = p_files - m_files
            diff_m = m_files - p_files
            if diff_p:
                print(f"  [ERROR] {skill}: principles 存在但 memory 缺失: {diff_p}")
            if diff_m:
                print(f"  [ERROR] {skill}: memory 存在但 principles 缺失: {diff_m}")

        # 5. principles.md 相对链接有效性
        p_index = os.path.join(skill_path, "references", "principles.md")
        if os.path.isfile(p_index):
            with open(p_index, "r", encoding="utf-8") as f:
                content = f.read()
            links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
            for text, link in links:
                target = os.path.normpath(os.path.join(os.path.dirname(p_index), link))
                if not os.path.exists(target):
                    print(f"  [ERROR] {skill}: principles.md 中存在死链 '{link}' -> {target}")
                    has_error = True

    if not has_error:
        print(f"  [PASS] 全部 11 项技能结构、元数据模式、簇双射映射与索引链接均有效。")
    return not has_error


def check_manifests_and_versions():
    print("[*] 开始检查各平台插件清单版本、元数据与技能路径一致性...")
    has_error = False

    manifest_paths = {
        "root": os.path.join(ROOT_DIR, "plugin.json"),
        "claude": os.path.join(ROOT_DIR, ".claude-plugin", "plugin.json"),
        "codex": os.path.join(ROOT_DIR, ".codex-plugin", "plugin.json"),
        "opencode": os.path.join(ROOT_DIR, "opencode.json"),
        "pi": os.path.join(ROOT_DIR, "package.json"),
    }

    versions = {}
    descriptions = {}
    for name, path in manifest_paths.items():
        if not os.path.isfile(path):
            print(f"  [ERROR] 缺失清单文件: {path}")
            has_error = True
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            v = data.get("version")
            desc = data.get("description")
            versions[name] = v
            descriptions[name] = desc

            # 校验声明的 skills 路径相对于仓库根目录 ROOT_DIR 真实存在
            if name == "opencode":
                for sp in data.get("skills", []):
                    resolved = os.path.normpath(os.path.join(ROOT_DIR, sp))
                    if not os.path.isdir(resolved):
                        print(f"  [ERROR] {name}: 声明的 skills 目录不存在: {resolved}")
                        has_error = True
            elif name == "pi":
                for sp in data.get("pi", {}).get("skills", []):
                    resolved = os.path.normpath(os.path.join(ROOT_DIR, sp))
                    if not os.path.isdir(resolved):
                        print(f"  [ERROR] {name}: 声明的 pi.skills 目录不存在: {resolved}")
                        has_error = True
            else:
                sp = data.get("skills")
                if sp:
                    resolved = os.path.normpath(os.path.join(ROOT_DIR, sp))
                    if not os.path.isdir(resolved):
                        print(f"  [ERROR] {name}: 声明的 skills 目录不存在: {resolved}")
                        has_error = True

        except Exception as e:
            print(f"  [ERROR] 解析 {path} 失败: {e}")
            has_error = True

    # 版本一致性
    unique_versions = set(versions.values())
    if len(unique_versions) > 1:
        print(f"  [ERROR] 平台清单版本不一致: {versions}")
        has_error = True
    elif len(unique_versions) == 1:
        target_version = list(unique_versions)[0]
        print(f"  [PASS] 核心清单版本统一为: {target_version}")

        # 校验 .agents/plugins/marketplace.json 版本
        mp_path = os.path.join(ROOT_DIR, ".agents", "plugins", "marketplace.json")
        if os.path.isfile(mp_path):
            with open(mp_path, "r", encoding="utf-8") as f:
                mp_data = json.load(f)
            for p in mp_data.get("plugins", []):
                if p.get("name") == "product-studio":
                    mp_v = p.get("version")
                    if mp_v and mp_v != target_version:
                        print(f"  [ERROR] marketplace.json 中的版本号 ({mp_v}) 与清单版本 ({target_version}) 不一致")
                        has_error = True

    # 描述一致性（包括清单与两个 marketplace）
    mp_agents_path = os.path.join(ROOT_DIR, ".agents", "plugins", "marketplace.json")
    if os.path.isfile(mp_agents_path):
        with open(mp_agents_path, "r", encoding="utf-8") as f:
            for p in json.load(f).get("plugins", []):
                if p.get("name") == "product-studio":
                    descriptions["agents_marketplace"] = p.get("description")

    mp_claude_path = os.path.join(ROOT_DIR, ".claude-plugin", "marketplace.json")
    if os.path.isfile(mp_claude_path):
        with open(mp_claude_path, "r", encoding="utf-8") as f:
            for p in json.load(f).get("plugins", []):
                if p.get("name") == "product-studio":
                    descriptions["claude_marketplace"] = p.get("description")

    unique_descs = set(descriptions.values())
    if len(unique_descs) > 1:
        print(f"  [ERROR] 清单与市场描述不一致: {descriptions}")
        has_error = True
    else:
        print("  [PASS] 核心清单与各端市场插件描述统一对齐。")

    return not has_error


def check_internal_facts():
    print("[*] 开始检查内部事实册 (docs/product-studio/product-studio/) 拓扑与规范...")
    facts_root = os.path.join(ROOT_DIR, "docs", "product-studio", "product-studio")
    if not os.path.isdir(facts_root):
        print(f"  [WARN] 未找到内部事实册根目录: {facts_root}")
        return True

    skills_dir = os.path.join(ROOT_DIR, "skills")
    valid_skills = set(os.listdir(skills_dir)) if os.path.isdir(skills_dir) else set()

    has_error = False
    fact_count = 0

    for root, dirs, files in os.walk(facts_root):
        for f in files:
            if not f.endswith(".md"):
                continue
            fact_count += 1
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, facts_root)
            parts = rel_path.split(os.sep)

            if len(parts) != 2:
                print(f"  [ERROR] 事实册文件层级不合规 (应为 <owner>/<cluster>.md): {rel_path}")
                has_error = True
                continue

            owner, cluster_file = parts[0], parts[1]
            cluster_name = cluster_file[:-3]

            if owner not in valid_skills:
                print(f"  [ERROR] 事实册拥有者 '{owner}' 并非已知 11 项技能之一: {rel_path}")
                has_error = True

            principle_file = os.path.join(skills_dir, owner, "references", "principles", cluster_file)
            if not os.path.isfile(principle_file):
                print(f"  [ERROR] 事实册分卷 '{cluster_file}' 在 {owner} 的 principles/ 中不存在对应簇卷: {rel_path}")
                has_error = True

            with open(full_path, "r", encoding="utf-8") as fp:
                first_line = fp.readline().strip()
                expected_prefix = f"# {owner} 当前产品事实 · "
                if not first_line.startswith(expected_prefix):
                    print(f"  [ERROR] 事实册首行标题不符合规范 (期望以 '{expected_prefix}' 开头): {rel_path}")
                    has_error = True

    if not has_error:
        print(f"  [PASS] 内部事实册共 {fact_count} 篇分卷，所有 Owner 归属、分卷映射及首行格式均合规。")
    return not has_error


def main():
    print("=" * 60)
    print(" Product Studio 工程契约校验")
    print("=" * 60)

    skills_ok = check_skills()
    versions_ok = check_manifests_and_versions()
    facts_ok = check_internal_facts()

    print("=" * 60)
    if skills_ok and versions_ok and facts_ok:
        print("[SUCCESS] 所有内部工程契约校验通过！")
        return 0
    else:
        print("[FAILED] 存在未满足的工程契约，请检查上方日志。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
