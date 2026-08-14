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

## 非语义终态守门边界

- **当前事实**：终态守门由 `UserPromptSubmit` 建立每回合基线，`PreToolUse` 与 `PostToolUse` 将工具前后仓库指纹写入同仓有界事件账本，`Stop` 再核验绑定当前会话、turn、最终指纹、观测验证、产品、Owner 与事实册路径的回执并最多请求一次续写；Hook 不选择专业、不裁定 Owner、不起草事实，也不从差异自动更新文档，只能核对观测证据、回执声明与事实册变化一致，不能证明 AI 已选全受影响 Owner 或事实语义正确。
- **权威依据**：`hooks/hooks.json`；`scripts/terminal-hook.mjs#handlePrompt`；`scripts/terminal-hook.mjs#handleToolEvent`；`scripts/terminal-hook.mjs#handleStop`；`references/terminal-protocol.md`
- **影响边界**：该边界只为客户端实际送达的 Hook 事件提供可写回合终态 guardrail，不是自动记忆引擎或不可绕过的执行沙箱，也不替代专业判断、Owner 完整性、验证质量或外部操作授权；非 Git 目录明确降级，同仓并发变更不静默归属。
- **复核入口**：运行 `node --test tests/terminal-hook.test.mjs`，核对四类事件、账本链、续写、回执、并发冲突、陈旧拒绝和非 Git 降级；Hook 事件、状态机、客户端事件字段或专业职责变化时重审。
