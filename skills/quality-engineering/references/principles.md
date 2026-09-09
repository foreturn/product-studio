# 质量工程专业约束

## 能力索引

正文位于本索引同级的 `principles/` 目录，下表链接相对于本索引文件。按任务的实际变化、风险与依赖选择能力簇，完整读取命中分卷；命中存疑时加读相关相邻簇，发现新边界时补读，无关簇不加载。形成质量结论、评审运行证据与退出条件时，加读“运行证据、归因与质量结论”卷。

| 能力簇 | 命中条件 | 正文 |
|---|---|---|
| 判据、风险与用例设计 | 制定质量判据与可证伪条件、评审验收对象、按风险覆盖分配验证投入、划定覆盖边界、设计用例与状态空间、编排拒绝超时重复等失败形态；质量判据、风险覆盖、输入边界、错误成功 | [criteria-risk-design.md](principles/criteria-risk-design.md) |
| 证据层级、隔离与自动化 | 选择证据层级与替身边界、搭建测试架构、组织测试代码与公共助手、治理夹具与测试数据、实现隔离与可重放等待、评审自动化失败的可诊断性与证据复用范围 | [evidence-automation.md](principles/evidence-automation.md) |
| 契约与数据验证 | 验证接口结构语义、错误版本与消费者兼容，核对数据事务、幂等、迁移和并发交错完整性 | [contract-data-verification.md](principles/contract-data-verification.md) |
| 体验与无障碍验证 | 从真实入口验证用户任务、响应式与生命周期变化、语义焦点辅助操作、视觉一致性及失败恢复 | [experience-accessibility-verification.md](principles/experience-accessibility-verification.md) |
| 性能与可靠性验证 | 测量性能容量、资源饱和与系统拐点，验证故障降级、数据不变量、积压与恢复 | [performance-reliability-verification.md](principles/performance-reliability-verification.md) |
| 安全行为验证 | 验证身份授权与租户边界的允许拒绝对照，确认扫描候选、攻击可达性、控制生效和测试安全边界 | [security-verification.md](principles/security-verification.md) |
| 运行证据、归因与质量结论 | 评审运行证据与质量反馈、归因缺陷与不稳定测试、划定回归范围、作出退出裁决与最终质量结论；运行证据、缺陷归因、不稳定测试、回归范围、退出裁决 | [verification.md](principles/verification.md) |
