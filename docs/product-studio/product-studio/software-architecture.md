# software-architecture 当前产品事实

## 自主发现的专业技能拓扑

- **当前事实**：Product Studio 以十一项同级 Skill 暴露专业能力，编码代理依据请求、仓库证据和风险自主选择与排序；插件没有中央路由文件，任何 Skill 都不得声明另一 Skill 为固定前置、后继、退回或移交目标。
- **权威依据**：`README.md#三层文件契约`；`.codex-plugin/plugin.json`；`scripts/validate-project.mjs#validateTopology`
- **影响边界**：该拓扑约束 Codex 与 Claude Code 的渐进式技能发现及每项 Skill 的所有权表述；同一任务可以命中一个或多个专业，但技能数量不构成交付完整性的代理指标。
- **复核入口**：枚举 `skills/` 并运行 `node scripts/validate-project.mjs`，再检索固定调用链语言；技能集合、发现机制或所有权模型变化时重审。

## 专业内容三层分离

- **当前事实**：每项专业使用相同目录形制：`SKILL.md` 用中文 description 作发现摘要，正文只保留目标、执行、输出、完成、停止、权限、参考和项目记忆八章，不以适用、不适用或必需输入清单代替 AI 自主判断；`references/principles.md` 按八至十六个专业大类组织，每类只列四至八条跨框架专业约束；`references/memory.md` 只有“使用方式”和“核心记忆”两章，以五至九个专业主题、每题一至三条普通列表说明未来 AI 应记住的项目不变量；`agents/openai.yaml` 只承载界面元数据。
- **权威依据**：`README.md#三层文件契约`；`scripts/validate-project.mjs#SKILL_HEADINGS`；`scripts/validate-project.mjs#PRINCIPLE_HEADINGS`；`scripts/validate-project.mjs#MEMORY_HEADINGS`；`scripts/validate-project.mjs#assertCoreMemoryLists`
- **影响边界**：十一项 Skill 的加载体积、专业边界、维护审查和项目事实写法都依赖此分层；三类文件各自格式统一，但彼此不共用同一内容模型。
- **复核入口**：运行项目契约校验与十一项 `quick_validate.py`，检查精确章节、能力索引、每类约束条目数、核心记忆主题数量、每题条目数、Owner locator 和元数据；任一文件职责或统一结构变化时重审。

## 项目记忆边界

- **当前事实**：每项专业 Skill 在自身“项目记忆”章节内绑定 Owner 事实册 locator，要求先唯一确认目标 Git 根与安全单级 `product-id`，工作前读取相关核心认知、以当前权威纠正旧事实，并在认知改变时于既有写权限内更新或移除旧内容；每份 `references/memory.md` 自含本专业的使用方式与应记主题，不再依赖公共协议，也不定义动作或结果状态。
- **权威依据**：`skills/*/SKILL.md#项目记忆`；`skills/*/references/memory.md`；`scripts/validate-project.mjs#validateRemovedRuntimeAssets`
- **影响边界**：该结构使事实选择、语义判断与维护责任保持在唯一 Owner 内，并消除客户端事件格式、信任和会话状态依赖；代价是提示指令无法机械阻断遗漏，也不能自行证明编码代理已选全受影响 Owner、维护正确或在后续会话完成读取。
- **复核入口**：运行项目校验与十一项 Skill 独立校验，确认每份提示都绑定正确 Owner、locator、当前权威优先和安全边界；再以未显式点名 Skill 的新上下文任务验证专业选择、相关事实读取、认知变化后的维护与跨会话复用。Skill 提示、Owner 模型或事实存储边界变化时重审。
