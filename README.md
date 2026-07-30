# 产品工作室

产品工作室是一套同时服务 Codex 与 Claude Code 的氛围编程插件。用户只需给出简短意图，插件便会先从仓库证据联想用户旅程、范围、约束与验收标准，再由职责清晰的产品研发角色推进实现，以减少过早编码、隐含假设和后期验收造成的返工。

扩写不是替用户虚构需求：仓库可查的信息自行查明，可逆细节记录假设后继续，只有会显著改变产品、安全、外部状态或不可逆数据的决策才请求确认。

## 工作流

端到端任务使用 `delivery`。它作为交付负责人，通过持久化产物协调各专项角色，不依赖对话历史独自传递决策：

```text
delivery
|-- discovery
|-- architecture（仅在存在重要架构决策时）
|-- frontend
|-- backend
|-- verification
`-- release（发布适用且获授权时）
```

角色职责如下：

| Skill | 角色 | 主责 |
|---|---|---|
| `delivery` | 交付负责人 | 接入、路由、阶段门禁、变更控制与最终收口 |
| `discovery` | 产品经理 | 短提示词扩写、用户价值、范围、假设与验收标准 |
| `architecture` | 架构师 | 模块边界、跨域不变量、迁移回滚与关键权衡 |
| `frontend` | 前端与体验负责人 | 用户可见流程、交互状态、实现与真实渲染证据 |
| `backend` | 后端负责人 | API、数据、权限、一致性、兼容与恢复 |
| `verification` | 验收负责人 | 要求追溯、核心旅程、失败路径、回归与交付结论 |
| `release` | 发布与运行负责人 | 发布授权、制品追溯、迁移回滚、上线验证与反馈回流 |

每个 `SKILL.md` 负责角色触发、输入、授权、执行、产物、交接与边界，并通过“专业能力来源”直接引用自身 `references/`。角色职责、核心能力、专业决策顺序、交付证据与常见误判只在对应能力手册中详细定义，按需载入而不与主提示词重复。前端手册覆盖易用性、交互、布局、视觉、可访问性、状态工程和真实渲染；其余六职也各自拥有可直接指导判断与实施的领域能力模型。

## 调用方式

- 按需直调：用户可显式调用任一 `$skill-name`；单一职责只检查本角色最小输入，不强制经过完整生命周期。
- 编排调用：跨角色或高风险任务由 `delivery` 选择最小必要角色链路。
- 安全并行：上游门禁已通过、输入快照一致、依赖独立且文件或章节归属互不冲突时，多个 Skill 可同时推进。
- 串行收口：同一契约、Schema、迁移、组件或共享环境由固定责任角色合并；并行不得绕过验收或发布授权。

## 项目记忆

`skills/`、角色参考资料与模板是可跨项目复用的专业能力；角色按授权写入 `<当前项目根>/docs/product-studio/` 的文档才是项目记忆。当前项目根是事实归属与持久化隔离键，产品名称只留作文档元数据，不再增加目录层级；不同仓库中的同名目录分别描述各自项目。

项目记忆是当前项目事实基线，不是信息访问白名单。用户显式提供的链接、页面、截图、设计稿、文档或其他项目材料可作为外部参考进入分析、比较与仿照；AI 记录其来源、用途和适用性。外部参考不会自动成为当前项目事实，得到当前用户确认、仓库实现、权威契约或本项目验证支持后，才形成当前决定或结论。

当前用户指令与当前仓库事实优先于旧记忆。只读任务不授权写入项目记忆，项目记忆保存安全引用而非凭据或其他秘密。每个角色完整拥有与 Skill 同名的 `<skill>.md`，交付负责人以 `delivery.md` 保存阶段、角色链、切片、风险、变更、阻塞与下一步，并通过稳定 ID 引用专项契约。完整规则见 `references/project-memory.md`。

每次获准的氛围编程完成前执行动态记忆收口：所有参与或受影响角色按当前差异与验证更新自己的文件；未受影响角色保持正文不变，只在已有 `delivery.md` 中标记“已复核、无变化”。记忆收口是完成结论的一部分。

产物按需写入当前项目的记忆目录。没有下游消费者的文档不会为了形式完整而创建。

Skill、模板和项目记忆采用同一主干名：`skills/<skill>/SKILL.md` → `templates/<skill>.md` → `docs/product-studio/<skill>.md`。模板面向 AI 恢复而设计，统一记录源码修订、恢复摘要、稳定 ID、精确依据、动作队列、当前验证和失效条件；不适用角色只保存原因与重新适用条件，不铺空表。

## 目录结构

```text
product-studio/
|-- .agents/plugins/marketplace.json
|-- .codex-plugin/plugin.json
|-- .claude-plugin/
|   |-- marketplace.json
|   `-- plugin.json
|-- skills/
|   |-- delivery/
|   |-- discovery/
|   |-- architecture/
|   |-- frontend/
|   |-- backend/
|   |-- verification/
|   `-- release/
|-- templates/
|-- references/
|   |-- platform-compatibility.md
|   `-- project-memory.md
|-- scripts/validate_project.py
|-- docs/product-studio/
`-- assets/
```

## 安装

### Codex

从 GitHub 向 Codex 注册 marketplace，再安装其中的插件：

```powershell
codex plugin marketplace add foreturn/product-studio
codex plugin add product-studio@foreturn
```

第一条命令只注册 marketplace；第二条命令才会安装 `product-studio`。仓库更新后，可运行 `codex plugin marketplace upgrade foreturn` 刷新 marketplace，再按 Codex 提示升级插件。

### Claude Code

Claude Code 使用独立的 marketplace 清单与安装命令：

```powershell
claude plugin marketplace add foreturn/product-studio
claude plugin install product-studio@foreturn
```

## 校验

运行项目检查：

```powershell
python scripts/validate_project.py
```

Codex 插件使用内置 `plugin-creator` 校验器。Claude Code 同时严格校验插件与 marketplace 清单：

```powershell
claude plugin validate --strict C:\Users\root\plugins\product-studio
```
