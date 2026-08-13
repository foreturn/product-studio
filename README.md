# 产品工作室

产品工作室是一套面向 Codex 与 Claude Code 的软件工程专业技能插件。它不接管编码，也不要求先写一套庞大计划；Codex 仍是执行者，十项 Skill 只在命中的专业边界内约束判断、产出和证据，并在可交付终态后把值得复用的当前项目事实沉淀到目标仓库。

## 十项 Skill

| Skill | 唯一裁决与专业能力 |
|---|---|
| `product-management` | 裁定为何做、为谁做、做什么、做到何处和何谓成功；覆盖问题与机会、角色与利益相关者、价值结果链、业务政策与状态语义、范围优先级、风险假设、指标口径、验收非目标、发现实验及决定追溯。 |
| `product-experience` | 裁定用户如何理解并完成已确认的产品任务；覆盖现状诊断、端到端旅程、信息架构、动作模型、可见状态与恢复、表单内容、无障碍、响应式、设计系统适用性和可用性验证。 |
| `software-architecture` | 只在真实跨边界风险存在时，裁定系统上下文、边界职责、数据主权与共享不变量、跨边界交互、质量权衡、故障恢复、信任边界、可运行性、演进迁移和交付切片。 |
| `backend-engineering` | 实现领域状态与不变量、API 与错误契约、应用服务、持久化适配、事务编排、并发幂等、任务消息、外部集成、服务端权限落实、性能保护、可观测性和开发测试；不改写数据库物理策略或安全策略。 |
| `frontend-engineering` | 将已确认的产品体验落实为路由、页面、请求适配、客户端状态、组件、表单、视觉令牌、响应式、无障碍、安全和性能代码，并以真实浏览器、视口、输入方式、网络与控制台证据自检。 |
| `database-engineering` | 裁定并实现物理 Schema、约束与键、索引和执行计划、隔离级别与锁、迁移回填、数据生命周期、容量性能、备份恢复、复制高可用、访问审计及数据库维护证据。 |
| `security-engineering` | 裁定资产与数据分级、威胁模型、身份会话、授权策略、输入和 API 滥用防护、秘密与加密、隐私最小化、供应链、安全配置、监测响应及漏洞验证标准。 |
| `quality-engineering` | 独立决定如何证明结果成立；覆盖需求追溯、风险与退出条件、测试分层、夹具环境、API 权限数据、浏览器与无障碍、非功能、迁移兼容、缺陷归因和通过／失败／阻塞／不适用裁决。 |
| `release-engineering` | 分别裁定仓库准备、发布就绪、当前授权、实际执行和运行健康；覆盖版本与 Tag、发布说明、制品供应链、环境配置、迁移批次、灰度门禁、观察窗、停止回滚、事故恢复和发布反馈。 |
| `fact-sync` | 在实现、验收或发布形成经验证终态后，核定 Git 根、`product-id` 和受影响 Owner，收集 `ADD / UPDATE / DELETE / NO_CHANGE` 判定，检查唯一所有权、四栏结构、依据、秘密边界与空册清理；它不拥有或发明事实正文。 |

每项能力按三层分工组织：

- `SKILL.md` 回答“做什么、具体怎么做”，详细规定专业目标、输入与证据、操作方法、产物、完成标准、停止条件和权限边界。
- `references/principles.md` 回答“依据什么作专业判断”，只保存本专业的不变量、权衡方法、证据标准与常见误判，不规定其他 Skill 的调用、先后、退回或移交。
- `references/memory.md` 回答“本专业哪些当前事实值得跨上下文保留、每类事实具体如何记”。它按专业事实类型逐项规定入册条件、主题合并键、当前事实写法、权威依据、影响边界、复核入口、`ADD / UPDATE / DELETE / NO_CHANGE` 规则和专属禁项，不承担专业执行或技能编排。

`fact-sync` 是不拥有事实正文的机械同步能力，因此只有 `SKILL.md` 与专业同步准则，没有自己的 `memory.md` 或事实册。

## AI 自主选择

插件不提供中央 `router`，也不在任何专业 Skill 中预设固定技能链。各 Skill 的 frontmatter `description` 只声明自身适用问题；Codex 依据用户请求、当前仓库事实、实际风险和仍缺失的专业判断，自主决定加载哪些 Skill、以何种顺序工作以及何时停止。

专业所有权只用于守界，不构成路由指令。例如，“物理 Schema 不属于后端工程的裁决范围”只防止后端凭空改写数据库策略；是否需要加载数据库工程、是否需要并行工作以及何时取得该输入，均由 Codex 根据当前任务决定。缺少必要专业输入时，命中的 Skill 应说明缺口、影响和继续所需的契约，不替其他专业作决定，也不命令下一项 Skill。

一项任务可以只命中一个 Skill，也可以由 Codex 按证据需要组合多个 Skill；不得因为插件列出了十项能力便机械全部加载。无论采用何种组合，完成声明都必须有与风险相称的当前验证。发布和生产迁移仍须具备明确绑定当前仓库或制品、目标环境、范围、动作与有效时窗的授权；代码权限、验收通过、方案和旧授权均不构成生产授权。

## 当前项目事实

`skills/` 约束 AI 如何判断；`<Git仓库根>/docs/product-studio/<product-id>/` 保存各产品下一次工作真正需要的总结性当前事实。源码、权威 Schema、流水线、制品库和环境查询始终是权威，事实册只是跨上下文的语义索引，不能代替重新核验命中的权威来源。

`product-id` 必须在仓库内唯一、稳定且可安全作为单级目录名，并由用户范围、产品入口与元数据、相关项目根、目标代码和调用链共同确定，不从任一目录名机械推导。一个产品可以跨多个项目根；一个仓库也可以包含多个产品。归属无法唯一确定时，不读取、不写入、不创建候选事实目录。

为避免外部项目的既有事实静默失联，六个旧文件名作为稳定 locator 保留；Skill 改名不触发机械迁移：

| 事实 Owner | 稳定事实册 | 保存的当前事实 |
|---|---|---|
| `product-management` | `design.md` | 已实现的目标角色与结果、业务政策、范围、指标口径和产品层验收约束 |
| `product-experience` | `product-experience.md` | 已实现的旅程、信息架构、动作内容、可见状态恢复、响应式和无障碍体验 |
| `software-architecture` | `architecture.md` | 系统边界、数据主权、共享不变量、跨边界交互、质量权衡、故障恢复、信任与演进约束 |
| `backend-engineering` | `backend.md` | 领域与 API、应用事务、并发幂等、事件任务、缓存、集成及服务端运行行为 |
| `frontend-engineering` | `frontend.md` | 路由任务、共享组件、客户端状态、请求表单、响应式、无障碍及浏览器约束 |
| `database-engineering` | `database-engineering.md` | 物理 Schema、约束索引、隔离锁、迁移回填、生命周期、容量和恢复约束 |
| `security-engineering` | `security-engineering.md` | 资产分类、身份会话、授权租户、滥用防护、秘密密码学、隐私、供应链与漏洞处置 |
| `quality-engineering` | `verification.md` | 要求与风险覆盖、可重复检查、环境夹具、接口浏览器、非功能与回归守卫 |
| `release-engineering` | `release.md` | 版本制品、当前部署身份、环境契约、部署迁移、健康观察、停止恢复与分发兼容约束 |

每册都是本 Owner 对产品的累计当前事实视图，不是任务摘要、计划、变更日志或文件清单。各 Owner 先依本专业的事实类型规则判断是否入册、如何合并与何时增改删；真正写入的每个主题只含四栏：

```markdown
## <稳定事实主题>

- **当前事实**：<当前已证实的语义、条件和边界>
- **权威依据**：<一至三个仓库相对路径、Symbol、Schema、制品或环境证据入口>
- **影响边界**：<消费者、适用条件、不得破坏关系及明确不适用处>
- **复核入口**：<可重复检查方式、关键断言、未覆盖边界和重审触发>
```

当前事实记录遵守以下门禁：

- 每次可写实现、验收或发布形成可交付终态并取得相称验证后，必须执行事实同步检查。
- 只对本次实际核验范围内的事实逐 Owner 判定 `ADD`、`UPDATE`、`DELETE` 或 `NO_CHANGE`；局部核验不得宣称全项目新鲜。
- 只有事实确有新增、改变或消失时才修改事实册；`NO_CHANGE` 不触碰文件。
- 同一语义只由一个 Owner 保存并原位增改删；最后主题消失时删除空册，最后一册消失时删除空产品目录。
- 只收稳定、非显然、会复用且重查代价高的当前语义；计划、任务流水、diff、历史、单次结果、临时状态、授权、秘密、令牌、用户数据和可生成清单不入册。
- 只读任务未获事实册写入授权时只报告候选变化；验证失败、证据不足或尚未形成终态时报告 `DEFERRED`，不得落盘。

## 目录

```text
product-studio/
|-- skills/
|   |-- product-management/      # principles.md + memory.md -> design.md
|   |-- product-experience/      # principles.md + memory.md
|   |-- software-architecture/   # principles.md + memory.md -> architecture.md
|   |-- backend-engineering/     # principles.md + memory.md -> backend.md
|   |-- frontend-engineering/    # principles.md + memory.md -> frontend.md
|   |-- database-engineering/    # principles.md + memory.md
|   |-- security-engineering/    # principles.md + memory.md
|   |-- quality-engineering/     # principles.md + memory.md -> verification.md
|   |-- release-engineering/     # principles.md + memory.md -> release.md
|   `-- fact-sync/               # principles.md，无事实册
|-- docs/product-studio/
|   `-- <product-id>/            # 仓库内实际存在的当前事实子集
|-- .codex-plugin/plugin.json
|-- .claude-plugin/
`-- .agents/plugins/marketplace.json
```

## 安装

Codex：

```powershell
codex plugin marketplace add foreturn/product-studio
codex plugin add product-studio@foreturn
```

Claude Code：

```powershell
claude plugin marketplace add foreturn/product-studio
claude plugin install product-studio@foreturn
```

## 校验

```bash
claude plugin validate --strict .
```

双平台静态校验只能证明清单与目录结构合法，不能证明 Codex 会在真实任务中正确触发、守界、验证或同步事实。行为验收须在安装对应版本后的全新上下文中，以未显式点名 Skill 的正反向场景检查实际选择、专业越权、固定链依赖和零更新行为。
