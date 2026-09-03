# quality-engineering 当前产品事实

## 插件结构契约校验

- **当前事实**：仓库的 `validate-project.mjs` 机械核对恰好十一项 Skill、三类文件各自的精确章节、principles 的八至十六个专业大类及每类四至八条通用约束、memory 仅含“核心记忆”且具有五至九个主题及每题一至三条“记住……”普通列表；对每份 SKILL 还核对决策中的目标政策、事实、推断与假设分层，具体方案来源不自证，完整流程复核，失效决定局部重开、无关决定保护与专业所有权边界，以及当前产品根目录不依赖 Git、用户目录与目标工件证据、Git 仅作佐证、进程目录与 Skill 目录不得决定根、Product Studio 仅作技能提供者时排除其源码与安装缓存、安全单级 `product-id`、根锚定 Owner locator、工作前读取、当前权威优先、既有事实准入、只读边界、产品根写权限、最终回复前直接维护、首册创建、空册禁令、实例标题与主题写法、末项清理和敏感信息排除，并拒绝旧有“目标 Git 根”措辞。README 同样受决策反思及产品根、非 Git、提供者排除与锚定读取断言约束；现有项目事实册必须标题匹配 Owner 且至少包含一个非空当前事实主题，OpenAI 界面元数据、已移除运行资产与公共协议及双端清单拓扑亦受校验，任一不一致以非零退出。
- **权威依据**：`scripts/validate-project.mjs`；`README.md#三层文件契约`；`.codex-plugin/plugin.json`
- **影响边界**：该入口证明源树结构、提示契约和声明一致，不证明专业内容在真实任务中被正确触发、判断或执行，也不证明任一客户端已安装当前快照或代理一定完成事实写入与后续读取。
- **复核入口**：运行 `node scripts/validate-project.mjs` 并检查退出码；技能集合、统一格式、memory 主题、manifest、项目记忆提示、事实册生命周期或 locator 规则变化时先更新机械断言，再更新实现。

## 单项 Skill 结构入口

- **当前事实**：每项 Skill 可使用当前 `skill-creator` 的 `quick_validate.py` 独立检查 frontmatter、命名与基本结构，项目契约校验再补充本插件的统一章节、principles 通用约束清单、memory 的单一“核心记忆”章、主题数量与“记住……”普通列表、SKILL 的项目记忆定位读取准入维护指令、Owner locator 和跨文件拓扑约束；两类静态检查互不替代。
- **权威依据**：`skills/product-management/SKILL.md`；`skills/release-engineering/SKILL.md`；`scripts/validate-project.mjs#validateSkill`
- **影响边界**：十一项 Skill 的源文件结构受此入口保护；详细专业正确性、自动发现、边界服从和实际行为仍需压力场景与真实任务证据。
- **复核入口**：枚举 `skills/` 后对每个实际目录运行 `quick_validate.py`，再运行项目校验并分别记录失败；skill-creator 规则或本插件结构契约变化时重审。

## 决策失效的缺陷归因守卫

- **当前事实**：质量工程不把用户或编码代理提出的具体方案、当前实现与已有测试反向提升为预期行为。缺陷分析从首个错误状态和最小复现出发，先区分实现偏离已确认决定、决定前提被证伪和适用条件变化，再区分产品缺陷、测试缺陷、环境故障、契约冲突与证据不足；失败若证伪上游决定前提，质量结论须指出待重审决定、影响范围和仍有效边界，不以放宽断言、增加下游例外或只修症状换取表面通过。
- **权威依据**：`skills/quality-engineering/SKILL.md#执行协议`；`skills/quality-engineering/references/principles.md#质量判据与可证伪性`；`skills/quality-engineering/references/principles.md#缺陷归因与不稳定测试`；`skills/quality-engineering/references/memory.md#缺陷归因不稳定测试与结论守卫`
- **影响边界**：该守卫约束缺陷归因、回归设计和质量结论，不替代产品或架构 Owner 重作其专业决定，也不把尚未验证的根因推断写成质量事实。
- **复核入口**：以实现错误、错误决策、条件变化、契约冲突和证据不足五类相似故障检查归因能否区分，并确认错误决策场景不会通过修改测试或下游特例掩盖；缺陷分类或质量结论模型变化时重审。
