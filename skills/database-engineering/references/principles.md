# 数据库工程专业约束

## 能力索引

专业约束正文按簇分卷存放于 `references/principles/`，每簇汇聚一至数个专业类别的跨引擎不变量。先依命中条件判定本次任务命中的簇（通常一至四簇），再完整读取命中簇文件；命中存疑时宁可加读相邻簇，不因漏判而缺约束；与本次工作无关的簇不读取。

| 能力簇 | 命中条件 | 正文 |
|---|---|---|
| 数据建模与标识 | 新建表结构或 Schema、定义字段类型与约束、设计主键与唯一标识、取舍规范化与冗余、制定派生值一致性与删除策略 | [modeling-identity.md](references/principles/modeling-identity.md) |
| 查询与性能 | 编写或优化查询、设计索引、解读执行计划，处理稳定分页、批量读取、数据倾斜与访问路径退化 | [query-performance.md](references/principles/query-performance.md) |
| 事务、并发与连接 | 划定事务边界与隔离级别、排查锁死与并发冲突、约束重试，调整连接池、会话清理与超时预算 | [transactions-connections.md](references/principles/transactions-connections.md) |
| 迁移与数据交换 | 执行结构变更、在线迁移与回填，切换读写格式，搭建同步导入管道、断点续传与跨系统对账 | [migration-exchange.md](references/principles/migration-exchange.md) |
| 分区、归档与生命周期 | 设计分区键、归档与保留策略，治理删除传播、引用完整性、恢复链和批量清理资源峰值 | [lifecycle-retention.md](references/principles/lifecycle-retention.md) |
| 复制、恢复与高可用 | 接入复制与读取路由、排查复制延迟与故障切换、制定备份与时间点恢复策略、执行恢复与高可用演练 | [replication-recovery.md](references/principles/replication-recovery.md) |
| 容量与运行维护 | 制定容量模型与性能基线、排查资源饱和与性能退化、规划统计清理压缩等维护任务与告警提前量 | [operations-capacity.md](references/principles/operations-capacity.md) |
| 访问与数据安全 | 分离数据库身份与最小权限、治理策略上下文、配置加密与密钥边界、脱敏生产数据并设计审计 | [access-security.md](references/principles/access-security.md) |
