# backend 当前代码事实

## 后端实现职责

- **当前事实**：`backend` 依据产品与适用架构契约实现领域规则、具体 API、Schema、权限、事务并发、缓存消息、外部集成、可观测性和服务端开发测试；发现系统边界、数据所有权、共享不变量或质量约束冲突时退回 `architecture`，不在实现层建立第二套架构。
- **代码定位**：`skills/backend/SKILL.md#输入门禁`；`skills/backend/SKILL.md#实施流程`；`skills/backend/SKILL.md#边界`
- **影响范围**：服务端代码、数据库与迁移代码、API 调用方、`frontend` 接口输入以及 `verification` 的服务端验收证据。
- **验证入口**：以局部 API 实现和跨数据所有权两类全新请求试用 `backend`，核对前者直接实现并验证，后者在共享不变量未定时退回 `architecture`，且两者均不改写产品语义。

## 服务端事实记忆

- **当前事实**：`backend` 的 `references/memory.md` 只收录最终代码当前执行的领域、具体接口、数据、权限、事务并发、事件、缓存、集成和服务端运行事实；系统边界、数据所有权、共享不变量与跨边界语义由 `architecture` 事实册保存。
- **代码定位**：`skills/backend/references/memory.md#收录门槛`；`skills/backend/SKILL.md#当前代码事实记忆`；`skills/architecture/references/memory.md#收录门槛`
- **影响范围**：目标项目的 `docs/product-studio/backend.md` 与 `docs/product-studio/architecture.md`、后续检索和终态事实同步；同一事实正文只由一个 Owner 保存。
- **验证入口**：在隔离样例中执行一次后端编码收口，核对只在最终代码事实确有变化时更新 `backend.md`，主题保持人类可读且只含当前事实、代码定位、影响范围和验证入口，不复制架构 Owner 的事实。
