# 数据库工程专业约束

## 能力索引

专业约束正文按簇分卷存放于 `references/principles/`，每簇汇聚数个专业类别的跨引擎不变量。先依命中条件判定本次任务命中的簇（通常一至三簇），再完整读取命中簇文件；命中存疑时宁可加读相邻簇，不因漏判而缺约束；与本次工作无关的簇不读取。

| 能力簇 | 命中条件 | 正文 |
|---|---|---|
| 数据建模与标识 | 新建表结构或 Schema、定义字段类型与约束、设计主键与唯一标识、取舍规范化与冗余、制定派生值一致性与删除策略 | [modeling-identity.md](references/principles/modeling-identity.md) |
| 查询、事务与连接治理 | 编写或优化查询、设计索引与解读执行计划、处理分页与批量读取、划定事务边界与隔离级别、排查死锁与并发冲突、调整连接池与会话超时 | [query-concurrency.md](references/principles/query-concurrency.md) |
| 迁移、生命周期与数据交换 | 执行结构变更与在线迁移、回填与切换读写格式、设计分区键与归档保留策略、搭建同步导入管道与断点续传、跨系统对账 | [migration-lifecycle.md](references/principles/migration-lifecycle.md) |
| 复制、恢复与高可用 | 接入复制与读取路由、排查复制延迟与故障切换、制定备份与时间点恢复策略、执行恢复与高可用演练 | [replication-recovery.md](references/principles/replication-recovery.md) |
| 运行治理与数据安全 | 制定容量模型与性能基线、排查资源饱和与性能退化、规划维护任务与告警提前量、分离数据库身份与最小权限、配置加密与密钥边界、脱敏生产数据与设计审计 | [operations-security.md](references/principles/operations-security.md) |
