# 后端工程专业约束

## 能力索引

专业约束正文按簇分卷存放于 `references/principles/`，每簇汇聚一至数个专业类别的跨技术栈不变量。先依命中条件判定本次任务命中的簇（通常一至四簇），再完整读取命中簇文件；命中存疑时宁可加读相邻簇，不因漏判而缺约束；与本次工作无关的簇不读取。实施类任务完成实现进入验证时，加读“测试与证据边界”卷。

| 能力簇 | 命中条件 | 正文 |
|---|---|---|
| 领域与结构 | 新建或调整领域模型、业务规则与状态流转、服务分层与模块边界、目录结构与命名、抽取或复用通用能力、引入新依赖与适配层 | [domain-structure.md](references/principles/domain-structure.md) |
| 契约与校验 | 设计或调整 API 契约、错误语义与版本兼容、处理缺省空值与边界值校验、实现语义解释与确定性规则判断、划分身份租户权限等信任校验与规范化 | [contract-validation.md](references/principles/contract-validation.md) |
| 持久化与事务 | 实现或调整持久化模型、查询与批量访问，划定事务边界并编排本地状态与外部副作用 | [persistence-transactions.md](references/principles/persistence-transactions.md) |
| 并发与缓存 | 设计并发仲裁、幂等去重、锁与版本机制，约束重试预算、缓存身份、新鲜度与失效策略 | [concurrency-cache.md](references/principles/concurrency-cache.md) |
| 异步与外部集成 | 接入消息队列与后台任务、对接外部服务与回调，处理重复乱序、结果未知、重试限流熔断与降级 | [async-integration.md](references/principles/async-integration.md) |
| 运行资源与可观测性 | 评审性能与容量、设置资源保护，建设日志指标追踪、健康告警与审计 | [runtime-observability.md](references/principles/runtime-observability.md) |
| 测试与证据边界 | 制定测试策略、编写或评审测试、验证事务并发消息与集成语义、评审性能容量与验证结论证据 | [verification.md](references/principles/verification.md) |
