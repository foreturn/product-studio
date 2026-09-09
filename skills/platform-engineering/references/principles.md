# 平台工程专业约束

## 能力索引

正文位于本索引同级的 `principles/` 目录，下表链接相对于本索引文件。按任务的实际变化、风险与依赖选择能力簇，完整读取命中分卷；命中存疑时加读相关相邻簇，发现新边界时补读，无关簇不加载。

| 能力簇 | 命中条件 | 正文 |
|---|---|---|
| 基础设施即代码与环境治理 | 编写或重构 IaC 模块与操作脚本、划分声明和配置归属、评审模块复用、在流水线中执行基础设施变更、治理状态与漂移、评审变更计划与破坏性影响、规划环境分层与配置一致性、归因成本与验证基础设施声明 | [iac-environments.md](principles/iac-environments.md) |
| 工作负载与调度治理 | 新建或迁移容器化工作负载、选择运行形态、设定资源请求限制与健康探针、设计滚动更新与排空回退、编排定时任务与副本分布 | [workload-scheduling.md](principles/workload-scheduling.md) |
| 持续集成执行域 | 设计或评审 CI 任务的触发、信任域、身份与秘密隔离，治理工作区和缓存污染，约束上传下载与重复执行的通道语义 | [ci-execution.md](principles/ci-execution.md) |
| 网络分段与流量治理 | 规划网段与分段策略、排查连通性与返回路径、设计 DNS 与服务命名、配置入口路由与传输证书、统一超时重试与排空预算 | [network-traffic.md](principles/network-traffic.md) |
| 配置、秘密与工作负载身份 | 接入配置与秘密存储、设计工作负载身份与最小权限、治理配置原子更新及凭据轮换撤销 | [config-secrets.md](principles/config-secrets.md) |
| 存储、耐久性与生命周期 | 选择存储形态与一致性耐久语义，管理创建扩容、迁移快照、保留分层与销毁 | [storage-lifecycle.md](principles/storage-lifecycle.md) |
| 可观测性与告警工程 | 建设日志指标与分布式追踪、设计遥测结构与采样、定义 SLI 与 SLO、编写告警规则与分页策略 | [observability-alerting.md](principles/observability-alerting.md) |
| 弹性、韧性与事故响应 | 制定容量模型与伸缩策略、设计限流降级与隔舱、规划故障域与灾难恢复、执行故障演练、指挥可用性事故处置与复盘 | [resilience-incident.md](principles/resilience-incident.md) |
