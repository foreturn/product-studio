# 产品工作室

产品工作室是一套同时服务 Codex 与 Claude Code 的氛围编程插件。用户只需给出简短意图，插件便会先从仓库证据联想用户旅程、范围、约束与验收标准，再由职责清晰的产品研发角色推进实现，以减少过早编码、隐含假设和后期验收造成的返工。

扩写不是替用户虚构需求：仓库可查的信息自行查明，可逆细节记录假设后继续，只有会显著改变产品、安全、外部状态或不可逆数据的决策才请求确认。

## 工作流

端到端任务使用 `delivery`。它作为交付负责人，在过程阶段通过当前会话中的输入、证据与角色交接协调各专项角色；项目记忆不承担过程协调，只在任务终态、适用验证完成并形成可复核结论后，由各受影响角色增量合并本轮已经成立的事实变化：

```text
delivery
|-- discovery
|-- architecture（仅在存在重要架构决策时）
|-- frontend
|-- backend
|-- verification
`-- release（发布适用且获授权时）
```

各 Skill 的能力分工如下：

| Skill | 能力域 | 应具备的核心能力 |
|---|---|---|
| `delivery` | 产品交付 | 意图归类、价值切片、依赖协调、风险门禁、变更控制与交付收口 |
| `discovery` | 产品发现 | 问题定义、用户任务、证据联想、旅程状态、范围优先级与验收口径 |
| `architecture` | 系统架构 | 系统建模、跨边界契约、质量属性、一致性故障、安全边界与演进约束 |
| `frontend` | 前端体验 | 任务效率、交互、信息架构、响应式、视觉、可访问性、状态工程与渲染验收 |
| `backend` | 后端工程 | 领域模型、API、数据迁移、权限、并发一致性、集成可靠性与服务端验证 |
| `verification` | 独立验收 | 需求追溯、风险建模、分层测试、体验与数据验收、回归及证据审计 |
| `release` | 发布运行 | 发布策略、制品配置、迁移执行、健康判断、风险回滚、事故处置与反馈闭环 |

每个 `SKILL.md` 只负责触发、输入、授权、执行、产物、交接与边界，并通过“专业能力来源”直达自身 `references/`。能力手册以“能力目录—核心能力卡—能力组合—完成判据”组织专业判断：目录只负责选择能力，不代替正文；每张适用能力卡都须完整读取，并以“启用、输入、执行、裁决、产出、验证、完成、边界”保存可直接实施的专业规则、证据要求与失败反例。跨能力协作或收口时再读取组合与判据，专业正文不在主提示词重复维护。

## 调用方式

- 按需直调：用户可显式调用任一 `$skill-name`；单一职责只检查本角色最小输入，不强制经过完整生命周期。
- 编排调用：跨角色或高风险任务由 `delivery` 选择最小必要角色链路。
- 安全并行：上游门禁已通过、输入快照一致、依赖独立且文件或章节归属互不冲突时，多个 Skill 可同时推进。
- 串行收口：同一契约、Schema、迁移、组件或共享环境由固定责任角色合并；并行不得绕过验收或发布授权。

## 项目记忆

`skills/` 与其中的角色能力手册约束 AI 如何工作；`<当前项目根>/docs/product-studio/` 只保存各角色跨轮仍成立的项目事实。当前项目根界定事实归属，每个角色只拥有与 Skill 同名的事实文件。

跨角色的终态收口顺序、受影响角色识别和写入失败隔离由 `skills/delivery/SKILL.md` 的“项目记忆”定义；每个角色写入什么、凭何成立、使用哪些稳定 ID 及如何维护 schema，则由各自 `SKILL.md` 的“项目记忆”完整定义。不存在另行覆盖这些规则的根级共享记忆契约。

过程阶段不更新记忆。任务到达终态且适用验证完成后，仅事实发生变化的角色由各自拥有者增量更新同名文件；未受影响事实、章节、文件和时间戳保持不变，不作整卷覆盖。只读、中断、未终态、无事实增量或明确排除记忆时不写。

Skill、模板和项目记忆采用同一主干名：`skills/<skill>/SKILL.md` → `templates/<skill>.md` → `docs/product-studio/<skill>.md`。`templates/` 只用于首次创建 schema 2 角色事实册，保留事实家族索引与一张十三字段通用骨架；既有 schema 1 或 schema 2 记忆由对应角色依据本角色规则和已有事实卡增量维护，不再套用模板，格式迁移须另获明确授权。

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
