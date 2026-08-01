---
schema: 4
memory: design
scope: current-project-code
project_root: "."
updated_at: "2026-08-01T08:39:25+08:00"
---

# design 代码事实

## 当前代码事实

### design:boundary:skill-topology

- **事实摘要**：插件只注册 `router`、`design`、`backend`、`frontend`、`verification` 五个可调用 Skill；产品与系统设计是 `design` 的条件模式，生产部署、迁移和其他生产写操作位于插件边界之外。
- **代码定位**：`skills/router/SKILL.md#编码任务网关`；`skills/design/SKILL.md#产品与系统设计`；`README.md#五个 Skill`
- **依赖与影响**：双端插件清单、最小调用链、四份事实模板、`design:contract:router-specialists` 与 `design:invariant:summary-memory` 均依赖该拓扑。
- **验证入口**：`python3 -X utf8 scripts/validate_project.py --self-test` 检查技能目录精确集合、Skill frontmatter、旧 callable 清除及第六技能负向退化；不证明真实自动触发行为。
- **失效条件**：技能目录、Skill 名称、`design` 模式、生产操作边界或插件清单的 skills 入口变化。

### design:contract:router-specialists

- **事实摘要**：边界清楚的单一实现任务直达专项 Skill，契约清晰的全栈任务由 `router` 编排后端与前端并以 `verification` 收口；只有产品语义或系统边界未定时才插入 `design`，共享 API 由实际契约 Owner 先冻结。
- **代码定位**：`skills/router/SKILL.md#直达与触发`；`skills/router/SKILL.md#最小调用链`；`skills/router/SKILL.md#编排规则`
- **依赖与影响**：`backend`、`frontend`、`verification` 的输入门禁及 `design:boundary:skill-topology`；错误路由会增加无消费者设计或令前后端各自猜测共享契约。
- **验证入口**：`python3 -X utf8 scripts/validate_project.py --self-test` 检查常规终端验证不触发 router、全栈保留 API 契约里程碑及对应负向退化；真实选链仍需全新上下文试用。
- **失效条件**：专项直达规则、跨领域触发条件、API 契约 Owner、并行条件、设计启用判定或终态门禁变化。

### design:invariant:summary-memory

- **事实摘要**：`design`、`backend`、`frontend`、`verification` 各自维护 schema 4 总结性当前代码事实，稳定键统一为 `owner:type:slug`；每次成功编码终态都检查受影响卡片，但仅五字段变化时落盘，`router` 不拥有事实册。
- **代码定位**：`references/project-memory.md#Schema 4`；`references/project-memory.md#终态同步`；`skills/router/SKILL.md#终态收口`
- **依赖与影响**：四个专业 Skill、四份模板、目标项目的 `docs/product-studio/*.md` 与 `verification:check:plugin-static-contract`；跨 Owner 事实通过依赖键链接而不复制正文。
- **验证入口**：`python3 -X utf8 scripts/validate_project.py --self-test` 检查共享契约、Owner、schema、稳定键、五字段、代码定位、跨卡链接、模板骨架和过程记忆负向退化。
- **失效条件**：共享记忆契约、Owner、事实类型、字段、终态同步规则、模板、实例校验或 router 记忆所有权变化。

### design:invariant:capability-layering

- **事实摘要**：五个 Skill 各加载一份策展后的专业能力卷；`design` 产品模式使用主 Skill 内的下游契约，系统模式加载架构卷，能力 reference 不承载触发、路由或项目记忆规则。
- **代码定位**：`skills/router/references/delivery-capabilities.md#核心能力`；`skills/design/SKILL.md#条件加载专业能力`；`scripts/validate_project.py#validate_reference`
- **依赖与影响**：五份 `SKILL.md` 的条件加载、专业判断深度及项目校验；共享项目记忆规则仅来自 `references/project-memory.md`。
- **验证入口**：`python3 -X utf8 scripts/validate_project.py --self-test` 检查每个 Skill 的精确 reference 集合、策展哈希、四章结构、能力卡名称与最低正文深度；不能证明模型必然正确应用能力卡。
- **失效条件**：reference 路径或内容、能力名称、章节结构、产品模式契约、加载方式或共享记忆边界变化。
