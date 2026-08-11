# backend 当前产品事实

## 后端实现职责

- **当前事实**：`backend` 依据产品与适用架构决定，通过领域建模与规则实现、API 与错误契约、数据建模与查询、迁移与数据演进、权限与安全、事务一致性与并发、集成与异步处理、性能与可观测性、后端测试与交付证据九项能力落实服务端行为；发现系统边界、数据所有权、共享不变量或质量约束冲突时退回 `architecture`，不在实现层建立第二套架构。
- **权威依据**：`skills/backend/SKILL.md#输入门禁`；`skills/backend/SKILL.md#实施流程`；`skills/backend/SKILL.md#边界`
- **影响边界**：服务端代码、数据库与迁移代码、API 调用方、`frontend` 接口输入以及 `verification` 的服务端验收证据。
- **复核入口**：以局部 API 实现和跨数据所有权两类全新请求试用 `backend`，核对前者直接实现并验证，后者在共享不变量未定时退回 `architecture`，且两者均不改写产品语义。

## 服务端事实记忆

- **当前事实**：`backend` 的 `references/memory.md` 只收录最终代码当前执行的领域、具体接口、数据、权限、事务并发、事件、缓存、集成和服务端运行事实；事实是否在本次被修改不影响收录，最终差异只用于定位变化与回归风险。系统边界、数据所有权、共享不变量与跨边界语义由 `architecture` 事实册保存。
- **权威依据**：`skills/backend/references/memory.md#收录门槛`；`skills/backend/SKILL.md#当前产品事实记忆`；`skills/architecture/references/memory.md#收录门槛`
- **影响边界**：目标产品的 `docs/product-studio/<product-id>/backend.md` 与 `docs/product-studio/<product-id>/architecture.md`、后续检索和终态事实同步；同一事实正文只由一个 Owner 保存。
- **复核入口**：在隔离样例中分别核验本次改动形成的事实与本次未触及但已由当前代码证实的既有事实，核对两者按同一门槛决定是否更新 `backend.md`；主题保持人类可读且只含当前事实、权威依据、影响边界和复核入口，不复制架构 Owner 的事实。
