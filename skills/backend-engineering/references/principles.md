# 后端工程专业约束

## 能力索引

正文位于本索引同级的 `principles/` 目录，下表链接相对于本索引文件。按任务的实际变化、风险与依赖选择能力簇，完整读取命中分卷；命中存疑时加读相关相邻簇，发现新边界时补读，无关簇不加载。设计或执行验证、评审检查结果与证据范围时，加读“测试与证据边界”卷。

| 能力簇 | 命中条件 | 正文 |
|---|---|---|
| 领域与结构 | 新建或调整领域模型、业务规则与状态流转、服务分层与模块边界、目录结构与命名、常量配置与计算副作用归属、抽取或复用通用能力、引入新依赖与适配层 | [domain-structure.md](principles/domain-structure.md) |
| 契约与校验 | 设计或调整 API 契约、错误语义与版本兼容、处理缺省空值与边界值校验、实现语义解释与确定性规则判断、划分身份租户权限等信任校验与规范化 | [contract-validation.md](principles/contract-validation.md) |
| 持久化与事务 | 实现或调整持久化模型、查询与批量访问，划定事务边界并编排本地状态与外部副作用 | [persistence-transactions.md](principles/persistence-transactions.md) |
| 并发与缓存 | 设计并发仲裁、幂等去重、锁与版本机制，约束重试预算、缓存身份、新鲜度与失效策略 | [concurrency-cache.md](principles/concurrency-cache.md) |
| 异步与外部集成 | 接入消息队列与后台任务、对接外部服务与回调，处理重复乱序、结果未知、重试限流熔断与降级 | [async-integration.md](principles/async-integration.md) |
| 运行资源与可观测性 | 评审性能与容量、设置资源保护，建设日志指标追踪、健康告警与审计 | [runtime-observability.md](principles/runtime-observability.md) |
| 测试与证据边界 | 制定测试策略、编写或评审测试、验证事务并发消息与集成语义、评审性能容量与验证结论证据 | [verification.md](principles/verification.md) |
