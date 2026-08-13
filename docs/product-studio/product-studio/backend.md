# backend-engineering 当前产品事实

## 后端实现职责

- **当前事实**：`backend-engineering` 依据已确认的产品、体验与适用架构契约，实现领域状态与不变量、API 和错误语义、应用服务与事务编排、持久化适配、并发幂等、任务消息、外部集成、服务端安全控制、性能保护、可观测性和开发测试；它不裁定物理 Schema、索引、隔离锁、数据库迁移或安全政策。
- **权威依据**：`skills/backend-engineering/SKILL.md#输入与证据门槛`；`skills/backend-engineering/SKILL.md#实施方法`；`skills/backend-engineering/references/principles.md#核心能力`
- **影响边界**：服务端代码、API 调用方、数据库适配、异步消费者和运行诊断由本技能落实；跨边界语义、数据库物理机制与安全策略分别回到 `software-architecture`、`database-engineering` 和 `security-engineering`。
- **复核入口**：以局部 API 修复、跨服务一致性、Schema 迁移和租户越权四类场景检查直接实现、缺口暴露与越权停止；可写实现须取得风险相称的当前验证，形成终态后再按事实同步门禁处理候选裁决。

## 服务端事实稳定入口

- **当前事实**：`backend-engineering` 唯一裁决稳定 locator `docs/product-studio/<product-id>/backend.md` 中的领域、API、应用事务、事件、缓存、集成和服务端运行事实；它只形成四态语义裁决，事实文件由 `fact-sync` 在终态与质量门禁通过后机械更新。
- **权威依据**：`skills/backend-engineering/SKILL.md#当前产品事实`；`skills/backend-engineering/references/memory.md#产品定位与事实实例`
- **影响边界**：旧 `backend.md` 在外部项目中保持可达；数据库物理事实、安全政策、跨边界数据主权和质量能力不得复制到本册。
- **复核入口**：核对 `backend.md` locator、Owner 裁决包及 `fact-sync` 门禁；以权威实现搬移、API 行为变化、最后消费者删除和实际核验范围无变化检查 `UPDATE`、`DELETE` 与 `NO_CHANGE` 行为。
