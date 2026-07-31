---
schema: 3
memory: design
scope: current-project-code
project_root: "."
updated_at: "2026-07-31T18:53:06+08:00"
---

# design 代码事实

## 当前代码事实

### design:system:boundary:skill-topology

- **当前实现**：插件仅注册 `router`、`design`、`backend`、`frontend`、`verification` 五个可调用 Skill；产品与系统设计是 `design` 的两种条件模式，`router` 只编排代码任务，不包含独立发布能力。实际生产部署、生产迁移及生产写操作属于本插件范围之外。
- **源码锚点**：`skills/router/SKILL.md#编码任务网关`；`skills/design/SKILL.md#产品与系统设计`；`skills/backend/SKILL.md#后端工程`；`skills/frontend/SKILL.md#前端工程与体验`；`skills/verification/SKILL.md#独立验证`；`README.md#五个 Skill`
- **关联与消费者**：双端插件清单加载整个 `skills/`；最小调用链与四份代码事实模板均以该集合为边界。
- **验证证据**：`scripts/validate_project.py` 比较技能目录的精确集合，并分别校验五份 Skill 的 frontmatter、引用和默认提示词。
- **重验条件**：技能目录、Skill 名称、设计模式、router 的代码任务边界或插件清单的 skills 入口变化。

### design:system:contract:router-specialists

- **当前实现**：边界清楚的单一前端或后端任务直接进入对应实现技能并交给 `verification`，常规终端验证不触发 `router`；模糊全栈任务先由 `design` 串行完成产品与系统模式，再由 `backend` 或实际契约拥有者冻结具体 API 字段、错误、权限、异步状态、分页与版本，满足契约定版、快照一致、无硬依赖、写集合隔离、共享文件唯一写入和独立可验后，前后端方可并行。生产部署、生产迁移与生产写操作不进入五技能调用链。
- **源码锚点**：`skills/router/SKILL.md#直达与触发`；`skills/router/SKILL.md#最小调用链`；`skills/router/SKILL.md#编排规则`；`skills/design/SKILL.md#启用判定`；`README.md#路由`
- **关联与消费者**：`backend`、`frontend`、`verification` 的输入门禁与交接边界；项目既有的环境专属工具或运行责任人只接收已经验收的代码结果，不由本插件编排。
- **验证证据**：`scripts/validate_project.py` 检查 `router` 能路由四个专项、常规终端验证不被误算为跨领域、模糊全栈保留具体 API 契约里程碑、`design` 分离两种模式，且旧四个 callable 名称不再出现在活跃提示词中；负向自检分别移除两条路由约束并确认门禁拒绝。
- **重验条件**：专项直达规则、最小技能链、并行条件、设计触发条件或外部操作范围边界变化。

### design:system:invariant:memory-single-owner

- **当前实现**：`router` 不持久化项目记忆；`design`、`backend`、`frontend`、`verification` 只维护自己的 schema 3 当前代码事实。事实按完整语义键原位更新、新增或删除，固定包含当前实现、源码锚点、关联与消费者、验证证据、重验条件，历史由 Git 承担。
- **源码锚点**：`templates/design.md#当前代码事实`；`templates/backend.md#当前代码事实`；`templates/frontend.md#当前代码事实`；`templates/verification.md#当前代码事实`；`README.md#当前代码事实`
- **关联与消费者**：四个专业 Skill 的项目记忆章节；`scripts/validate_project.py` 的模板、实例、唯一键与 Owner 校验。
- **验证证据**：`scripts/validate_project.py` 拒绝 router 记忆、非 Owner 文件、重复或越权语义键、五字段缺失、模板残留及过程／历史字段。
- **重验条件**：记忆 Owner、schema、语义键家族、事实字段、增删改规则、模板用途或 Git 历史边界变化。

### design:system:invariant:capability-executable-detail

- **当前实现**：五个 Skill 共加载六份专业能力 reference，正文逐字恢复自 Git 节点 `9efef58ddb3f3a4bebcf856f6c2eef7ca7a53194`：`router` 使用原交付编排卷，`design` 按产品模式和系统模式分别使用原产品设计卷与系统架构卷，后端、前端、验证各使用本领域原卷。六卷均保持目录、角色职责、核心能力、专业决策顺序、交付证据、常见误判六章及 45 项核心能力；reference 不保存触发、路由、记忆或外部操作规则。
- **源码锚点**：`skills/router/references/delivery-capabilities.md#核心能力`；`skills/design/references/product-design-principles.md#核心能力`；`skills/design/references/architecture-principles.md#核心能力`；`skills/backend/references/backend-design-principles.md#核心能力`；`skills/frontend/references/frontend-design-principles.md#核心能力`；`skills/verification/references/verification-principles.md#核心能力`
- **关联与消费者**：五份 `SKILL.md` 的条件加载规则与 `scripts/validate_project.py#validate_reference` 的来源哈希、章节、能力集合及正文深度门禁。
- **验证证据**：六个工作树 Git blob 与该节点对应原文件逐一相等；`scripts/validate_project.py#validate_reference` 另以规范化 SHA-256、六章精确顺序、45 项核心能力名称及每项最低正文深度复核，并通过篡改原文的负向用例证明门禁有效。
- **重验条件**：来源节点、reference 路径或内容、能力名称、六章结构、模式加载方式或哈希门禁发生变化。
