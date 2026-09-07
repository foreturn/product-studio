# 质量工程专业约束

## 能力索引

专业约束正文按簇分卷存放于 `references/principles/`，每簇汇聚数个专业类别的跨技术栈不变量。先依命中条件判定本次任务命中的簇（通常一至三簇），再完整读取命中簇文件；命中存疑时宁可加读相邻簇，不因漏判而缺约束；与本次工作无关的簇不读取。实施类任务进入证据评审与退出裁决时，加读“运行证据、归因与质量结论”卷。

| 能力簇 | 命中条件 | 正文 |
|---|---|---|
| 判据、风险与用例设计 | 制定质量判据与可证伪条件、评审验收对象、按风险覆盖分配验证投入、划定覆盖边界、设计用例与状态空间、编排拒绝超时重复等失败形态；质量判据、风险覆盖、输入边界、错误成功 | [criteria-risk-design.md](references/principles/criteria-risk-design.md) |
| 证据层级、隔离与自动化 | 选择证据层级与替身边界、搭建测试架构、治理夹具与测试数据、实现隔离与可重放等待、评审自动化失败的可诊断性；证据层级、测试架构、夹具、隔离复现、可诊断性 | [evidence-automation.md](references/principles/evidence-automation.md) |
| 契约、体验、性能与安全验证 | 验证接口契约与数据并发完整性、评审用户界面与无障碍行为、测量性能容量与可靠性、验证安全行为与有效边界；契约验证、数据迁移、并发交错、视觉一致性、性能基线、安全对照 | [specialized-verification.md](references/principles/specialized-verification.md) |
| 运行证据、归因与质量结论 | 评审运行证据与质量反馈、归因缺陷与不稳定测试、划定回归范围、作出退出裁决与最终质量结论；运行证据、缺陷归因、不稳定测试、回归范围、退出裁决 | [verification.md](references/principles/verification.md) |
