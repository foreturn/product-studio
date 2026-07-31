---
schema: 1
memory: frontend
scope: current-project
project_root: "current product-studio repository"
status: done
updated_at: "2026-07-31T15:37:46+08:00"
verified_at: "2026-07-31T15:37:46+08:00"
verified_revision: "9efef58ddb3f + source-worktree:f0cd0325d657"
confidence: high
supersedes: [MIG-001]
---

# frontend

- 固定责任角色：`frontend`（前端与体验负责人）
- 项目根：当前 `product-studio` 仓库
- 记忆路径：`docs/product-studio/frontend.md`

## 恢复摘要

- 当前用户任务：在既有八字段前端能力契约与终态增量规则之上，将首次建档模板瘦身为八个前端事实家族索引与一张十三字段通用骨架，不再为每个家族预铺空卡。
- 当前界面结论：本轮只有首建模板、七职自包含项目记忆规则、两份根级 reference 删除与校验门禁变化，没有 UI、组件或渲染运行时变化；前端专业细节仍唯一保存在能力手册，既有八字段结论 `D-006` / `V-006` 仍然有效。
- 当前前端边界：只实现产品契约与触发条件证明适用且可达的状态；视口由项目标准、目标用户、现有断点或流量证据驱动；禁用态须说明禁用原因与恢复条件；项目记忆仅在终态验证后增量合并。
- 首个可执行动作：无；后续仅在前端能力语义、运行时 UI 或上游产品／接口契约变化时重验。
- 阻塞：无源码提示词阻塞；真实安装后的 UI 触发验证不在本轮授权范围，也不影响当前源码结论。

## 输入来源与适用性

| 来源 ID | 类型 | 记忆、路径或链接 | 提取内容与用途 | 采纳状态 | verified_revision | 失效条件 |
|---|---|---|---|---|---|---|
| SRC-001 | 当前项目事实 | `discovery.md` AC-001..010 | 一词命名、同名文件、来源分层与能力分层验收 | adopted | `347c769c5e9b + worktree:186d7c03e713` | 产品标准变化 |
| SRC-002 | 当前项目事实 | `architecture.md` ADR-002..006 | 使用 `$frontend`、AI 恢复骨架、来源分层及 Skill/reference 两层契约 | adopted | `347c769c5e9b + worktree:186d7c03e713` | 架构决定被取代 |
| SRC-003 | 外部参考 | `https://github.com/settings/profile`，fresh `$frontend` 前向测试输入 | 目标页跳转登录，受保护界面细节未被观察；仅以导航层级、带标签表单和完整状态作为候选设计方向 | reference-only | `347c769c5e9b + worktree:7052a4ba756b` | 获得可访问页面、截图或用户明确采纳 |
| SRC-004 | 用户确认 | 早先用户指令（2026-07-31） | 删除宽泛角色职责与重复段落，按 reference 既有核心能力改写为四字段能力卡 | superseded | `9efef58ddb3f + worktree:78def6775d85` | 已由 SRC-005 取代 |
| SRC-005 | 用户反馈 | 本轮用户指令（2026-07-31） | 上一版比改前更宽泛且不够详细；以 HEAD 改前版本为语义基线，在四章内恢复可执行判断、证据与反例 | adopted | `9efef58ddb3f + worktree:babe95b0ce48` | 用户接受降低专业细节密度，或语义审计发现旧版独有内容仍缺失 |
| SRC-006 | 用户确认 | 本轮用户指令（2026-07-31） | 过程不写项目记忆；实现与适用验证完成、任务进入终态后，按受影响角色增量合并并保留仍有效事实与无关章节 | adopted | `9efef58ddb3f + worktree:edbcc2f9564f` | 用户改变项目记忆生命周期 |
| SRC-007 | 用户确认 | 本轮用户指令（2026-07-31） | 项目记忆须保存已成立的详细事实；前端首建模板只保留页面／路由、用户行为、状态、实现、可访问性、响应式、渲染与限制八个完整事实家族索引及一张可复制的十三字段通用骨架，实例化只生成有证据的事实卡，角色专业细节仍由前端 reference 承载 | adopted | 当前源码与最终验证基线 | 用户改变模板用途、事实家族或首建方式 |

## 依据账本

| ID | 类型 | 内容 | 精确来源 | 置信度 | 状态 | 取代关系 | 失效条件 |
|---|---|---|---|---|---|---|---|
| F-001 | 仓库事实 | 本仓库没有本轮需渲染的运行时前端界面 | `.codex-plugin/`、`skills/`、`templates/` 目录边界 | 高 | active | 无 | 新增运行时 UI |
| D-001 | 决定 | 前端首次建档模板只列页面与路由、用户流程、界面状态、实现映射、可访问性、响应式、真实渲染及已证实限制八个事实家族，并提供一张可复制的十三字段通用骨架；不得为每个家族预铺空卡，实例化时只生成有证据的真实事实，专业机制仍由前端能力手册提供 | `templates/frontend.md`、`skills/frontend/references/frontend-design-principles.md` | 高 | active | 旧综合功能规格模板、恢复过程骨架与逐家族空卡 | 模板职责、事实家族或首建方式改变 |
| D-002 | 决定 | 显式页面、截图与设计稿可供读取、分析和仿照；品牌、字段、文案、权限与未观察细节保持参考或未知，直至当前项目证据采纳 | `skills/frontend/SKILL.md`、ADR-005 | 高 | active | 旧来源白名单措辞 | 来源模型变化 |
| D-003 | 决定 | 前端职责、八项核心能力、决策顺序、证据与误判唯一存于 `frontend-design-principles.md`，Skill 只保存直达入口和工作约束 | `skills/frontend/`、ADR-006 | 高 | superseded | 被 D-004 取代 | 能力手册或加载模型变化 |
| D-004 | 决定 | 前端 reference 使用能力目录、八张四字段核心能力卡、能力组合与完成判据；Skill 先查目录，再按任务读取适用卡 | `skills/frontend/SKILL.md`、`skills/frontend/references/frontend-design-principles.md` 的历史修订 | 高 | superseded | supersedes D-003；superseded by D-006 | 用户实读证明压缩正文更宽泛、专业细节不足 |
| D-005 | 边界 | 状态只覆盖产品契约、调用路径和触发条件证明适用且可达的集合；浏览器、设备、视口、可访问性与性能验收绑定项目标准，缺失时记录显式假设并限制结论 | `skills/frontend/SKILL.md`、`frontend-design-principles.md` 的组件状态、响应式、可访问性与视觉验收能力卡 | 高 | active | supersedes 机械全状态与任意视口表述 | 上游契约、项目标准或目标用户证据变化 |
| D-006 | 决定 | 保留四章与按需加载，以 HEAD 改前版本为最低语义基线；前端八张卡各依次且仅一次包含启用、输入、执行、裁决、产出、验证、完成、边界，目录仅导航且不替代正文，不恢复空泛“角色职责” | 当前 `skills/frontend/` 差异与本轮用户反馈 | 高 | active | supersedes D-004 的四字段压缩正文，保留其四章和渐进加载原则 | 语义审计或真实任务发现改前独有判断、证据或反例缺失 |
| D-007 | 前端边界 | 候选状态必须记录适用性、可达条件与并存规则；目标视口由项目证据决定；禁用控件在原因并非上下文自明时须提供可访问解释及恢复条件 | `frontend-design-principles.md` 的布局与响应式、可访问性、组件与状态工程能力卡 | 高 | active | supersedes 压缩式状态与任意视口结论 | 产品状态、目标用户、项目标准或前端调用链变化 |
| D-008 | 记忆边界 | 前端过程阶段不得创建或更新项目记忆；任务终态且适用验证完成后，仅按稳定 ID 合并本角色受影响事实，保留仍有效事实、无关章节和未受影响角色，禁止全量覆盖。schema 2 模板仅用于首次创建；既有 schema 1 或 schema 2 不再读取或套用模板，只依据 `skills/frontend/SKILL.md`“项目记忆”中的本角色事实卡规则、前端 ID 家族与自身事实卡增量维护，不迁移或重建 | `skills/frontend/SKILL.md`、`templates/frontend.md` 与本轮用户确认 | 高 | active | supersedes 过程即落盘或整卷重写的记忆方式 | 项目记忆生命周期、事实字段或版本边界变化 |
| D-009 | 记忆内容边界 | 每张前端事实卡须以稳定 ID 加可读标题独立说明事实，并分别保存角色专属细节、范围、精确定位、证据、核验基线、关联事实、下游约束、状态、置信度、取代关系与失效条件；既有 schema 1/2 `frontend.md` 以自身事实卡为更新基线，不读取首建模板或迁移 | `skills/frontend/SKILL.md`、`templates/frontend.md` | 高 | active | 补充 D-001、D-008 | 事实字段、模板版本或格式迁移授权变化 |

## 当前前端语义边界

| 关注面 | 当前规则 | 直接依据 |
|---|---|---|
| 状态 | 仅覆盖适用且可达状态；每个候选状态记录触发条件、可并存关系与不适用依据，不机械铺满加载、空白、错误、权限或恢复状态 | 产品契约、真实调用路径与状态工程能力卡 |
| 视口 | 优先使用项目容器、断点、支持设备、目标用户或流量证据；项目未规定时仅能记录窄屏、常用桌面与宽屏假设并缩小结论 | 布局与响应式、视觉验收能力卡 |
| 禁用态 | 内容、禁用状态与原因均须可辨识；原因并非上下文自明时，提供可访问说明、解除条件与下一动作 | 可访问性与交互能力卡 |

## 实现映射

| 行为或状态 | 文件 / 组件 / Symbol | 数据依赖 | 状态来源 | 测试位置 | Owner |
|---|---|---|---|---|---|
| `$frontend` 角色触发 | `skills/frontend/SKILL.md` | 无 | frontmatter description | Skill 快速校验、项目校验 | `frontend` |
| Codex 默认入口 | `skills/frontend/agents/openai.yaml` | 无 | `default_prompt` | 项目 YAML 断言 | `frontend` |
| 前端项目记忆骨架 | `templates/frontend.md` | `discovery.md`、`backend.md` 引用 | 首次创建使用八家族索引与一张 schema 2 通用骨架；当前 `frontend.md` 继续保留 schema 1，并在终态后按稳定 ID 增量合并 | 单骨架、模板语义、ID 家族与记忆生命周期门禁 | `frontend` |
| 前端专业能力 | `skills/frontend/references/frontend-design-principles.md` | 当前产品、设计系统与实现证据 | 仅导航的能力目录与八字段适用能力卡 | 八卡／64 字段、改前语义基线、能力组合、完成判据与前向行为门禁 | `frontend` |

## 动作队列

| 优先级 | 动作 | 前置条件 | 责任角色 | 完成判据 |
|---|---|---|---|---|
| P2 | 能力字段、正文语义或加载方式变化后重验 D-006、D-007 | frontend Skill/reference 或校验器变化 | `frontend` / `verification` | 新修订重新取得结构、语义与前向直接证据 |
| P2 | 真实 UI 或上游契约变化后重验前端记忆 | 新界面差异或 AC / ADR 变化 | `frontend` | 状态矩阵、实现映射与渲染证据反映当前修订 |

## 当前验证

| ID | 验证目标 | 命令或制品 | 修订与环境 | 结果及退出码 | 核验时间 | 失效条件 |
|---|---|---|---|---|---|---|
| V-001 | 前端影响边界与角色恢复 | 当前工作区差异、Skill / 模板门禁、fresh `$frontend` 前向试用 | `347c769c5e9b + worktree:7052a4ba756b` | 无运行时 UI 变化；新会话读取同名记忆并将缺失产品语义退回 `discovery` | 2026-07-30T23:03:19+08:00 | 新增运行时前端文件或 Skill 提示词变化 |
| V-002 | 外部页面参考行为 | fresh `$frontend` 使用 GitHub 设置页仿照场景 | 只读前向试用，当前 Skill 与记忆 | 页面可作为外部参考；登录阻断被明确记录，未臆造受保护界面，也未把品牌、字段和权限语义记作当前事实 | 2026-07-30T23:42:45+08:00 | Skill 来源语义或参考页面证据变化 |
| V-003 | 前端来源契约回归 | frontend Skill Creator 校验、项目校验与三类来源负向变体 | 本地 Linux，当前 worktree | 正向通过；旧硬辞与来源字段缺失均被拒绝 | 2026-07-30T23:54:16+08:00 | frontend Skill、模板、记忆或校验器变化 |
| V-004 | 前端能力分层 | frontend Skill Creator、项目校验、旧标题零命中、reference 五章节与角色能力词 | `347c769c5e9b + worktree:186d7c03e713` | superseded：该修订曾满足旧结构，当前 Skill/reference 差异已触发失效条件 | 2026-07-31T00:22:11+08:00 | 已命中：frontend Skill 与能力手册变化 |
| V-005 | 四字段能力卡结构与前端边界 | 八张四字段能力卡计数、项目与 Skill 校验、差异检查及独立审校 | `9efef58ddb3f + worktree:78def6775d85`，Windows PowerShell | superseded：历史结构门禁曾通过，但用户实读判定正文更宽泛且不如改前详细，不能继续作为当前专业质量证据 | 2026-07-31T10:09:16+08:00 | 已命中并由 V-006 取代 |
| V-006 | 八字段前端语义恢复 | D-006、D-007、八张能力卡、语义基线审计、结构负向门禁与前向行为复核 | `9efef58ddb3f + worktree:babe95b0ce48`，Windows PowerShell | 通过：八卡／64 字段齐备；适用可达状态、项目驱动视口、禁用原因与恢复条件均有具体正文。七 refs 合计 52 卡／416 字段、2255 行，HEAD 旧版 1015 行；行数仅作完整性旁证，质量由语义审计与前向裁决证明 | 2026-07-31T10:49:30+08:00 | 任一 frontend Skill、reference、记忆、校验器或专业语义变化 |
| V-007 | 前端终态记忆契约 | D-001、D-008、frontend Skill、schema 2 首建模板、ID 家族与项目门禁 | `9efef58ddb3f + source-worktree:bfa1d4812af3`，Windows PowerShell | 通过：前端模板恰有八个完整事实家族索引、一张可复制的十三字段通用骨架；实例化只生成有证据的事实，专业细节仍由前端 reference 承载。全插件七份模板共七张骨架／91 个字段；项目静态校验、缺家族／重复家族／多骨架／缺字段／额外章节／模板复用六类负向门禁均通过。记忆仅在终态且适用验证完成后更新受影响稳定 ID；既有 schema 1/2 不读取模板、不迁移；确认无 UI、组件或渲染运行时变化 | 2026-07-31T14:33:37+08:00 | frontend Skill、模板、记忆或记忆生命周期规则变化 |
| V-008 | 前端自包含记忆契约与运行时零影响 | D-008、D-009、frontend Skill“项目记忆”、同名首建模板、根级 reference 零残留与项目门禁 | `9efef58ddb3f + source-worktree:f0cd0325d657`，Windows PowerShell | 通过：前端事实准入、ID 家族、十三字段、终态增量与 schema 1/2 规则均由 `skills/frontend/SKILL.md` 自包含定义；`templates/frontend.md` 仅加载本角色能力手册，已删除的根级 reference 不再参与寻址。项目校验、Skill 校验、Claude strict 与差异检查通过；确认没有 UI、组件、路由或渲染运行时变化 | 2026-07-31T15:37:46+08:00 | frontend Skill、模板、记忆、校验器或运行时前端差异变化 |

## 交接与失效

- 下游先读：`discovery.md` 的 AC-001 至 AC-014、`architecture.md` 的 ADR-002、ADR-005、ADR-006、ADR-008 至 ADR-011。
- 已知体验缺口：未在已安装插件 UI 中实测触发显示；本轮没有安装授权，该项不构成源码阻塞。
- 尚未解决：无源码前端契约缺口；真实安装插件后的 UI 展示仅在后续获授权时重新适用。
- 重新核验触发器：前端 Skill、默认提示词、事实卡字段或 ID 家族、模板版本边界、manifest 或运行时 UI 变化。
- 本记忆失效条件：出现运行时 UI 改动或上游产品/接口契约变化。
