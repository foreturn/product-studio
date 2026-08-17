# 产品工作室

产品工作室是一套面向 Codex 与 Claude Code 的软件工程专业技能插件。编码代理仍直接理解请求、阅读仓库、编写代码并自主决定需要哪些专业判断；插件以十一项 Skill 提供清晰的专业所有权、实施准则与证据约束，并由每项命中 Skill 读取和维护相关项目核心记忆。

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

- `SKILL.md` 的中文 `description` 只作专业发现摘要；正文统一保留目标、六步执行、输出、完成、停止、权限、参考和项目记忆八章，其中“项目记忆”章独占目标仓库与产品标识定位、事实读取、准入、维护与排除规则。它不列适用、不适用或必需输入清单，不展开领域方法，也不编排其他 Skill。
- `references/principles.md` 是通用专业约束正文。正文按八至十六个专业大类组织，每类只列四至八条跨框架仍成立的不变量、取舍标准或禁止边界；不设置字段，不固化特定库、算法、架构模板、阈值或操作步骤。
- `references/memory.md` 只定义本 Owner 应记住哪些项目核心认知。每卷只有“核心记忆”一章，以五至九个专业主题、每题一至三条“记住……”陈述详细列出会持续影响后续判断的项目不变量，不再承载使用协议。
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

事实册是语义索引，不是第二份源码。代码、权威 Schema、流水线、制品库和当前环境查询始终是真相来源；旧记忆与当前权威冲突时，以当前权威为准。

## 项目记忆

每项 Skill 都在 `references/memory.md` 中详细列明本专业应记住的核心认知，并由 `SKILL.md` 的“项目记忆”章统一规定使用方式：先唯一确认目标 Git 根与安全单级 `product-id`，开始相关工作前读取命中的核心主题和目标事实册，核心认知改变时更新或移除旧内容，只保留当前仍成立的事实。归属不唯一或名称不安全时不猜测或创建事实册；事实册不存在时直接依据当前仓库工作，不以缺少记忆阻断任务。

项目记忆只保存会影响未来专业判断、又难以从局部代码直接看清的项目不变量，例如权威边界、跨模块保证、恢复关系和兼容约束。它不保存秘密、令牌、用户数据、任务过程、文件改动清单、迁移进度、运行快照、当前版本或一次性结果，也不要求编码代理输出专门的记忆状态。

维护项目记忆不得扩大原任务的写权限；只读任务仍保持只读。静态校验只能证明十一项 Skill 都含读取与维护指令，真实任务中的专业选择、记忆质量和后续会话读取仍须通过新上下文行为验收。

## 目录

```text
product-studio/
|-- skills/                       # 十一项自主发现的专业 Skill
|   `-- <skill>/
|       |-- SKILL.md              # 统一执行契约
|       |-- agents/openai.yaml
|       `-- references/
|           |-- principles.md     # 统一专业能力格式
|           `-- memory.md         # 本专业项目核心记忆主题
|-- scripts/validate-project.mjs
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

安装后应在新上下文确认十一项 Skill 可被发现，并用未显式点名 Skill 的正反向任务检查专业选择、项目记忆读取与必要的旧认知维护。

## 校验

```bash
node scripts/validate-project.mjs
claude plugin validate --strict .
```

每项 Skill 还应使用当前 `skill-creator` 的 `quick_validate.py` 独立校验。静态结构不能证明真实客户端一定会在新上下文中选择正确专业、读取相关记忆或维护正确事实；发布前仍应以未显式点名 Skill 的正反向任务做安装态行为验收。
