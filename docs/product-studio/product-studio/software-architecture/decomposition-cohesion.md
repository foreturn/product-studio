# software-architecture 当前产品事实 · 分解、内聚与代码组织

## 自主发现的专业技能拓扑

- **当前事实**：Product Studio 以十一项同级 Skill 暴露专业能力，编码代理依据请求、仓库证据和风险自主选择与排序；插件没有中央路由文件，任何 Skill 都不得声明另一 Skill 为固定前置、后继、退回或移交目标。
- **权威依据**：`README.md#三层文件契约`；`.codex-plugin/plugin.json`；`scripts/validate-project.mjs#validateTopology`
- **影响边界**：该拓扑约束 Codex 与 Claude Code 的渐进式技能发现及每项 Skill 的所有权表述；同一任务可以命中一个或多个专业，但技能数量不构成交付完整性的代理指标。
- **复核入口**：枚举 `skills/` 并运行 `node scripts/validate-project.mjs`，再检索固定调用链语言；技能集合、发现机制或所有权模型变化时重审。

## 专业内容三层分离

- **当前事实**：每项专业使用相同目录形制：`SKILL.md` 用中文 description 作发现摘要，正文只保留目标、执行、输出、完成、停止、权限、参考和项目记忆八章，其中“项目记忆”章承载当前产品根目录与产品标识定位、按簇事实读取、准入、随写随记与收口对账维护及排除规则；`references/principles.md` 以瘦索引列四至六个能力簇与任务句式命中条件，约束正文按簇分卷于 `references/principles/`，全部簇卷合计八至十六个专业大类，每类只列四至八条跨框架专业约束；`references/memory/` 按能力簇分卷，卷名与 `references/principles/` 簇卷文件名一致，每卷以簇名为题，只列一至十二条“记住……”普通列表详细定义未来 AI 应记住的项目不变量；`agents/openai.yaml` 只承载界面元数据。
- **权威依据**：`README.md#三层文件契约`；`scripts/validate-project.mjs#SKILL_HEADINGS`；`scripts/validate-project.mjs#PRINCIPLE_HEADINGS`；`scripts/validate-project.mjs#assertMemoryVolumes`
- **影响边界**：十一项 Skill 的加载体积、专业边界、维护审查和项目事实写法都依赖此分层；三类文件各自格式统一，但彼此不共用同一内容模型。
- **复核入口**：运行项目契约校验与十一项 `quick_validate.py`，检查精确章节、能力索引、每类约束条目数、memory 簇卷与 principles 簇卷一一对应、每卷条目数与“记住”陈述、SKILL 内 Owner locator 和元数据；任一文件职责或统一结构变化时重审。

## 完整业务流优先的能力复用与极简实现

- **当前事实**：Product Studio 的软件架构、后端、Web、Android 与 iOS 工程要求会改变用户任务、领域行为或共享能力的实施，先沿真实入口及实际存在的调用、状态、持久化、数据交互和副作用追踪至可确认结果，识别能力所有者、既有实现、共同不变量与真实消费者。相同业务动作由唯一用例、领域公共面或稳定业务契约承载，接口、消息、任务、页面和系统入口只作协议或平台适配，不以参数化样例、抽取工具函数或复制条件冒充复用；业务能力复用之后才评估语言、平台与成熟开源组件提供的技术机制。代码仍须先完整满足已确认功能、边界与验收，再在行为等价方案中以用户步骤、业务状态与交接、代码路径、运行部件、失败恢复和变更扩散的总成本选择整体最简且易读的实现。
- **权威依据**：`skills/software-architecture/SKILL.md#执行协议`；`skills/software-architecture/references/principles/decomposition-cohesion.md#代码组织命名与能力复用`；`skills/backend-engineering/SKILL.md#执行协议`；`skills/backend-engineering/references/principles/domain-structure.md#应用分层与模块内聚`；Web、Android 与 iOS 工程的 `SKILL.md#执行协议`、工程结构准则及 `references/memory/`。
- **影响边界**：该约束影响服务端与客户端实现、共享业务能力、调用链和消费者契约；它不要求为单一消费者或假想变化预建通用框架，也不允许以复用或极简之名省略权限、错误、事务、数据约束、副作用、恢复或验证。平台标准与开源复用仍须审查契约、维护、安全、许可、体积、依赖、运维、升级和退出成本。
- **复核入口**：运行项目与各 Skill 校验，并以同一业务动作的接口、消息、任务、页面及系统入口检查是否收敛到同一能力和结果语义；再用当前样例、等价变体、相邻业务情形及失败恢复路径核对完整流程。能力所有权、消费者、调用链、工程专业范围或复用优先级变化时重审。
