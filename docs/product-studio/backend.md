---
schema: 1
memory: backend
scope: current-project
project_root: "current product-studio repository"
status: done
updated_at: "2026-07-31T15:37:46+08:00"
verified_at: "2026-07-31T15:37:46+08:00"
verified_revision: "9efef58ddb3f + source-worktree:f0cd0325d657"
confidence: high
supersedes: [MIG-001]
---

# backend

- 固定责任角色：`backend`（后端负责人）
- 项目根：当前 `product-studio` 仓库
- 记忆路径：`docs/product-studio/backend.md`

## 恢复摘要

- 当前后端目标：保持八字段后端能力与调用路径结论；schema 2 首次建档模板只保留领域、Schema、API、权限、一致性、集成、可观测、兼容与限制九个事实家族的完整索引及一张可复制的十三字段通用骨架，实例化只生成有证据的事实，后端专业细节仍唯一保存在 `skills/backend/references/backend-design-principles.md`；`backend.md` 仍只在实现和适用验证完成后的任务终态增量更新。
- 当前契约结论：本轮仅变更 Skill、schema 2 首建模板与校验器所承载的项目记忆契约；无运行时 API、Schema、数据库、权限、迁移、数据或调用方行为变化。既有 schema 1 记忆不迁移，只修改本轮实际受影响的稳定 ID。
- 首个可执行动作：无；下次真实后端任务仍从实际调用方出发完成最小实现与适用验证，形成终态后仅在存在后端事实增量时合并受影响稳定 ID。
- 阻塞或不适用原因：无源码后端能力阻塞；实际安装与发布未获授权，但不构成本轮源码交付阻塞。

## 输入来源与适用性

| 来源 ID | 类型 | 记忆、Schema、路径或链接 | 提取内容与用途 | 采纳状态 | verified_revision | 失效条件 |
|---|---|---|---|---|---|---|
| SRC-001 | 当前项目事实 | `discovery.md` AC-001..010 | 一词命名、同名文件、来源分层与能力分层验收 | adopted | `347c769c5e9b + worktree:186d7c03e713` | 产品标准变化 |
| SRC-002 | 当前项目事实 | `architecture.md` ADR-002..006 | 使用 `$backend`、Schema 优先、来源分层及 Skill/reference 两层契约 | adopted | `347c769c5e9b + worktree:186d7c03e713` | 架构决定被取代 |
| SRC-003 | 当前项目决定 | `architecture.md` ADR-007 | 在两层单向引用内采用四字段能力卡结构并明确架构／后端裁决边界 | superseded | `9efef58ddb3f + worktree:78def6775d85` | 已由用户反馈触发失效并被 SRC-004、SRC-005 取代 |
| SRC-004 | 当前产品事实 | `discovery.md` AC-012、D-006 | 以 HEAD 改前版本为语义基线，52 张卡恢复八字段专业正文，目录只导航且不恢复宽泛角色职责 | adopted | `9efef58ddb3f + worktree:babe95b0ce48` | 产品标准或能力语义变化 |
| SRC-005 | 当前架构决定 | `architecture.md` ADR-008、ADR-009 | 八字段能力卡、完整裁决轨迹及架构／后端职责边界 | adopted | `9efef58ddb3f + worktree:babe95b0ce48` | ADR-008、ADR-009 被取代或语义审计失败 |
| SRC-006 | 当前架构与角色本地契约 | `architecture.md` ADR-010 至 ADR-012、INV-010；`skills/delivery/SKILL.md`、`skills/backend/SKILL.md` 与 `scripts/validate_project.py` | `delivery` 负责跨角色路由与串行收口，`backend` 自包含事实准入和增量规则，校验器守住单一所有权与冲突语义；后端落盘晚于实现与适用验证 | adopted | `9efef58ddb3f + source-worktree:f0cd0325d657` | 终态、事实粒度、Owner、权威路由或串行顺序变化 |
| SRC-007 | 用户确认 | 本轮用户指令（2026-07-31） | 记忆模板应保存已成立的项目详细事实，使 AI 能清晰理解项目；后端事实须落到领域行为、权威 Schema、Operation、权限、一致性与运行证据 | adopted | 当前源码与最终验证基线 | 用户改变模板用途或后端事实分类 |

## 依据账本

| ID | 类型 | 内容 | 精确来源 | 置信度 | 状态 | 取代关系 | 失效条件 |
|---|---|---|---|---|---|---|---|
| F-001 | 仓库事实 | 当前仓库是插件指令与模板工程，本轮无运行时 API 或数据实现 | 当前 Git 差异 | 高 | active | 无 | 出现业务后端差异 |
| D-001 | 决定 | 无后端影响时只记影响判断、依据与重新适用条件，不铺设空 API 章节 | `templates/backend.md` | 高 | active | 旧空壳契约写法 | 出现真实 API 变化 |
| D-002 | 决定 | 外部 API 文档、协议与参考实现可参与方案分析；当前项目 Schema、调用链、实现与验证证据决定契约采纳状态 | `skills/backend/SKILL.md`、ADR-005 | 高 | active | 旧来源白名单措辞 | 来源模型变化 |
| D-003 | 决定 | 后端职责、八项核心能力、决策顺序、证据与误判按旧五章节存于 `backend-design-principles.md` | `skills/backend/`、ADR-006 | 高 | superseded | superseded by D-004 | 仅作取代链追溯 |
| D-004 | 决定 | 后端 reference 使用能力目录、八张四字段核心能力卡、能力组合与完成判据，Skill 按需加载适用能力卡 | `skills/backend/SKILL.md`、`skills/backend/references/backend-design-principles.md`、ADR-007 | 高 | superseded | supersedes D-003；superseded by D-006 | 用户实读证明正文更宽泛、没有改前详细 |
| D-005 | 决定 | `architecture` 只裁决跨边界语义、不变量、数据所有权、信任边界、质量属性与演进约束；`backend` 裁决具体 API 字段和错误码、Schema 与索引、授权校验、事务、幂等及补偿实现 | `skills/architecture/references/architecture-principles.md`、`skills/backend/references/backend-design-principles.md` | 高 | active | supersedes 双方双重所有的宽泛表述 | 新任务出现无法唯一归属的裁决 |
| F-002 | 用户反馈 | 上一轮能力卡更宽泛且不如改前详细，须恢复可执行判断、证据、失败模式与反例，而非继续压缩 | 本轮用户反馈（2026-07-31） | 高 | active | supersedes 四字段压缩式质量结论 | 用户明确接受更低专业细节密度 |
| D-006 | 决定 | 后端 reference 保留四章与八个原能力 H3，每卡依次且仅一次包含启用、输入、执行、裁决、产出、验证、完成、边界，并以 HEAD 改前版本为最低语义基线 | `skills/backend/SKILL.md`、`skills/backend/references/backend-design-principles.md`、ADR-008 | 高 | active | supersedes D-004 的压缩型正文；不恢复宽泛角色职责 | 语义审计或真实任务发现改前独有细节缺失 |
| D-007 | 决定 | 每个真实后端入口先画清正常、拒绝、失败调用路径并落实最小完整行为；只对受影响关键路径补业务状态、拒绝、失败、延迟与积压信号，再按并发、幂等、迁移和依赖故障等实际风险扩展验证 | `backend-design-principles.md#能力组合`、API／可靠性／性能／测试能力卡 | 高 | active | supersedes 先堆可观测性、全量测试或抽象层再实现核心行为的顺序 | 新任务证明前置运行信号是安全实施所必需，或上游契约改变 |
| F-003 | 仓库事实 | 本轮后端影响仅涉及产品工作室的 `delivery` 路由、各 Skill 本地项目记忆规则、模板引用、说明与校验器；未修改运行时 API、Schema、数据库、权限、迁移、数据或调用方行为 | 当前完整差异、V-008 与最终审计 | 高 | active | 无 | 出现任一运行时后端文件、权威 Schema、数据库、权限、迁移、数据或调用方差异 |
| F-004 | 用户确认 | 新建后端记忆须保存已成立、可举证且足以独立理解项目的详细事实，不保存恢复摘要、动作队列、任务过程、未来计划或未证实假设 | 本轮用户确认（2026-07-31） | 高 | active | 补充 D-009 的事实内容要求 | 用户改变项目记忆用途或允许过程内容入册 |
| D-008 | 决定 | 后端终态后整文件全量覆盖 `backend.md` | 本轮短暂方案、用户纠正（2026-07-31） | 高 | superseded | superseded by D-009 | 已命中：会删除仍有效契约、证据与无关章节 |
| D-009 | 决定 | 后端项目记忆步骤位于实现与适用验证之后；仅当终态存在后端事实增量时，由 `backend` 按稳定 ID 合并受影响条目，无增量不改文件或时间戳。schema 2 首建模板只保留后端九个事实家族的完整索引与一张可复制的十三字段通用骨架，不按家族预铺空卡；实例化仅生成有证据的事实，后端专业细节仍唯一保存在 `skills/backend/references/backend-design-principles.md`。既有 schema 1 或 schema 2 不再读取或套用模板，只依据 `skills/backend/SKILL.md` 的本角色事实卡规则、后端 ID 家族与自身事实卡增量维护，不迁移或重建；跨角色次序由 `delivery` 路由，结构与冲突语义由校验器守护 | `skills/backend/SKILL.md`、`skills/delivery/SKILL.md`、`skills/backend/references/backend-design-principles.md`、`templates/backend.md`、`scripts/validate_project.py`、ADR-010 至 ADR-012 | 高 | active | supersedes D-008 及实现前落盘 | 后端记忆生命周期、Owner、事实分类、权威路由或版本边界变化 |

## 调用路径与实施顺序

| 路径 | 必须追踪的链路 | 收口要求 |
|---|---|---|
| 正常 | 调用方 → HTTP／RPC／消息／任务入口 → 领域规则与状态转换 → 权威 Schema／事务 → 缓存、外部依赖或事件副作用 → 调用方可见结果 | 字段来源、授权、提交点、响应和最终业务状态一致；不增加无消费者的字段或抽象 |
| 拒绝 | 结构／类型／跨字段校验、认证、授权、资源存在性、状态冲突或重复操作 → 对应错误分类 → 调用方修正、停止或重试行为 | 在副作用前拒绝；错误可行动且不泄露他人资源、租户数据或内部实现 |
| 失败 | 数据库、外部依赖、消息、缓存、并发竞态或进程中断 → 已提交状态与部分成功 → 唯一重试主体、幂等／补偿／对账 → 用户反馈、告警或人工入口 | 每个失败状态可观察、可恢复并有最终责任者；不得以消息入队、进程重启或快乐路径单测冒充业务完成 |

实施次序固定为：核验产品与架构契约及现有调用图 → 完成当前需求所需的最小领域、API、持久化和权限改动 → 仅为受影响关键路径补充可定位的日志、指标、追踪或健康语义 → 依据真实风险增加契约、数据库、并发、幂等、迁移或故障验证 → 形成终态后仅合并受影响的后端记忆事实。不存在对应风险时，不强制铺设无关中间件、抽象、观测或测试矩阵；无后端事实增量时不改 `backend.md` 或时间戳。

## 动作队列

| 优先级 | 动作 | 前置条件 | 责任角色 | 完成判据 |
|---|---|---|---|---|
| P2 | 后端能力卡正文、字段、调用路径或实现顺序变化后重验 D-006、D-007 | 任一 backend Skill/reference 或校验器变化 | `backend` / `verification` | 新修订重新取得结构、语义、负向和 fresh 后端场景证据 |
| P2 | 后端记忆终态、事实粒度、Owner 或权威路由变化后重验 D-009 | backend 本地记忆规则、`delivery` 路由、模板或校验器变化 | `backend` / `verification` | 根路径、路由、单一所有权、章节唯一与冲突语义门禁及 fresh backend／delivery 场景重新通过，且无运行时后端误报 |
| P2 | 真实后端差异或上游契约变化后重验本记忆 | API、Schema、权限、数据或 ADR 变化 | `backend` | 契约、不变量、恢复、迁移与调用方证据反映当前修订 |

## 当前验证

| ID | 验证目标 | 命令或制品 | 修订与环境 | 结果及退出码 | 核验时间 | 失效条件 |
|---|---|---|---|---|---|---|
| V-001 | 运行时契约影响与 Skill 结构 | 当前工作区差异、七 Skill / 插件 / 项目门禁 | `347c769c5e9b + worktree:7052a4ba756b` | `$backend`、同名文件与专属模板通过；无运行时后端变化 | 2026-07-30T23:03:19+08:00 | 出现 API、Schema、迁移或数据差异 |
| V-002 | 后端来源分层 | Skill / 模板来源语义正向门禁与旧硬辞注入负向变体 | `347c769c5e9b + worktree:7052a4ba756b` | 外部契约材料可作参考，缺少来源或自动升级为当前事实的退化会被识别 | 2026-07-30T23:42:45+08:00 | Skill、模板或校验器变化 |
| V-003 | 后端来源契约回归 | backend Skill Creator 校验、项目校验与完整差异复核 | 本地 Linux，当前 worktree | 结构与来源分层通过，退出码 0；仍无运行时后端变化 | 2026-07-30T23:54:16+08:00 | backend Skill、模板、Schema 或实现变化 |
| V-004 | 后端能力分层与行为 | backend Skill Creator、项目校验、四类负向变体、fresh 支付捕获场景 | `347c769c5e9b + worktree:186d7c03e713` | 主卷无重复；新会话读取 reference 并给出幂等、并发、未知态恢复、迁移与测试交接 | 2026-07-31T00:22:11+08:00 | backend Skill 或能力手册变化 |
| V-005 | 四字段后端能力卡结构与裁决分界 | D-004、D-005、后端 Skill/reference、结构负向门禁与 fresh `GET /users?status=` 场景 | `9efef58ddb3f + worktree:78def6775d85`，Windows PowerShell | 历史结构验证曾通过；随后被用户实读反馈判定正文更宽泛、不如改前详细，故不再作为当前专业质量证据 | 2026-07-31T10:09:16+08:00 | 已命中并由 V-006 取代 |
| V-006 | 八字段后端语义恢复与调用路径 | D-005 至 D-007、后端 Skill/reference、HEAD 语义基线审计、负向变体及 fresh 后端场景 | `9efef58ddb3f + worktree:babe95b0ce48`，Windows PowerShell | 通过：全局 52 卡、416 字段、七 refs 共 2255 行（HEAD 旧版 1015 行）；项目校验、七次 Skill Creator、Claude strict 与 git diff-check 均通过。后端专项复核补齐验证顺序和调用图，fresh 场景先收束最小实现，再覆盖正常、拒绝、失败路径及适用的可观测性与风险验证；行数仅作完整性旁证 | 2026-07-31T10:49:30+08:00 | backend／architecture Skill/reference、记忆、校验器或专业语义变化 |
| V-007 | 后端记忆终态增量与运行时零影响 | D-009、backend Skill／schema 2 首建模板、后端 reference、共享事实卡契约、ID 家族门禁与增量哨兵 | `9efef58ddb3f + source-worktree:bfa1d4812af3`，Windows PowerShell | 通过：后端首建模板保留 9 个事实家族的完整索引与 1 张十三字段通用骨架，共 13 字段，不再预铺 9 张空卡／117 字段；实例化只生成有证据的事实，后端专业细节仍唯一保存在 `skills/backend/references/backend-design-principles.md`。全插件七份模板合计 7 骨架／91 字段，全套静态校验、模板复用／全量覆盖负向门禁及增量哨兵通过；既有 schema 1/2 不读取首建模板、不迁移，只依据共享契约与自身事实卡原位更新受影响稳定 ID；确认无 API、Schema、数据库、权限、迁移、数据或调用方运行时变化 | 2026-07-31T14:33:37+08:00 | backend Skill／模板／校验器、共享记忆契约或运行时后端差异变化 |
| V-008 | 根 reference 删除后的后端权威链与运行时零影响 | SRC-006、F-003、D-009、ADR-012、backend／delivery Skill、校验器及 fresh backend／delivery 场景 | `9efef58ddb3f + source-worktree:f0cd0325d657`，Windows PowerShell | 通过，退出码 0：Python 编译、项目校验、七次 Skill Creator、Claude strict 与 `git diff --check` 全部通过；根路径、角色路由、单一所有权、项目记忆章节唯一及冲突语义负向门禁均按预期拒绝退化，fresh backend 与 delivery 均通过。完整差异确认无 API、Schema、数据库、权限、迁移、数据或调用方运行时变化 | 2026-07-31T15:37:46+08:00 | backend／delivery Skill、模板、校验器、权威 Schema 或任一运行时后端表面变化 |

## 交接与失效

- 调用方先读：`discovery.md` 的当前 AC、`architecture.md` 的 ADR-002、ADR-005、ADR-006、ADR-008 至 ADR-012 与 INV-010、INV-011；ADR-003、ADR-007、D-004、D-008 仅作被取代历史。
- 尚未解决：无源码后端能力缺口；本轮后端影响仅有 Skill、模板与校验器所承载的项目记忆契约变化，无运行时 API、Schema、数据库、权限、迁移、数据或调用方行为变化，真实安装与发布未获授权但不构成源码阻塞。
- 重新核验触发器：后端 Skill、能力字段／正文语义、调用路径规则、事实卡字段或 ID 家族、模板版本边界、记忆终态／增量／Owner 契约、默认提示词或权威 Schema 变化。
- 本记忆失效条件：出现运行时 API、数据、权限、迁移或调用方变化。
