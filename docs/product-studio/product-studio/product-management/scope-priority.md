# product-management 当前产品事实 · 范围与优先级

## 十一项通用专业底座

- **当前事实**：Product Studio 的通用产品软件范围固定为十一项独立专业能力：产品管理、软件架构、后端、Web、Android、iOS、数据库、平台、安全、质量与发布工程；产品管理同时拥有产品意图和产品体验语义，不再设置第二个体验裁决入口。
- **权威依据**：`README.md#十一项通用底座`；`.codex-plugin/plugin.json#keywords`；`scripts/validate-project.mjs#EXPECTED_SKILLS`
- **影响边界**：Codex 与 Claude Code 的技能发现、插件说明、专业 Owner 和项目事实 locator 均以此集合为准；数据工程与 AI 系统等条件专业不在当前通用底座内。
- **复核入口**：运行 `node scripts/validate-project.mjs` 核对技能目录、frontmatter、双端清单和 README 拓扑完全一致；新增、合并、删除或改名任何通用专业时重审。
