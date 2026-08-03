# backend 当前代码事实

## 后端实现职责

- **当前事实**：`backend` 依据产品与适用架构契约实现领域规则、具体 API、Schema、权限、事务并发、缓存消息、外部集成、可观测性和服务端开发测试；发现系统边界、数据所有权、共享不变量或质量约束冲突时退回 `architecture`，不在实现层建立第二套架构。
- **代码定位**：`skills/backend/SKILL.md#输入门禁`；`skills/backend/SKILL.md#实施流程`；`skills/backend/SKILL.md#边界`
- **影响范围**：服务端代码、数据库与迁移代码、API 调用方、`frontend` 接口输入以及 `verification` 的服务端验收证据。
- **验证入口**：`python3 -X utf8 scripts/validate_project.py --self-test` 检查后端工程卷唯一加载、具体 API 职责、架构回退路径和后端越权承担系统架构的退化。

## 服务端事实记忆

- **当前事实**：`backend` 的 `references/memory.md` 只收录最终代码当前执行的领域、具体接口、数据、权限、事务并发、事件、缓存、集成和服务端运行事实；系统边界、数据所有权、共享不变量与跨边界语义由 `architecture` 事实册保存。
- **代码定位**：`skills/backend/references/memory.md#收录门槛`；`skills/backend/SKILL.md#当前代码事实记忆`；`skills/architecture/references/memory.md#收录门槛`
- **影响范围**：目标项目的 `docs/product-studio/backend.md` 与 `docs/product-studio/architecture.md`、后续检索和终态事实同步；同一事实正文只由一个 Owner 保存。
- **验证入口**：`python3 -X utf8 scripts/validate_project.py --self-test` 检查五份技能自有记忆卷、人类可读主题、四字段、代码定位、最终状态表述和跨 Owner 错链。
