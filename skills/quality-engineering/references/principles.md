# 质量工程专业约束

## 能力索引

专业约束正文按簇分卷存放于 `references/principles/`，每簇汇聚一至数个专业类别的跨技术栈不变量。先依命中条件判定本次任务命中的簇（通常一至四簇），再完整读取命中簇文件；命中存疑时宁可加读相邻簇，不因漏判而缺约束；与本次工作无关的簇不读取。实施类任务进入证据评审与退出裁决时，加读“运行证据、归因与质量结论”卷。

| 能力簇 | 命中条件 | 正文 |
|---|---|---|
| 判据、风险与用例设计 | 制定质量判据与可证伪条件、评审验收对象、按风险覆盖分配验证投入、划定覆盖边界、设计用例与状态空间、编排拒绝超时重复等失败形态；质量判据、风险覆盖、输入边界、错误成功 | [criteria-risk-design.md](references/principles/criteria-risk-design.md) |
| 证据层级、隔离与自动化 | 选择证据层级与替身边界、搭建测试架构、治理夹具与测试数据、实现隔离与可重放等待、评审自动化失败的可诊断性；证据层级、测试架构、夹具、隔离复现、可诊断性 | [evidence-automation.md](references/principles/evidence-automation.md) |
| 契约与数据验证 | 验证接口结构语义、错误版本与消费者兼容，核对数据事务、幂等、迁移和并发交错完整性 | [contract-data-verification.md](references/principles/contract-data-verification.md) |
| 体验与无障碍验证 | 从真实入口验证用户任务、响应式与生命周期变化、语义焦点辅助操作、视觉一致性及失败恢复 | [experience-accessibility-verification.md](references/principles/experience-accessibility-verification.md) |
| 性能与可靠性验证 | 测量性能容量、资源饱和与系统拐点，验证故障降级、数据不变量、积压与恢复 | [performance-reliability-verification.md](references/principles/performance-reliability-verification.md) |
| 安全行为验证 | 验证身份授权与租户边界的允许拒绝对照，确认扫描候选、攻击可达性、控制生效和测试安全边界 | [security-verification.md](references/principles/security-verification.md) |
| 运行证据、归因与质量结论 | 评审运行证据与质量反馈、归因缺陷与不稳定测试、划定回归范围、作出退出裁决与最终质量结论；运行证据、缺陷归因、不稳定测试、回归范围、退出裁决 | [verification.md](references/principles/verification.md) |
