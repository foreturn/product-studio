# 产品工作室

产品工作室是一套面向 Codex 与 Claude Code 的软件工程专业技能插件。编码代理仍直接理解请求、阅读仓库、编写代码并自主决定需要哪些专业判断；插件以十一项 Skill 提供清晰的专业所有权、实施准则与证据约束，并在可写回合结束前由终态 Hook 检查当前项目事实是否得到处置。

它不提供中央路由，不要求预先写成套计划，也不规定固定技能链。一个任务可以只使用一项 Skill，也可以按证据需要组合多项；未命中的专业内容不会被机械加载。

## 十一项通用底座

| Skill | 唯一专业边界 |
|---|---|
| `product-management` | 产品问题、用户与利益相关者、结果价值、业务资格与产品结果政策、状态语义、范围优先级、指标验收，以及旅程、信息架构、内容、动作反馈、恢复、响应式、无障碍、可用性、视觉层级与设计系统语义。 |
| `software-architecture` | 系统上下文、跨模块与跨服务职责、系统与部署边界、数据主权、跨边界交互、质量属性权衡、故障恢复、可运行性和演进约束。 |
| `backend-engineering` | 领域与应用服务、API 和错误、事务一致性、并发幂等、持久化适配、缓存、事件任务、外部集成、服务端性能和可观测实现。 |
| `web-engineering` | 浏览器运行时、路由、DOM 与 CSS、客户端状态、网络交互、表单、响应式、Web 无障碍、本地化与双向文本、兼容、安全和性能实现。 |
| `android-engineering` | Android 生命周期与进程恢复、Compose/View、导航与深链、离线数据、后台工作、权限、存储网络、本地化与双向文本、性能、兼容和平台测试。 |
| `ios-engineering` | iOS 生命周期与状态恢复、SwiftUI/UIKit、导航与 Universal Links、网络 API、并发、持久化、后台能力、隐私权限、Keychain、本地化与双向文本、性能和平台测试。 |
| `database-engineering` | 服务端、共享或独立运营数据库的物理 Schema、键与约束、索引和执行计划、事务隔离与锁、迁移回填、生命周期容量、备份恢复、复制和高可用；客户端私有本地库归对应端。 |
| `platform-engineering` | 环境与账户、IaC 和状态、网络 DNS、计算容器、编排、运行配置注入、CI 运行平台、观测平台、容量弹性、恢复、纯可用性事故治理、成本与漂移。 |
| `security-engineering` | 资产与威胁、身份会话、授权强制与租户隔离、API 滥用、秘密密码学、隐私、供应链、安全配置、安全事故响应与取证、漏洞处置。 |
| `quality-engineering` | 独立验收对象、风险覆盖、测试架构、环境夹具、功能与数据、用户界面与无障碍、非功能证据、缺陷归因和退出裁决。 |
| `release-engineering` | 发布对象、版本 Tag、不可变制品、环境就绪、兼容迁移、部署切流、健康观察、停止恢复、分发映射和操作授权。 |

产品管理同时拥有产品意图与产品体验语义。产品政策回答“允许谁在何条件下得到何种结果”；体验契约回答“用户从何处进入、如何理解与完成、怎样看到状态并从失败中恢复”。二者在同一专业内保持对象级分界，避免两套相反裁决。

产品中的业务资格与预期结果不等于安全授权强制：前者由产品管理裁定，后者由安全工程把已确认政策绑定可信主体、对象、租户和不可绕过的决策点。客户端私有本地库也不等于共享数据库运行面；Room、IndexedDB、SwiftData 或 Core Data 随客户端版本交付时归对应客户端专业，具有共享消费者或独立运维生命周期时才归数据库工程。

这十一项是面向应用型产品软件的通用底座，不把所有条件领域硬塞给相邻 Owner。ETL/ELT、数仓湖仓、批流计算、血缘与分析数据质量，机器学习系统，以及硬件或嵌入式等专门领域，应在项目真实需要时以同样三层契约增设条件 Skill；未增设前保持为显式未覆盖，不由后端、数据库或平台越权代裁。

## 三层文件契约

每项 Skill 使用完全相同的文件布局，但三类文件各有自己的统一格式：

- `SKILL.md` 的中文 `description` 只作专业发现摘要；正文统一保留目标、六步执行、输出、完成、停止、权限、参考和终态八章。它不列适用、不适用或必需输入清单，不展开领域方法，也不编排其他 Skill。
- `references/principles.md` 是通用专业约束正文。正文按八至十六个专业大类组织，每类只列四至八条跨框架仍成立的不变量、取舍标准或禁止边界；不设置字段，不固化特定库、算法、架构模板、阈值或操作步骤。
- `references/memory.md` 只规定本 Owner 记住哪些当前项目事实以及具体如何记。每卷收敛为五至九类终态语义，每类固定描述入册条件、主题合并键、当前事实写法、权威依据、影响边界、复核入口、变更规则和排除项。
- `agents/openai.yaml` 只提供界面元数据和显式调用示例。

专业所有权用于防止越界，不构成调用关系。遇到输入矛盾或缺失时，当前专业只说明缺口、影响和停止范围；编码代理依据当前任务自行决定怎样取得所需判断。

## 当前项目事实

目标仓库的事实册位于：

```text
<Git-root>/docs/product-studio/<product-id>/<owner>.md
```

`product-id` 必须由用户范围、产品入口与元数据、相关项目根、目标代码和调用链共同确定，在仓库内唯一、稳定且可作为安全的单级目录名。一个产品可以跨项目根，一个仓库也可包含多个产品；归属不唯一时不创建候选目录。

十一位 Owner 的稳定 locator 与 Skill 名一致：

| Owner | 事实册 |
|---|---|
| `product-management` | `product-management.md` |
| `software-architecture` | `software-architecture.md` |
| `backend-engineering` | `backend-engineering.md` |
| `web-engineering` | `web-engineering.md` |
| `android-engineering` | `android-engineering.md` |
| `ios-engineering` | `ios-engineering.md` |
| `database-engineering` | `database-engineering.md` |
| `platform-engineering` | `platform-engineering.md` |
| `security-engineering` | `security-engineering.md` |
| `quality-engineering` | `quality-engineering.md` |
| `release-engineering` | `release-engineering.md` |

事实册是语义索引，不是第二份源码。代码、权威 Schema、流水线、制品库和当前环境查询始终是真相来源。候选必须同时满足：当前可交付终态已经成立、跨局部改动仍稳定、并非从单一入口显然可得、会改变后续专业判断、重新发现成本高、具有唯一 Owner、能够沿当前权威入口复核且适合安全留存。任一门禁不成立便只留在本轮报告；源码或配置摘要、计划、目标态、迁移进度、运行快照、任务流水、历史、原始差异、一次测试结果、授权、秘密、令牌、用户数据和可生成清单均不入册。

长期兼容窗口只记当前仍受支持的版本组合、不变量、消费者与退出触发，不记阶段计划、完成比例、回填游标或未来目标蓝图。质量事实只保存权威契约与证据之间的稳定覆盖关系，不复制被验证契约正文；发布事实只保存稳定身份、门禁、兼容与恢复契约，不保存当前版本、digest、实例、流量、健康值或 rollout 状态。

每个事实以稳定语义与主题合并键组织，不规定统一 Markdown 标题、四栏标签、顺序或句数。正文可依事实类型与检索需要使用段落、列表、表格或局部小节；但必须能够辨认当前成立的语义、权威依据、适用或影响边界、复核方式与失效触发。同一主题只容纳共同检索、共同变化的稳定事实，不用空栏或占位符凑格式。

每次实现形成可交付终态并取得相称验证后，必须执行事实同步检查。每个受影响 Owner 先读取所有权、索引、通用门禁、动作与安全规则，再只展开本轮命中的事实类型和既有主题，并沿权威入口重新取证；只有通过全部门禁的事实确有新增、改变或消失时才修改事实册。事实动作只有 `ADD`、`UPDATE`、`DELETE`、`NO_CHANGE`，其中 `NO_CHANGE` 必须保持事实文件字节不变。

## 终态 Hook

插件通过默认路径 `hooks/hooks.json` 注册四类事件：

- `UserPromptSubmit` 记录当前 Git 仓库和事实册基线。
- `PreToolUse` 与 `PostToolUse` 以 `session + turn + tool_use_id` 配对，记录输入摘要、命令哈希、可解析退出状态和仓库前后指纹。
- `Stop` 比较终态与仓库事件账本，并核验是否存在绑定当前会话、观测验证、产品、Owner 和事实册路径的终态回执。

只读回合且没有观测到本轮变化时自动放行。仓库变化但没有匹配回执时，Hook 只续写一次，要求编码代理按实际核验范围检查受影响 Owner；再次停止仍无回执时报告协议失败并放行，避免无限循环。Skill 内的 `references/memory.md` 是入册规则，真正的事实写入目标仓库 Owner 事实册。Hook 不选择 Skill、不判断事实 Owner、不起草事实正文，也不从 diff 自动写文档；它只能核验回执、观测证据与事实册变化是否一致，不能证明 AI 已选全受影响 Owner 或事实语义本身正确。

验证证据不能自报命令或退出码，只能引用 `status.validationEvidenceCandidates` 中由 Hook 实际观察到的 `Bash`、`exec_command` 或 `shell_command` 完成事件；`status`、`begin`、`record` 协议命令与 `apply_patch`、`Edit` 等编辑工具不能冒充验证。候选必须发生在最后一次实现变更之后，且验证前后实现指纹均与终态一致；实现指纹只排除合法 Owner 事实册，因而验证后可再写入事实，其他文件变更仍会使旧证据失效。无法解析、超时、取消、Pre/Post 输入不一致或并发的事件均无效。其他会话的顺序变更只用于解释共享工作树漂移，不会归给当前会话；重叠会话触及同一事实册时只能明确 `DEFERRED` 或 `BLOCKED`。

终态结果只有：

- `SYNCED`：至少一个事实执行 `ADD`、`UPDATE` 或 `DELETE`，事实册指纹已经变化。
- `NO_CHANGE`：已检查 Owner，但所有事实均无变化，事实册字节未变。
- `DEFERRED`：实现已有观测验证，但事实归属、证据或写权限不足，事实册保持不变并记录原因。
- `BLOCKED`：交付物尚未形成可验证终态，事实册保持不变并记录阻塞。

Hook 注入的上下文会给出当前会话可直接执行的完整 `status` 命令。普通工具 Shell 不保证继承 Hook 数据环境，必须保留命令中的 `--data-dir` 与 `--session`：

```bash
node "<plugin-root>/scripts/terminal-hook.mjs" status --data-dir "<plugin-data>" --session "<session-id>" --json
```

专门维护事实而其他仓库内容可能不变时，先显式开始：

```bash
node "<plugin-root>/scripts/terminal-hook.mjs" begin --data-dir "<plugin-data>" --session "<session-id>" --json
```

按 `references/terminal-protocol.md` 创建回执后记录：

```bash
node "<plugin-root>/scripts/terminal-hook.mjs" record --data-dir "<plugin-data>" --session "<session-id>" --envelope "<status.envelopePath>" --json
```

每个会话与 turn 使用独立的 `envelopePath`，新 `turn_id` 不继承旧续写。回执绑定 Git 根、会话、turn、最终指纹、账本中的工具 ID/输入摘要/命令哈希、`productId + owner + factBookPath` 和事实动作；实际归属于当前会话的事实册变化必须逐册一致。回执记录成功或拒绝后立即删除，孤儿回执 24 小时清理，七日未更新的会话状态与超过 1024 条的旧账本边会被有界清理。

Hook 是客户端 guardrail，不是不可绕过的执行沙箱。未注册工具、专用执行路径或外部编辑器可能不产生工具事件，`tool_response` 也只是 model-facing JSON；这类未观测变化会令回执失败，但若客户端完全绕过 Hook，插件不能宣称形成完整强制边界。Hook 也不能仅凭 Shell 名称或退出零判定验证是否充分；完整指纹与实现指纹都流式覆盖脏文件、`assume-unchanged`、`skip-worktree` 与脏子模块，仍只证明本地工作树状态。

## 目录

```text
product-studio/
|-- skills/                       # 十一项自主发现的专业 Skill
|   `-- <skill>/
|       |-- SKILL.md              # 统一执行契约
|       |-- agents/openai.yaml
|       `-- references/
|           |-- principles.md     # 统一专业能力格式
|           `-- memory.md         # 统一事实规则格式
|-- hooks/hooks.json              # Prompt、工具前后与 Stop 终态 Hook
|-- scripts/
|   |-- terminal-hook.mjs
|   `-- validate-project.mjs
|-- references/terminal-protocol.md
|-- tests/terminal-hook.test.mjs
|-- docs/product-studio/<product-id>/
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

安装后应先审阅并信任插件 Hook。Hook 命令在当前会话目录执行，状态与回执写入客户端提供的插件数据目录，不写入目标仓库。

## 校验

```bash
node scripts/validate-project.mjs
node --test tests/terminal-hook.test.mjs
claude plugin validate --strict .
```

每项 Skill 还应使用当前 `skill-creator` 的 `quick_validate.py` 独立校验。静态结构和 Hook 单元测试不能证明真实客户端一定会在新上下文中选择正确专业；发布前仍应以未显式点名 Skill 的正反向任务做安装态行为验收。
