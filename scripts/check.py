#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Product Studio 静态契约校验脚本。
验证内容：
1. 十一项技能的目录规范与必要文件完整性。
2. principles/ 与 memory/ 之间能力簇分卷的双射映射（Bijective mapping）。
3. references/principles.md 中索引链接的有效性。
4. 各平台插件清单（plugin.json, .claude-plugin, .codex-plugin, marketplace）版本一致性。
"""

import os
import sys
import json
import re

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
    print(f"[*] 开始检查 {len(skills)} 项专业技能内部契约...")

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

        # 2. principles/ 与 memory/ 双射映射
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

        # 3. principles.md 相对链接有效性
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
        print(f"  [PASS] 全部 11 项技能结构、簇双射映射与索引链接均有效。")
    return not has_error


def check_versions():
    print("[*] 开始检查各平台插件清单版本一致性...")
    has_error = False

    manifest_paths = {
        "root": os.path.join(ROOT_DIR, "plugin.json"),
        "claude": os.path.join(ROOT_DIR, ".claude-plugin", "plugin.json"),
        "codex": os.path.join(ROOT_DIR, ".codex-plugin", "plugin.json"),
        "opencode": os.path.join(ROOT_DIR, "opencode.json"),
    }

    versions = {}
    for name, path in manifest_paths.items():
        if not os.path.isfile(path):
            print(f"  [ERROR] 缺失清单文件: {path}")
            has_error = True
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            v = data.get("version")
            versions[name] = v
        except Exception as e:
            print(f"  [ERROR] 解析 {path} 失败: {e}")
            has_error = True

    unique_versions = set(versions.values())
    if len(unique_versions) > 1:
        print(f"  [ERROR] 平台清单版本不一致: {versions}")
        has_error = True
    elif len(unique_versions) == 1:
        target_version = list(unique_versions)[0]
        print(f"  [PASS] 核心清单版本统一为: {target_version}")

        # 校验 .agents/plugins/marketplace.json
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

    return not has_error


def main():
    print("=" * 60)
    print(" Product Studio 工程契约校验")
    print("=" * 60)

    skills_ok = check_skills()
    versions_ok = check_versions()

    print("=" * 60)
    if skills_ok and versions_ok:
        print("[SUCCESS] 所有内部工程契约校验通过！")
        return 0
    else:
        print("[FAILED] 存在未满足的工程契约，请检查上方日志。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
