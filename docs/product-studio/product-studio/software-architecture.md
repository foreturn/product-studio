# software-architecture 当前产品事实

## 自主发现的专业技能拓扑

- **当前事实**：Product Studio 以十一项同级 Skill 暴露专业能力，编码代理依据请求、仓库证据和风险自主选择与排序；插件没有中央路由文件，任何 Skill 都不得声明另一 Skill 为固定前置、后继、退回或移交目标。
- **权威依据**：`README.md#三层文件契约`；`.codex-plugin/plugin.json`；`scripts/validate-project.mjs#validateTopology`
- **影响边界**：该拓扑约束 Codex 与 Claude Code 的渐进式技能发现及每项 Skill 的所有权表述；同一任务可以命中一个或多个专业，但技能数量不构成交付完整性的代理指标。
- **复核入口**：枚举 `skills/` 并运行 `node scripts/validate-project.mjs`，再检索固定调用链语言；技能集合、发现机制或所有权模型变化时重审。

## 专业内容三层分离

- **当前事实**：每项专业使用相同目录形制：`SKILL.md` 用中文 description 作发现摘要，正文只保留目标、执行、输出、完成、停止、权限、参考和终态八章，不以适用、不适用或必需输入清单代替 AI 自主判断，并按命中主题读取与权威复核；`references/principles.md` 按八至十六个专业大类组织，每类只列四至八条跨框架专业约束，不固化特定方案；`references/memory.md` 以统一七章和八字段规定五至九类终态语义，并以当前、稳定、非显然、决策相关、重查昂贵、唯一 Owner、可复核和安全留存作为共同门禁；目标事实册按类型自由选用段落、列表或表格，只保留当前语义、权威依据、影响范围与复核方式，不固定 Markdown 栏位；`agents/openai.yaml` 只承载界面元数据。
- **权威依据**：`README.md#三层文件契约`；`scripts/validate-project.mjs#SKILL_HEADINGS`；`scripts/validate-project.mjs#PRINCIPLE_HEADINGS`；`scripts/validate-project.mjs#assertConstraintLists`；`scripts/validate-project.mjs#FACT_FIELDS`
- **影响边界**：十一项 Skill 的加载体积、专业边界、维护审查和项目事实写法都依赖此分层；三类文件各自格式统一，但彼此不共用同一内容模型。
- **复核入口**：运行项目契约校验与十一项 `quick_validate.py`，检查精确章节、能力索引、每类约束条目数、事实类型数量、共同门禁、字段顺序、locator 和元数据；任一文件职责或统一结构变化时重审。

## 提示式终态记忆边界

- **当前事实**：每项专业 Skill 在自身“终态记忆”章节内写死 Owner 与事实册 locator，并要求最终答复前主动读取该 Owner 的 memory 规则、复核命中主题、执行事实动作和报告终态结果；公共终态协议只统一多 Owner 协调、权威删除、按 `BLOCKED` > `DEFERRED` > `SYNCED` > `NO_CHANGE` 的互斥结果及安全边界。插件不维护独立运行时状态，专业差异仍由各 Skill 的 memory 规则渐进加载。
- **权威依据**：`skills/*/SKILL.md#终态记忆`；`skills/*/references/memory.md`；`references/terminal-protocol.md`；`scripts/validate-project.mjs#validateTerminalMemoryContract`
- **影响边界**：该结构使事实选择、语义判断与写入责任保持在唯一 Owner 内，并消除客户端事件格式、信任和会话状态依赖；代价是提示契约无法机械阻断遗漏，也不能自行证明编码代理已选全受影响 Owner、写入正确或在后续会话完成读取。
- **复核入口**：运行项目校验与十一项 Skill 独立校验，确认每份提示都绑定正确 Owner、locator、四种动作与四种结果；再以未显式点名 Skill 的新上下文任务验证专业选择、实际写入、无变化守恒与跨会话读取。Skill 提示、公共协议、Owner 模型或事实存储边界变化时重审。
