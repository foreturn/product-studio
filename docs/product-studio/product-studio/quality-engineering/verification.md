# quality-engineering 当前产品事实 · 运行证据、归因与质量结论

## 决策失效的缺陷归因守卫

- **当前事实**：质量工程不把用户或编码代理提出的具体方案、当前实现与已有测试反向提升为预期行为。缺陷分析从首个错误状态和最小复现出发，先区分实现偏离已确认决定、决定前提被证伪和适用条件变化，再区分产品缺陷、测试缺陷、环境故障、契约冲突与证据不足；失败若证伪上游决定前提，质量结论须指出待重审决定、影响范围和仍有效边界，不以放宽断言、增加下游例外或只修症状换取表面通过。
- **权威依据**：`skills/quality-engineering/SKILL.md#执行协议`；`skills/quality-engineering/references/principles/criteria-risk-design.md#质量判据与可证伪性`；`skills/quality-engineering/references/principles/verification.md#缺陷归因与不稳定测试`；`skills/quality-engineering/references/memory/verification.md`
- **影响边界**：该守卫约束缺陷归因、回归设计和质量结论，不替代产品或架构 Owner 重作其专业决定，也不把尚未验证的根因推断写成质量事实。
- **复核入口**：以实现错误、错误决策、条件变化、契约冲突和证据不足五类相似故障检查归因能否区分，并确认错误决策场景不会通过修改测试或下游特例掩盖；缺陷分类或质量结论模型变化时重审。
