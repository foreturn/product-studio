# quality-engineering 当前产品事实 · 证据层级、隔离与自动化

## 技能元数据与清单校验

- **当前事实**：技能元数据可使用 `skill-creator` 提供的 `quick_validate.py` 检查 frontmatter、命名与描述；Claude Code CLI 可分别校验 marketplace 和插件清单。能力簇、专业规则与项目记忆的语义完整性由任务评审和实际使用证据判断。
- **权威依据**：`README.md#校验`；`skills/*/SKILL.md`；`.claude-plugin/marketplace.json`；`.claude-plugin/plugin.json`。
- **影响边界**：这些工具的通过结果不能证明专业选择、规则合理性、提示完整性或事实册正确维护，也不能替代安装后的新会话验证。
- **复核入口**：按实际变更运行相关元数据或清单检查；以具体任务、真实边界和可观察结果评审提示效果，技能接口、客户端加载方式或验证工具发生变化时重审。
