# 产品工作室

产品工作室是一套面向 Codex 与 Claude Code 的软件工程专业技能插件。编码代理仍直接理解请求、阅读仓库、编写代码并自主决定需要哪些专业判断；插件以十一项 Skill 提供清晰的专业所有权、实施准则与证据约束，并由每项命中 Skill 的提示契约在最终答复前完成当前项目事实检查。

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

每次实现形成可交付终态并取得相称验证后，必须执行事实同步检查。每个受影响 Owner 先读取所有权、索引、通用门禁、动作与安全规则，再只展开本轮命中的事实类型和既有主题，并沿权威入口重新取证。新增或更新候选通过全部门禁后才可入册；既有主题须沿当前权威与删除规则判定是否消失。事实动作只有 `ADD`、`UPDATE`、`DELETE`、`NO_CHANGE`，其中 `NO_CHANGE` 必须保持事实文件字节不变。

## 提示式终态记忆

每项 `SKILL.md` 的“终态记忆”都是必须在最终答复前主动执行的提示契约。插件不注册客户端 Hook，也不维护会话状态、工具账本或机器回执；专业判断、事实写入和结果报告均由实际命中的 Skill 完成。

对每个受影响 Owner，编码代理必须唯一确认 Git 根、产品与 `product-id`，读取该 Skill `references/memory.md` 的所有权、事实类型索引、通用门禁、动作与安全规则，再只展开命中的事实类型和既有主题。事实册只作语义导航，所有候选都须沿当前代码、Schema、配置、契约、制品或获准环境重新复核。

事实动作仍只有 `ADD`、`UPDATE`、`DELETE`、`NO_CHANGE`。新增或更新候选通过全部门禁时才可 `ADD` 或 `UPDATE`；当前权威证明既有主题或最后消费者消失时执行 `DELETE`；完整复核且无实质变化时为 `NO_CHANGE` 且必须保持文件字节不变。增改删均须已获仓库写入授权；归属、证据、当前性或写权限不足时不写入，并报告具体缺口。

最终答复按实际检查的 Owner 报告，每个 Owner 只有一个结果，并按 `BLOCKED` > `DEFERRED` > `SYNCED` > `NO_CHANGE` 裁定：

- `BLOCKED`：交付物尚未形成可验证终态，不进行事实同步。
- `DEFERRED`：交付已形成终态，但至少一个应检查主题尚未安全收束；未通过项不写入，已安全完成的事实动作仍逐项报告。
- `SYNCED`：全部应检查主题已安全收束，至少一个事实执行了 `ADD`、`UPDATE` 或 `DELETE`，且写后已经复核。
- `NO_CHANGE`：全部应检查主题已安全收束且没有事实变化，事实册保持字节不变。

完整步骤见 `references/terminal-protocol.md`。提示契约无法机械阻断遗漏，也不能证明编码代理已经选全受影响 Owner；项目静态校验只证明十一项 Skill 都含完整指令。专业选择、事实语义、实际写入与后续会话读取必须通过新上下文行为验收。

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
|-- scripts/validate-project.mjs
|-- references/terminal-protocol.md # 提示式终态记忆公共协议
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

安装后应在新上下文确认十一项 Skill 可被发现，并用未显式点名 Skill 的正反向任务检查专业选择与终态事实报告。

## 校验

```bash
node scripts/validate-project.mjs
claude plugin validate --strict .
```

每项 Skill 还应使用当前 `skill-creator` 的 `quick_validate.py` 独立校验。静态结构不能证明真实客户端一定会在新上下文中选择正确专业、执行终态记忆或写出正确事实；发布前仍应以未显式点名 Skill 的正反向任务做安装态行为验收。
