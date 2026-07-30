#!/usr/bin/env python3
"""SessionStart 钩子：将当前项目 docs/memory/ 下的角色记忆合并注入会话上下文。

扫描 $CLAUDE_PROJECT_DIR/docs/memory/*.md（回退到当前工作目录的 docs/memory/），
读取全部角色记忆文件并合并为 SessionStart 的 additionalContext 输出。
目录或文件不存在时静默退出（退出码 0），不报错、不阻断会话。

仅使用标准库，跨平台，与 scripts/validate_project.py 的依赖约定一致。
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def discover_memory_dir() -> Path | None:
    """定位当前项目的 docs/memory 目录，找不到返回 None。"""
    candidates: list[Path] = []
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_dir:
        candidates.append(Path(project_dir) / "docs" / "memory")
    candidates.append(Path.cwd() / "docs" / "memory")
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    return None


def load_memories(memory_dir: Path) -> list[tuple[str, str]]:
    """读取目录下全部 .md，返回 (角色名, 正文) 列表，按文件名排序。"""
    items: list[tuple[str, str]] = []
    for path in sorted(memory_dir.glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8").strip()
        except (OSError, UnicodeDecodeError):
            continue
        if text:
            items.append((path.stem, text))
    return items


def main() -> int:
    memory_dir = discover_memory_dir()
    if memory_dir is None:
        return 0  # 无记忆目录，静默退出
    items = load_memories(memory_dir)
    if not items:
        return 0

    parts = ["# 项目角色记忆（docs/memory/，跨会话延续）"]
    for name, text in items:
        parts.append(f"\n## {name}\n\n{text}")
    additional_context = "\n".join(parts)

    payload = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": additional_context,
        }
    }
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
