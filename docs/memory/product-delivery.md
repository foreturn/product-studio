# 角色记忆：product-delivery

- 角色与文件：`docs/memory/product-delivery.md`
- 当前产品或任务：product-studio 插件自身升级（角色专业化 + 按需调用 + 角色记忆簿）
- 最近更新：2026-07-30

## 关注事实

- product-studio 是 Claude Code + Codex 双平台插件，7 个角色 skill；产品交付契约写入 `docs/product/<slug>/`。
- 校验脚本 `scripts/validate_project.py` 硬性校验 frontmatter、能力术语、模板章节与双平台 manifest 一致性；任何改动须保持其通过。
- `description` 文本可自由修改；但各 SKILL.md 必须保留 `COMMON_SKILL_SECTIONS` 与各自的能力术语。

## 关键决策

| 决策 | 依据 | 影响范围 | 日期 |
|---|---|---|---|
| 角色记忆按角色分文件（`docs/memory/<role>.md`） | 职责分明，各角色只读写自己的记忆，互不干扰 | 全部角色 | 2026-07-30 |
| 读取用 `SessionStart` 钩子，写入靠 SKILL 指令 | plugin 内 `Stop` 钩子有失灵瑕疵（#29767），不可强依赖 | Claude Code 侧 | 2026-07-30 |

## 约定与偏好

- 中文写作；references 遵循极简/YAGNI，只补高价值、可操作的准则，不堆砌。
- 跨平台脚本仅用标准库（参照 `scripts/validate_project.py`）。

## 待续事项

| 事项 | 状态 | 下一步 | 阻塞 |
|---|---|---|---|
|  |  |  |  |

## 最近变更

- 2026-07-30｜初始化角色记忆簿机制，建立 `docs/memory/` 与 `SessionStart` 读取钩子。
