# 产品工作室

产品工作室是一套面向 Codex 与 Claude Code 的氛围编程插件。它用七个可调用 Skill 约束路由编排、产品设计、架构设计、前后端编码、测试验证和发布运行，使 AI 先读取现有仓库和调用链，再在最小范围内修改代码并以证据收口。

## 七个 Skill

| Skill | 专业能力 |
|---|---|
| `router` | 识别任务涉及的产品设计、系统架构、后端、前端与验证代码面，选择最短 Skill 链；建立依赖图和输入快照；判断前后端能否并行；锁定共享契约、Schema 与公共组件的唯一合并者；处理代码任务的范围变化与失败隔离，并在约定产物齐备或硬依赖失败时停止编排。 |
| `design` | 从目标用户与业务结果出发，删减无价值步骤，定义最短任务路径、必要信息与动作、交互状态、反馈恢复、端到端业务闭环、范围、指标和可观察验收标准；不承担系统架构或界面代码设计。 |
| `architecture` | 只在真实跨边界风险存在时，依据系统上下文裁定边界职责、数据所有权与共享不变量、跨边界交互、质量方案、故障安全、信任边界、可运行性、演进迁移和交付切片；不代替实现技能编码。 |
| `backend` | 依据产品与适用架构契约实现领域状态与不变量、具体 API、Schema/索引/迁移代码、身份授权、事务/并发/幂等、缓存消息、外部集成和服务端开发测试。 |
| `frontend` | 设计并实现页面任务流、信息层级、设计令牌、组件变体、布局与响应式规则、loading/empty/error/success/disabled 状态、键盘与读屏可访问性、性能预算，并在真实浏览器中核验主题、视口、身份和数据状态。 |
| `verification` | 将产品、架构与实现契约追溯到证据，按风险设计、补充并执行测试用例，包括单元、契约、集成、端到端和非功能验证；核验接口、权限、数据不变量、迁移恢复、前端交互与真实渲染，只依据当前制品与环境给出独立结论。 |
| `release` | 接收已验收变更，约束仓库发布差异、版本权威、版本号、Tag 与发布说明，再分别裁定发布就绪、当前授权、实际执行与运行健康；管理制品配置、发布策略、迁移编排、观测门禁、停止回滚、事故恢复和反馈闭环，只有明确授权覆盖当前仓库或制品、目标提交、环境、范围、动作与时窗时才执行状态变更。 |

每个 `SKILL.md` 保存触发、职责边界、能力加载、执行顺序、输入输出、记忆入口和交接；可复用的具体专业事项位于同技能 `references/principles.md`，并统一使用“目录—核心能力—常见误判”三章，不再重复宽泛的角色职责。六个专业 Skill 另以技能自有的 `references/memory.md` 保存本 Owner 唯一的记忆规则与实例格式；能力准则不承载记忆规则，`router` 也不拥有记忆。

## 路由

明确的单一任务直达专项 Skill，不必先经过网关：

```text
明确前端改动    frontend -> verification
明确后端改动    backend -> verification
仅产品设计      design
仅系统架构      architecture
已验收制品发布  release
```

模糊、跨角色、端到端或高风险代码任务由 `router` 选择最小链：

```text
清晰全栈功能    router -> backend / frontend -> verification
产品语义未定    router -> design -> architecture[按风险启用]
                -> backend / frontend -> verification
技术边界未定    router -> architecture
                -> backend / frontend -> verification
实现并发布      router -> [design / architecture 按需]
                -> backend / frontend -> verification -> release
```

前后端只有在公共契约稳定、输入快照一致、依赖独立且写入不冲突时才能并行。同一 API、Schema、迁移代码或公共组件必须串行合并。

生产部署、生产数据库迁移、切流、生产配置写入、回滚与故障处置只由 `release` 在明确授权覆盖当前制品、目标环境、范围、动作与有效时窗时，使用项目既有且已核验的运行工具执行。其余 Skill 的代码权限、验收结论、方案或历史许可均不构成生产授权；缺少授权时 `release` 只给出就绪、缺口和下一动作，不得宣称线上操作已经执行或生产环境已经健康。

## 当前项目事实

`skills/` 约束 AI 如何工作；`<项目根>/docs/product-studio/` 保存下一次编码或发布真正需要的总结性当前事实。源码、权威 Schema、流水线、制品库和环境查询始终是权威，记忆只保留跨消费者、重查成本高或误判风险大的语义摘要。`router` 不拥有记忆，避免编排状态成为第二事实源；只有下列六册可按需存在：

每册都是对应 Owner 对整个项目的累计专业事实视图，不是单轮任务摘要，也不是六份相互复制的项目总览。单轮任务只增量同步实际核验范围，事实册整体不以单轮范围、最近差异或最后一次修改为边界；不要求每轮扫描全库，明确记忆维护任务可按专业范围补做基线核对。

| Owner | 保存的当前项目事实 |
|---|---|
| `design` | 已实现的目标用户与业务结果、用户旅程、业务规则、交互闭环、范围和体验约束 |
| `architecture` | 架构问题与系统上下文、边界职责、数据所有权与共享不变量、跨边界交互、质量决定、故障恢复、安全与信任、可观测与可运行，以及已实施的演进、迁移和兼容约束 |
| `backend` | 非显然的领域、具体接口、数据、权限、事务并发、事件、缓存、集成和服务端运行行为 |
| `frontend` | 核心界面任务、共享组件、状态恢复、布局、响应式、可访问性和设计系统约束 |
| `verification` | 可重复执行的检查能力、稳定风险覆盖关系和持续验证约束 |
| `release` | 可复用的仓库发布基线、版本权威与政策、Tag 约定、制品识别、环境契约、部署迁移顺序、健康与业务信号、停止恢复入口和运行限制；易变状态必须绑定当前仓库或环境、目标提交、制品、核验时点与失效条件 |

每个专业 Skill 的 `references/memory.md` 是该 Owner 唯一的收录、实例格式和终态同步规则；首次确有事实时按其中格式创建当前项目事实册，不在插件根维护共享契约、模板或格式版本号，事实册也不使用 frontmatter。每个事实使用简短的人类可读主题，只含当前事实、权威依据、影响边界和复核入口。

- 只在获准写入的编码、验收、发布或明确记忆维护任务形成终态且取得相称验证后同步；只读任务未获事实册写入授权时只报告候选增改删与证据。
- 事实是否入册只由当前是否成立、Owner 归属和后续复用价值决定，与本次是否修改相关代码、配置或环境无关；最终差异只用于定位变化与回归风险，不构成事实边界。
- 有变化便原位增改删主题；完成本次实际核验范围的当前事实核对后无增、改、删，才报告 `memory: 0 facts changed`。
- 重构、迁移、改名和实现变更只是重新核对记忆的触发器，不得成为主题、阶段记录或前后对比；未完成状态与临时兼容路径不入册。
- 实例只保存预计后续仍会使用的当前事实；任务经过、执行流水、一次性指标样本、历史版本、授权、秘密与可由权威来源生成的清单不入册。最后一个主题删除后移除整册，Git、流水线、制品库与事件系统承担历史。

## 目录

```text
product-studio/
|-- skills/
|   |-- router/references/        # principles.md，无记忆卷
|   |-- design/references/        # principles.md + memory.md
|   |-- architecture/references/  # principles.md + memory.md
|   |-- backend/references/       # principles.md + memory.md
|   |-- frontend/references/      # principles.md + memory.md
|   |-- verification/references/  # principles.md + memory.md
|   `-- release/references/       # principles.md + memory.md
|-- docs/product-studio/   # 当前项目实际存在的代码事实子集
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

Claude 严格校验负责清单与目录格式；Codex 侧以 marketplace 实际安装和新线程中的技能发现为准。平台格式校验不证明路由选择、专业判断或目标项目行为，须使用未提示技能名的全新上下文作正反向试用，并将输入、输出、当前版本和越权情况绑定为直接证据。
