# 产品工作室

产品工作室是一套面向 Codex 与 Claude Code 的氛围编程插件。它用五个可调用 Skill 约束产品与系统设计、前后端编码和测试验证，使 AI 先读取现有仓库和调用链，再在最小范围内修改代码并以证据收口。

## 五个 Skill

| Skill | 专业能力 |
|---|---|
| `router` | 识别任务涉及的产品、系统、后端、前端与验证代码面，选择最短 Skill 链；建立依赖图和输入快照；判断前后端能否并行；锁定共享契约、Schema 与公共组件的唯一合并者；处理代码任务的范围变化、失败隔离和终态收口。 |
| `design` | 产品模式定义用户、任务、旅程、状态、业务规则、范围、指标与可观察验收标准；系统模式设计领域边界、数据所有权、跨模块契约、质量属性、一致性与故障、安全边界、可观测性、兼容及迁移。局部实现不因流程完整而强制进入设计。 |
| `backend` | 设计并实现领域状态与不变量、API 请求响应和错误契约、Schema/索引/迁移、身份授权与审计、事务/并发/幂等、缓存与消息一致性、外部集成的超时重试及未知态、可观测信号和服务端测试。 |
| `frontend` | 设计并实现页面任务流、信息层级、设计令牌、组件变体、布局与响应式规则、loading/empty/error/success/disabled 状态、键盘与读屏可访问性、性能预算，并在真实浏览器中核验主题、视口、身份和数据状态。 |
| `verification` | 将产品规则追溯到证据，按风险设计分层测试，包括单元、契约、集成、端到端和非功能验证；核验接口、权限、数据不变量、迁移恢复、前端交互与真实渲染；区分失败、阻塞和既有问题，只依据当前制品与环境给出独立结论。 |

每个 `SKILL.md` 保存触发、能力加载、执行顺序、输入输出、记忆和边界；可复用的细分专业判断位于同目录 `references/`。当前五份能力准则以 `9efef58ddb3f3a4bebcf856f6c2eef7ca7a53194` 的对应原卷为基线，删去了独立的决策顺序与交付证据章节；`design` 的产品模式直接依其 `SKILL.md` 契约执行，系统模式加载架构卷。每卷沿用“目录—角色职责—核心能力—常见误判”；`references` 只保存专业能力、判断方法与证据标准，不承载触发、路由、记忆或外部操作规则。

## 路由

明确的单一任务直达专项 Skill，不必先经过网关：

```text
明确前端改动    frontend -> verification
明确后端改动    backend -> verification
仅产品或系统设计 design
```

模糊、跨角色、端到端或高风险代码任务由 `router` 选择最小链：

```text
清晰全栈功能    router -> backend / frontend -> verification
边界尚不清晰    router -> design -> backend[冻结具体 API 契约]
                -> backend / frontend -> verification
```

前后端只有在公共契约稳定、输入快照一致、依赖独立且写入不冲突时才能并行。同一 API、Schema、迁移代码或公共组件必须串行合并。

本插件不执行生产部署、生产数据库迁移、切流、生产配置写入或回滚。这些外部状态操作应交由项目既有发布工具与运行责任人处理；插件可以设计、实现和验证相关代码，但不得据此宣称线上操作已经执行或生产环境已经健康。

## 当前代码事实

`skills/` 约束 AI 如何工作；`<项目根>/docs/product-studio/` 保存 AI 下一次编码必须知道的当前实现事实。`router` 不拥有记忆，避免编排状态成为第二事实源。只有下列四册可按需存在：

| Owner | 事实键示例 | 保存内容 |
|---|---|---|
| `design` | `design:product:rule:*`、`design:system:contract:*` | 已实现的用户旅程、业务规则、边界、契约、不变量和迁移阶段 |
| `backend` | `backend:api:*`、`backend:schema:*`、`backend:auth:*` | 实际 API、Schema、权限、事件、外部集成和运行配置 |
| `frontend` | `frontend:token:*`、`frontend:component:*`、`frontend:layout:*` | 实际颜色/间距令牌、组件样式与状态、页面布局、断点和交互状态 |
| `verification` | `verification:check:*`、`verification:coverage:*` | 可重复执行的检查、风险覆盖关系和已证实的验证限制 |

每条事实只含五项：当前实现、源码锚点、关联与消费者、验证证据、重验条件。维护规则如下：

- 任务完成且适用验证结束后，只更新本次代码真正改变的事实键；只读、取消、中断、失败在终态前或无事实变化时不写。
- 同一语义键原位更新；新增代码新增键；代码、路由、组件或契约被删除后移除对应事实。Git 承担历史，不在事实册保存 `superseded` 卡、任务摘要、动作队列或每轮命令流水。
- 精确 API/路由、OpenAPI、Schema、设计令牌等若能从源码稳定生成，以生成结果为权威；记忆只保留便于编码的语义投影、消费者关系和证据锚点。
- `templates/` 仅供该角色首次建册。实例化后删除说明、键目录和占位；既有事实册不得再次套用模板。

## 目录

```text
product-studio/
|-- skills/
|   |-- router/
|   |-- design/
|   |-- backend/
|   |-- frontend/
|   `-- verification/
|-- templates/             # design/backend/frontend/verification schema 3 母版
|-- docs/product-studio/   # 当前项目实际存在的代码事实子集
|-- scripts/validate_project.py
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

```powershell
python scripts/validate_project.py
claude plugin validate --strict C:\Users\root\plugins\product-studio
```

项目校验覆盖五技能集合、五份能力准则的裁剪后基线哈希与四章结构、38 项核心能力、代码路由边界、四份 schema 3 母版、当前事实键和双端 manifest 一致性。静态通过只证明源码契约自洽；真实插件触发、目标项目运行与交互行为仍须取得直接证据。
