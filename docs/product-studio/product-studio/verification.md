# quality-engineering 当前产品事实

## 独立质量与事实门禁

- **当前事实**：`quality-engineering` 从原始意图、专业契约与完整差异设计风险相称的证据，对当前修订作通过、失败、阻塞或不适用裁决；实现自测不能替代总体结论。只有获准写入、已形成终态且总体通过的实际核验范围才具备事实同步资格；失败、阻塞、未形成终态或只读未授权时不得写事实册。
- **权威依据**：`skills/quality-engineering/SKILL.md#输出`；`skills/quality-engineering/SKILL.md#完成门槛`；`skills/fact-sync/SKILL.md#输入门禁`
- **影响边界**：前后端、数据库、安全和架构实现的完成声明，以及九位专业 Owner 的事实落盘，均依赖绑定当前修订、环境、输入和断言的质量证据；质量通过不构成生产操作授权或环境健康结论。
- **复核入口**：以聚焦逻辑、真实数据库迁移、浏览器交互、安全控制、失败测试和验收后直接发布等场景检查证据层级、独立裁决、Owner 语义边界、事实停止点与发布授权边界。

## 插件结构与行为证据

- **当前事实**：仓库以 `quick_validate.py` 逐项检查 Skill 结构，以 `validate_plugin.py .` 检查 Codex 插件清单，以 `claude plugin validate --strict .` 检查 Claude marketplace 结构，并以契约扫描检查十技能集合、旧 Router 引用、目录与 frontmatter 同名、三层职责边界及九份专业事实类型规则；这些静态证据不证明新上下文中的真实技能发现和专业判断正确。
- **权威依据**：`README.md#校验`；`.codex-plugin/plugin.json#skills`；`.claude-plugin/marketplace.json#plugins[0]`
- **影响边界**：Codex 与 Claude Code 两套分发面、十项 Skill 的形制、专业资料边界和事实类型结构均有可重复入口；任一平台或静态检查通过不得外推到另一平台安装成功、自动触发正确或目标环境行为成立。
- **复核入口**：设置 UTF-8 后对 `skills/*` 逐项运行 Skill validator，再运行 Codex 与 Claude 插件 validator 和仓库契约扫描；行为证据须在全新上下文中用未点名 Skill 的正反向场景另行取得，已验证的规则检索不等于已证明平台自动发现。
