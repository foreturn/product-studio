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

每个 `SKILL.md` 保存触发、能力加载、执行顺序、输入输出、记忆入口和边界；可复用的细分专业判断位于同技能 `references/`。当前五份能力准则以 `9efef58ddb3f3a4bebcf856f6c2eef7ca7a53194` 的对应原卷为基线，删去了独立的决策顺序与交付证据章节；`design` 的产品模式直接依其 `SKILL.md` 契约执行，系统模式加载架构卷。每卷沿用“目录—角色职责—核心能力—常见误判”。四个专业 Skill 另以技能自有的 `references/memory.md` 保存本 Owner 唯一的记忆规则与首建骨架；专业能力卷不承载记忆规则，`router` 也不拥有记忆。

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

`skills/` 约束 AI 如何工作；`<项目根>/docs/product-studio/` 保存下一次编码真正需要的总结性当前代码事实。源码和可生成清单始终是权威，记忆只保留跨消费者、重查成本高或误判风险大的语义摘要。`router` 不拥有记忆，避免编排状态成为第二事实源；只有下列四册可按需存在：

| Owner | 事实键示例 | 保存内容 |
|---|---|---|
| `design` | `design:rule:*`、`design:contract:*` | 已实现的用户旅程、业务规则、边界、共享契约、不变量和迁移阶段 |
| `backend` | `backend:domain:*`、`backend:api:*`、`backend:data:*` | 非显然的领域行为、接口语义、数据与并发约束、权限、事件、集成和运行行为 |
| `frontend` | `frontend:surface:*`、`frontend:state:*`、`frontend:system:*` | 核心界面任务、共享组件、状态恢复、布局、响应式、可访问性和设计系统约束 |
| `verification` | `verification:check:*`、`verification:coverage:*` | 可重复执行的检查、风险覆盖关系和已证实的验证限制 |

每个专业 Skill 的 `references/memory.md` 是该 Owner 唯一的收录、键型、建册和终态同步规则；首次确有事实时，只把其中的内嵌骨架实例化到当前项目，不在插件根维护共享契约、模板或格式版本号。每个键统一为稳定的 `owner:type:slug`，每条事实只含五项：事实摘要、代码定位、依赖与影响、验证入口、失效条件。

- 每次编码任务进入完成终态，或部分完成中已有独立可用且验证成立的切片时，受影响 Owner 都必须按最终差异执行同步检查；有变化便增改删，无变化报告 `memory: 0 keys changed`，不制造时间戳差异。
- 实例只保存已在代码中成立、预计仍会使用的总结事实；任务经过、一次性证据、历史版本、秘密与可由源码生成的清单不入册。
- 同一语义原位更新，跨 Owner 只链接事实键；最后一张卡删除后移除整册，Git 承担历史。

## 目录

```text
product-studio/
|-- skills/
|   |-- router/references/        # 交付编排能力卷，无记忆卷
|   |-- design/references/        # 架构能力卷 + 技能自有 memory.md
|   |-- backend/references/       # 后端能力卷 + 技能自有 memory.md
|   |-- frontend/references/      # 前端能力卷 + 技能自有 memory.md
|   `-- verification/references/  # 验证能力卷 + 技能自有 memory.md
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

```bash
python3 -X utf8 scripts/validate_project.py --self-test
claude plugin validate --strict .
```

项目校验覆盖五技能集合、五份能力准则的裁剪后基线哈希与四章结构、38 项核心能力、代码路由边界、四份技能自有记忆卷及内嵌骨架、稳定事实键、五字段摘要和双端 manifest 一致性。静态通过只证明当前快照的源码契约、定位和链接自洽，不能发现锚点仍存在但事实语义已陈旧；语义新鲜度由每次编码终态对照最终差异同步。真实插件触发、目标项目运行与交互行为仍须取得直接证据。
