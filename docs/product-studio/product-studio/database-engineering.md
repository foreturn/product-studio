# database-engineering 当前产品事实

## 数据库工程裁决边界

- **当前事实**：`database-engineering` 唯一裁定物理 Schema、列类型与键约束、索引与执行计划、数据库事务隔离与锁、迁移回填机制、容量与生命周期、备份恢复及复制高可用；业务规则和应用兼容代码归后端，跨边界数据主权归架构，安全依据归安全工程，生产执行归发布工程。
- **权威依据**：`skills/database-engineering/SKILL.md#唯一决策权`；`skills/database-engineering/references/principles.md#能力索引`
- **影响边界**：ORM 模型、迁移生成成功和内存数据库测试不能替代目标数据库精确版本的 DDL、执行计划、并发、迁移或恢复证据；`quality-engineering` 对实现给出最终证明。
- **复核入口**：以 Schema 约束、慢查询、死锁、大表回填、代码回滚和备份恢复场景检查数据库 Owner 的判断、产出与证据，并确认生产 DDL 与切换只能由 `release-engineering` 在精确授权内执行。

## 数据库事实入口

- **当前事实**：当前已执行且会复用的物理关系、引擎约束、关键索引或分区、隔离锁不变量、迁移兼容条件、容量、生命周期和恢复机制进入 `docs/product-studio/<product-id>/database-engineering.md`；`database-engineering` 裁决语义，`fact-sync` 在质量通过后机械落盘。
- **权威依据**：`skills/database-engineering/SKILL.md#终态事实候选`；`skills/database-engineering/references/memory.md#共同定位与写入契约`
- **影响边界**：数据库事实须绑定目标引擎版本与可重复数据库证据；迁移进度、一次性执行记录、推测负载、未演练恢复、连接秘密和生产数据不得入册。
- **复核入口**：核对 Owner 裁决包包含 `product-id`、locator、目标数据库版本、四栏或删除依据及直接证据，并以质量失败、依据搬移、结构消失和无变化场景检查不提前写入与最小更新。
