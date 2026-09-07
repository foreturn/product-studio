# 软件架构专业约束

## 能力索引

专业约束正文按簇分卷存放于 `references/principles/`，每簇汇聚数个专业类别的跨技术栈不变量。先依命中条件判定本次任务命中的簇（通常一至三簇），再完整读取命中簇文件；命中存疑时宁可加读相邻簇，不因漏判而缺约束；与本次工作无关的簇不读取。

| 能力簇 | 命中条件 | 正文 |
|---|---|---|
| 分解、内聚与代码组织 | 设计或评审系统分解与服务边界、模块内聚与依赖方向、目录结构与命名组织、能力复用与自研选型取舍 | [decomposition-cohesion.md](references/principles/decomposition-cohesion.md) |
| 契约、数据与一致性 | 划定语义解释与确定性执行责任边界、设计跨界契约与同步异步交互方式、确定数据权威与复制传播、定义一致性语义与跨界补偿流程 | [contracts-data.md](references/principles/contracts-data.md) |
| 容量、部署与故障恢复 | 估算容量与性能约束、设计部署单元与运行拓扑、制定扩缩容与隔离策略、设计故障恢复并验证备份冗余 | [capacity-resilience.md](references/principles/capacity-resilience.md) |
| 信任边界与可运维性 | 划分信任边界与安全控制、保护敏感数据全生命周期、设计观测信号与运行操作、评审告警与可运维性 | [security-operations.md](references/principles/security-operations.md) |
| 驱动因素与演进验证 | 明确架构驱动因素与质量场景、排序质量属性取舍、规划契约数据与事件演进迁移、记录或重审架构决定 | [drivers-evolution.md](references/principles/drivers-evolution.md) |
