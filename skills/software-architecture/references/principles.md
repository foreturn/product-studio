# 软件架构专业约束

## 能力索引

正文位于本索引同级的 `principles/` 目录，下表链接相对于本索引文件。按任务的实际变化、风险与依赖选择能力簇，完整读取命中分卷；命中存疑时加读相关相邻簇，发现新边界时补读，无关簇不加载。

| 能力簇 | 命中条件 | 正文 |
|---|---|---|
| 分解、内聚与代码组织 | 设计或评审系统分解与服务边界、模块内聚与依赖方向、目录结构与命名组织、能力复用与自研选型取舍 | [decomposition-cohesion.md](principles/decomposition-cohesion.md) |
| 契约与交互 | 划定语义解释与确定性执行责任边界、设计跨界契约及同步异步交互方式、约束端到端时间预算与部分失败语义 | [contracts-interactions.md](principles/contracts-interactions.md) |
| 数据与一致性 | 确定数据权威、复制与删除传播，定义读取一致性、跨界状态、重复乱序与补偿流程 | [data-consistency.md](principles/data-consistency.md) |
| 容量与运行拓扑 | 估算容量与性能约束、设计部署单元与运行拓扑、制定扩缩容策略与健康判断 | [capacity-topology.md](principles/capacity-topology.md) |
| 韧性与故障恢复 | 分析失效模式与传播、设计资源隔离和诚实降级、验证备份冗余与完整恢复路径 | [resilience-recovery.md](principles/resilience-recovery.md) |
| 信任边界与安全结构 | 划分信任边界、保持身份租户上下文、设置不可绕过的授权隔离并保护敏感数据生命周期 | [trust-security.md](principles/trust-security.md) |
| 可观测性与可运维性 | 设计业务结果与故障恢复信号、关联请求消息任务、约束观测成本，并评审修复操作与告警 | [observability-operations.md](principles/observability-operations.md) |
| 驱动因素与演进验证 | 明确架构驱动因素与质量场景、排序质量属性取舍、规划契约数据与事件演进迁移、记录或重审架构决定 | [drivers-evolution.md](principles/drivers-evolution.md) |
