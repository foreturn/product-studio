# release-engineering 当前产品事实 · 分发、热修复与发布沟通

## 三渠道分发证据边界

- **当前事实**：Codex 与 Antigravity 通过 `.agents/plugins/marketplace.json` 及根目录 `plugin.json` 描述安装源，Claude Code 通过 `.claude-plugin/marketplace.json` 描述仓库内插件源；README 分别给出安装与校验命令，源树静态通过不等于任一远端渠道已发布或缓存已刷新。
- **权威依据**：`plugin.json`；`.agents/plugins/marketplace.json`；`.claude-plugin/marketplace.json`；`README.md#安装`；`scripts/check.py`。
- **影响边界**：三端清单、marketplace、安装发现、Skill 选择和新上下文项目记忆行为必须分别取证；源树修改与静态校验本身既不会触发外部发布或安装，也不能证明远端渠道已更新。
- **复核入口**：先运行 `python scripts/check.py` 及三端清单校验，再在明确授权后分别执行渠道安装与新线程发现、项目记忆读取维护及后续复用检查；marketplace 地址、来源格式、版本或客户端 Skill 发现机制变化时重审。
