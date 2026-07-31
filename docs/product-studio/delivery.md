---
schema: 1
memory: delivery
scope: current-project
project_root: "current product-studio repository"
status: done
updated_at: "2026-07-31T15:37:46+08:00"
verified_at: "2026-07-31T15:37:46+08:00"
verified_revision: "9efef58ddb3f + source-worktree:f0cd0325d657"
confidence: high
supersedes: [MIG-001]
---

# delivery

- 固定责任角色：`delivery`（产品交付负责人）
- 项目根：当前 `product-studio` 仓库
- 记忆路径：`docs/product-studio/delivery.md`

## 恢复摘要

- 当前目标：在保留七职八字段专业语义的同时，把项目记忆落实为“已成立项目详细事实册”；事实须让后续 AI 直接理解主体、关键值、行为、边界、证据和跨角色约束，并继续遵守终态后按角色稳定 ID 增量合并。
- 当前阶段：跨角色终态总路由已由 `delivery` Skill 独立定义，七个角色的项目事实准入、稳定 ID、终态增量与模板版本规则分别自包含于同名 Skill；七份 schema 2 首建模板与校验器已采用“完整角色事实家族索引 + 一张可复制的十三字段通用骨架”，不再为每个家族预铺空卡，角色专业细节仍唯一保存在对应 `skills/*/references`。根级 project-memory 与 platform reference 已删除，既有七份 schema 1 记忆未迁移，只对本轮实际变化的事实条目增量修订。
- 当前结论：任务执行、中断、取消或未终态时不创建或修改记忆；终态且适用验证完成后，仅由事实变化角色合并已成立事实。七份模板共 7 张可复制骨架、91 个字段；首次创建仅为有证据的事实复制骨架，既有 schema 1/2 不读取模板，现有记忆不因模板变化重建。
- 首个可执行动作：无；后续仅在能力内容、记忆事实或加载契约变化时重新执行适用验证，并增量合并真实变化条目。
- 阻塞：无；当前源码已完成验收，实际安装与发布仍不在本轮授权范围。

## 原始意图与范围

- 本轮包含：既有命名、记忆与来源契约，七职 Skill/reference 专业分层、能力卡重构，以及项目记忆的终态事实增量生命周期、事实家族索引与通用骨架、模板版本边界、校验器、前向行为与当前事实收口。
- 本轮不包含：插件安装、缓存刷新、Marketplace 外部更新、部署或生产变更。
- 授权边界：可修改并验证当前仓库；不得把源码修改许可外推为外部状态变更许可。

## 依据账本

| ID | 类型 | 内容 | 精确来源 | 置信度 | 状态 | 取代关系 | 失效条件 |
|---|---|---|---|---|---|---|---|
| F-001 | 用户确认 | 每个 Skill 名收紧为一个符合职责的单词 | 本轮用户指令（2026-07-30） | 高 | active | supersedes MIG-001 | 用户另行更改命名策略 |
| F-002 | 用户确认 | 每个 Skill 的项目记忆与 Skill 名一致 | 本轮用户指令（2026-07-30） | 高 | active | 无 | 用户另行指定映射 |
| F-003 | 用户确认 | 记忆模板须提升对 AI 恢复与氛围编程的价值 | 本轮用户指令（2026-07-30） | 高 | active | 无 | 模板目标改变 |
| D-001 | 决定 | 三处命名满足 `skills/<name>/`、`templates/<name>.md`、`docs/product-studio/<name>.md` | 七份 `skills/*/SKILL.md`、七份同名模板与 `scripts/validate_project.py` | 高 | active | supersedes MIG-001 | 平台新增别名或命名约束 |
| F-004 | 用户确认 | “只读取”“不得从其他项目继承”等绝对来源措辞会造成上下文缺失，页面仿照等外部参考应可进入分析 | 本轮用户指令（2026-07-30） | 高 | active | supersedes 旧来源白名单措辞 | 用户重新定义来源边界 |
| D-002 | 决定 | 项目根界定事实归属与写入位置；读取范围按任务相关性开放，外部材料以来源、用途、适用性和采纳状态管理；每个角色的事实准入与写入规则由同名 Skill 的“项目记忆”完整定义 | 七份 `skills/*/SKILL.md#项目记忆` | 高 | active | 无 | 来源模型、事实归属或角色写入规则变化 |
| F-005 | 用户确认 | `SKILL.md` 删除职责、核心能力、专业决策顺序，详细专业能力由同角色 reference 承载并被 Skill 引用 | 本轮用户指令（2026-07-31） | 高 | superseded | supersedes 主卷与 reference 双写；superseded_by F-006 | 用户改变能力分层 |
| D-003 | 决定 | 七职采用约束层与专业层分离；reference 统一包含角色职责、核心能力、专业决策顺序、交付证据与常见误判 | `skills/*/SKILL.md`、`skills/*/references/*.md` | 高 | superseded | superseded_by D-004 | Skill 资源加载模型变化 |
| F-006 | 用户确认 | reference 删除宽泛角色职责，以既有核心能力改写为含启用、执行、产出与完成字段的能力卡 | 本轮用户指令（2026-07-31） | 高 | superseded | supersedes F-005 中的详细职责结构；superseded_by F-007 | 用户改变能力卡结构 |
| D-004 | 决定 | 七职 reference 统一为能力目录、核心能力、能力组合、完成判据；Skill 先读目录，只加载适用能力卡，组合或收口时再读后两节 | `skills/*/SKILL.md`、`skills/*/references/*.md` | 高 | superseded | supersedes D-003；superseded_by D-005 | 能力卡实证表明压缩结构丢失专业细节 |
| F-007 | 用户确认 | 上一轮提示词更宽泛且不如改前详细；须以 HEAD 改前版本为语义基线，删除空泛角色职责但恢复其他章节的独有专业细节 | 本轮用户反馈（2026-07-31） | 高 | active | supersedes F-006 的四字段压缩型能力卡 | 用户明确接受更低细节密度 |
| D-005 | 决定 | 四章骨架继续保留；52 张能力卡各固定启用、输入、执行、裁决、产出、验证、完成、边界八字段，并逐条迁回旧版核心能力、专业决策顺序、交付证据和常见误判中的可执行判断、证据与反例 | 七份 `skills/*/references/*.md` | 高 | active | supersedes D-004 的压缩型正文；保留其四章与按需加载原则 | 用户改变结构，或语义审计发现旧版独有细节遗漏 |
| F-008 | 用户确认 | 氛围编程执行过程中不要持续更新项目记忆，只在任务完成后记录最后一次事实结果 | 本轮用户指令（2026-07-31） | 高 | superseded | superseded_by F-009；过程不写与终态后收口原则继续保留 | 用户重新允许过程写入 |
| D-006 | 决定 | 曾短暂将 F-008 解释为终态时整文件覆盖、仅保留最后事实结果 | 本轮短暂实现（2026-07-31） | 高 | superseded | superseded_by D-007 | 不再适用；不得恢复全量覆盖模型 |
| F-009 | 用户确认 | 完成后不得全量覆盖；各受影响角色只对自己文件做一次事实级增量合并，保留旧有且仍有效事实与未受影响章节，无事实增量不修改文件或时间戳 | 本轮用户纠正（2026-07-31） | 高 | active | supersedes F-008 的全量覆盖解释，保留其过程不写和终态时机 | 用户改变记忆合并语义 |
| D-007 | 决定 | 终态收口采用按角色增量合并：新增事实给稳定 ID，同一语义更新原 ID，语义取代才建立最短取代关系，仅失效事实修改状态；跨角色总路由由 `delivery` Skill 按产品／架构、前端、后端、`verification`、适用的 `release`、`delivery` 顺序串行协调，各角色只依据同名 Skill 的项目记忆契约、角色 ID 家族与自身事实卡维护自己的文件。schema 2 模板仅用于首次建档，既有 schema 1/2 不读取模板、不迁移或重建；任一写入失败时，不依赖该增量的角色可继续，依赖其尚未落盘新 ID 的增量必须暂缓并报告，不得形成悬空引用 | `skills/delivery/SKILL.md#项目记忆`、七份 `skills/*/SKILL.md#项目记忆` 与七份模板 | 高 | active | supersedes D-006 | 事实归属、终态条件、跨角色路由、失败隔离、单一写入所有权或模板版本边界变化 |
| F-010 | 用户确认 | 记忆模板应以已成立的项目详细事实作为正文，使 AI 可清晰理解项目，而不是保存恢复摘要、任务过程、动作队列或未来计划 | 本轮用户确认（2026-07-31） | 高 | active | 补充 F-009 的记忆内容要求 | 用户改变项目记忆用途或允许过程内容入册 |
| D-008 | 决定 | 新建记忆使用 schema 2 角色事实卡：每份模板只保留本角色完整事实家族索引与一张可复制的 13 字段通用骨架，不再为每个家族预铺空卡；角色专业细节仍唯一保存在对应 `skills/*/references`。实例化仅为有证据的事实复制骨架，并删除说明、索引与占位。既有 schema 1/2 保持可读，只依据同名 Skill 的项目记忆契约、角色 ID 家族与自身事实卡按实际变化 ID 增量维护，不再读取模板 | 七份模板、七份 `skills/*/SKILL.md#项目记忆`、七份角色 reference 与校验器 | 高 | active | supersedes S-003 的恢复／动作型模板；补充 D-007 的内容模型 | 事实字段、ID 家族、模板用途或格式迁移授权变化 |
| F-011 | 仓库事实 | 根级 `references/project-memory.md` 与 `references/platform-compatibility.md` 已删除；七个角色的项目事实准入、稳定 ID、终态增量与模板版本规则分别自包含于同名 Skill，跨角色终态总路由由 `delivery` Skill 独立定义。任一角色写入失败时，依赖该失败增量且尚未落盘新 ID 的事实必须暂缓，不得形成悬空引用 | 七份 `skills/*/SKILL.md#项目记忆`、`skills/delivery/SKILL.md#项目记忆`、`scripts/validate_project.py` 与根 `references/` 删除差异 | 高 | active | 补充 D-001、D-002、D-007、D-008 | 角色事实归属、根 reference 架构、跨角色路由或失败隔离语义变化 |

## 角色链与依赖

| 顺序 | Skill | 输入契约 | 输出记忆 | 进入条件 | 状态 |
|---|---|---|---|---|---|
| 1 | `delivery` | 用户指令、仓库差异 | `delivery.md` | 跨角色迁移 | done |
| 2 | `discovery` | 原始意图、现有行为 | `discovery.md` | 产品命名与验收口径需明确 | done |
| 3 | `architecture` | 已确认映射、仓库结构 | `architecture.md` | 目录、兼容与模板结构需裁决 | done |
| 4 | `frontend` / `backend` | 上游决定 | 同名记忆 | 各自 Skill 与模板受影响，可在写集独立时并行 | done |
| 5 | `verification` | 完整差异 | `verification.md` | 所有引用与模板就绪 | done |
| 6 | `release` | 验收与发布授权 | `release.md` | 本轮仅复核源码发布处置 | not_applicable |

## 交付切片

| Slice | Outcome | Owner | Depends on | Write set | Status | Done when |
|---|---|---|---|---|---|---|
| S-001 | 七个 Skill 目录、frontmatter 与调用名均为单词 | `delivery` | F-001 | `skills/` | done | 旧目录与旧显式调用零残留 |
| S-002 | 七份模板与七份项目记忆均和 Skill 同名 | `architecture` | S-001 | `templates/`、`docs/product-studio/` | done | 三处主干名一一对应 |
| S-003 | 模板提供恢复摘要、依据、动作与验证等过程结构 | 七职责任角色 | S-002 | 七份历史模板 | superseded | 已由 S-013 的角色事实卡首建模板取代；过程结构不再写入项目记忆 |
| S-004 | 校验器能阻止命名、同名关系与模板价值退化 | `verification` | S-001、S-003 | `scripts/` | done | 正向和负向断言均通过 |
| S-005 | 七职记忆反映当前差异与验证 | 七职责任角色 | S-004 | 七份项目记忆 | done | 收口表与当前证据一致 |
| S-006 | 七职不再把项目隔离写成上下文读取禁令 | 七职责任角色 | F-004 | `skills/`、`references/`、`templates/` | done | 显式外部参考可读且不会自动升级为当前事实 |
| S-007 | 校验器阻止旧硬辞复发并验证来源分层 | `verification` | S-006 | `scripts/` | done | 正向、旧硬辞注入与来源字段缺失变体均符合预期 |
| S-008 | 七份 Skill 移除三段专业正文并建立唯一能力来源 | 七职责任角色 | F-005 | `skills/*/SKILL.md` | done | 旧标题零命中且七个引用均可达 |
| S-009 | 七份 reference 扩展为可执行角色能力手册 | 七职责任角色 | S-008 | `skills/*/references/*.md` | superseded | 历史五章节、角色专属能力词与目录门禁通过 |
| S-010 | 七份 reference 以既有核心能力重构为按需加载的能力卡 | 七职责任角色 | F-006、D-004 | 七份 `SKILL.md`、七份 reference、校验器与受影响记忆 | superseded | 历史四字段结构曾通过结构校验，但因用户反馈其专业正文更宽泛、细节不足而由 S-011 取代 |
| S-011 | 以改前语义基线恢复七份 reference 的专业执行深度 | 七职责任角色 | F-007、D-005 | 七份 reference、校验器与七职终态记忆 | done | 52 卡、416 字段齐备；旧版独有判断、证据与反例完成迁移；七类结构负向变体、三组语义审计及 fresh 前向场景均通过 |
| S-012 | 将七职项目记忆改为终态事实级增量合并 | 七职责任角色 | F-008、F-009、D-007 | 共享记忆契约、七份 Skill、七份模板、校验器与七份当前记忆 | done | 过程阶段零写入；终态后仅适用且事实变化角色修改受影响条目；既有 schema 1 原样保留，增量与中断 fresh 场景符合契约 |
| S-013 | 七份角色模板改为 schema 2 事实家族索引与通用骨架首建母版 | 七职责任角色 | D-007、S-012 | 七份模板、七份 Skill、七份 reference 与校验器 | done | 全插件 7 份模板各由完整角色事实家族索引与 1 张可复制的十三字段通用骨架组成，不再按家族预铺空卡，共 7 张骨架／91 个字段；delivery 保留 7 个家族。实例化只生成有证据事实，角色专业细节仍唯一保存在对应 `skills/*/references`；既有 schema 1/2 不读取模板且不迁移或重建 |

## 风险与阻塞

| ID | 风险或阻塞 | 触发信号 | 影响 | Owner | 缓解或解除动作 | 状态 |
|---|---|---|---|---|---|---|
| R-001 | 旧显式调用失效 | 外部提示仍使用复合旧名 | 触发失败 | `delivery` | 在 CHANGELOG 记录迁移；不留重复 Skill 壳 | accepted |
| R-002 | 通用单词误触发 | 仅凭名称而忽略 description | 路由精度下降 | 各 Skill | 已以角色化 description、默认提示词及两次前向试用缓解；真实安装后持续观察 | monitored |
| R-003 | 旧、新记忆并存 | 旧文件残留 | 双事实源 | `verification` | 已由精确集合与旧名零残留门禁解除 | resolved |
| R-004 | 外部参考被误记为当前事实 | 仿照页面的品牌、字段或权限语义未经核验即落盘 | 产品或实现偏离 | 各 Skill | 记录精确来源、提取特征、用途、适用性与采纳状态 | mitigated |
| R-005 | Skill 与 reference 再次双写、能力卡退化、细节压缩或引用失效 | 主卷重现详细专业正文、旧四章节复发、八字段缺失、目录替代正文、路径变化或旧版独有判断再次丢失 | 上下文膨胀、能力漂移或专业判断缺失 | `verification` | 校验四章、全部能力 H3、八字段、按需加载和直达引用，并结合语义审计与 fresh 场景防止只满足结构 | mitigated |
| R-006 | 记忆在执行中被反复写入，或终态收口通过整文件重建覆盖仍有效事实 | 出现过程状态、重复命令、无事实增量时间戳、无关章节改写或全覆盖措辞 | 流水账、事实丢失与跨角色契约漂移 | `delivery` / `verification` | 过程零写入、按角色单一所有权、稳定 ID 增量、七职语义锚点与错误模型零命中门禁 | mitigated |
| R-007 | 事实卡只写抽象结论、未结合 reference 补足角色细节，或把模板升级当作迁移授权 | 卡片无法回答主体、前提、关键值、行为、边界、证据或下游约束，或既有记忆出现整卷结构变化 | 后续 AI 仍需猜测项目，旧事实可能丢失或改义 | 七职责任角色 / `verification` | 完整家族索引、一张 13 字段通用骨架、同角色 reference、schema 1 兼容及逐字保留哨兵场景 | mitigated |

## 动作队列

| 优先级 | 动作 | 前置条件 | 责任角色 | 完成判据 |
|---|---|---|---|---|
| P2 | 相关源码变化后重新核验对应记忆事实 | Skill、模板、记忆、manifest 或校验器变化 | 对应责任角色 | 过程阶段文件保持不变；终态且适用验证完成后，仅事实变化角色增量修改受影响条目 |
| P2 | 如需安装或发布，先取得明确授权 | 用户指定制品、环境与动作 | `release` | 授权、门禁与回滚契约齐备 |
| P2 | 能力结构、字段、正文语义或加载方式变化后重验 S-011 | 任一 Skill/reference 或校验器变化 | `verification` | 当前修订重新取得结构、语义、负向、前向与差异证据 |

## 当前验证

| ID | 验证目标 | 命令或制品 | 修订与环境 | 结果及退出码 | 核验时间 | 失效条件 |
|---|---|---|---|---|---|---|
| V-001 | 三处同名集合 | `find skills templates docs/product-studio` | `347c769c5e9b + worktree:7052a4ba756b` | 三组均为七个同名主干，退出码 0 | 2026-07-30T23:03:19+08:00 | 任一目录或文件再次改名 |
| V-002 | 七 Skill 与插件结构 | 七次 `quick_validate.py`、一次 `validate_plugin.py` | 本地 Linux，当前 worktree | 全部通过，退出码 0 | 2026-07-30T23:03:19+08:00 | Skill 或 manifest 变化 |
| V-003 | 项目契约与退化防护 | `python3 scripts/validate_project.py` 与内存负向变体 | 本地 Linux，当前 worktree | 正向通过；命名、同名、统一章节、角色章节、AI 语义及跨记忆矛盾均被拒绝 | 2026-07-30T23:24:38+08:00 | 校验器、模板或记忆变化 |
| V-004 | 新会话角色恢复 | fresh subagent 分别显式使用 `$frontend` 与 `$delivery` | 只读前向试用 | 均读取同名记忆、守住角色边界并给出正确首步 | 2026-07-30T23:03:19+08:00 | Skill 提示词或记忆结构变化 |
| V-005 | 来源契约行为 | 旧硬辞零残留、三类内存负向变体、fresh `$frontend` GitHub 设置页参考场景 | `347c769c5e9b + worktree:7052a4ba756b` | 旧来源禁令被拒绝；链接可分析和仿照且未被误记为当前事实 | 2026-07-30T23:42:45+08:00 | Skill、模板或来源契约变化 |
| V-006 | 最终交付门禁 | `py_compile`、项目校验、七次 Skill Creator 校验、插件校验、`git diff --check` | 本地 Linux，当前 worktree | 全部通过，退出码 0 | 2026-07-30T23:54:16+08:00 | 任一受检文件变化 |
| V-007 | 能力分层门禁 | 项目校验、七次 Skill Creator 校验、插件校验、结构检索与四类内存负向变体 | `347c769c5e9b + worktree:186d7c03e713` | 正向通过；正文回流、引用丢失、证据章节与专属能力缺失均被拒绝 | 2026-07-31T00:22:11+08:00 | Skill、reference 或校验器变化 |
| V-008 | reference 前向行为 | fresh `$backend` 支付捕获幂等与未知态只读设计场景 | 当前 Skill 与能力手册 | 明确读取 reference，并产出并发、恢复、迁移、可观测与验证交接 | 2026-07-31T00:12:40+08:00 | backend Skill 或能力手册变化 |
| V-009 | 四字段能力卡重构 | S-010、四章节与能力卡字段门禁、旧四标题零命中、按需加载、内存负向变体、独立审校及 fresh 前向试用 | `9efef58ddb3f + worktree:78def6775d85`，Windows PowerShell | 历史结构验证通过；随后被用户实读反馈判定为正文更宽泛、没有改前详细，故不能继续作为当前质量证据 | 2026-07-31T10:09:16+08:00 | 已由用户反馈触发失效并被 V-010 取代 |
| V-010 | 八字段专业语义恢复与最终门禁 | S-011、七份 Skill/reference、语义基线审计、七类负向变体、三组独立语义审计及 fresh 场景 | `9efef58ddb3f + worktree:babe95b0ce48`，Windows PowerShell | 通过：52 卡、416 字段、七 refs 共 2255 行；项目校验、七次 Skill Creator、Claude strict、git diff-check 均通过。架构证据、后端顺序/调用图、交付外部材料溯源、前端禁用原因四类缺口已修复并复核；fresh discovery/architecture/backend/verification 输出具体专业裁决。计数仅作完整性旁证，不作为质量门槛 | 2026-07-31T10:49:30+08:00 | 任一 Skill、reference、记忆、校验器或专业语义变化 |
| V-011 | 终态事实级增量记忆契约 | S-012、S-013、共享事实卡契约、七份 Skill／reference／首建模板／当前记忆、校验器与增量哨兵 | `9efef58ddb3f + source-worktree:bfa1d4812af3`，Windows PowerShell | 通过：全插件 7 份模板／7 张可复制骨架／91 个字段及稳定 ID 家族完整，delivery 模板为 7 个家族／1 张骨架／13 个字段，且未按家族预铺空卡；角色专业细节仍唯一保存在对应 `skills/*/references`，实例化只生成有证据事实。`py_compile`、项目校验、七项 `quick_validate.py`、Claude strict、正式决策准入、schema 1/2 兼容、模板复用／全量覆盖／结论极性负向门禁、增量哨兵与 `git diff --check` 均通过；既有记忆按同一事实 ID 原位更新或以最短取代关系新增，不读取模板，也不改无关事实、章节、角色文件与时间戳 | 2026-07-31T14:33:37+08:00 | 记忆写入时机、合并语义、模板、Skill、reference 或校验器变化 |
| V-012 | 分布式角色记忆契约与根 reference 移除 | F-011、D-001、D-002、D-007、D-008、七份 Skill／模板、校验器与强化负向门禁 | `9efef58ddb3f + source-worktree:f0cd0325d657`，Windows PowerShell | 通过：根级 project-memory/platform reference 已删除，跨角色规则归 `delivery` Skill、各角色事实规则归同名 Skill，失败依赖增量不得产生悬空引用；`py_compile`、项目校验、七项 `quick_validate.py`、Claude strict、`git diff --check`、根 reference 路径／路由顺序／禁止代写／项目记忆冲突语义强化负向门禁及 fresh backend/delivery 场景均通过 | 2026-07-31T15:37:46+08:00 | 根 reference 架构、Skill 项目记忆、跨角色路由、失败隔离、校验器或模板变化 |

## 角色记忆收口

| Skill | 影响 | 记忆文件 | verified_revision | 当前证据或说明 |
|---|---|---|---|---|
| `delivery` | 有变化 | `delivery.md` | `9efef58ddb3f + worktree:edbcc2f9564f` | 新增两次用户事实、取代决定、S-012、R-006 与终态增量验证，并汇总七职最终恢复点 |
| `discovery` | 有变化 | `discovery.md` | `9efef58ddb3f + worktree:edbcc2f9564f` | 增量加入记忆更新问题、两次用户事实、当前验收与决定，保留既有产品事实 |
| `architecture` | 有变化 | `architecture.md` | `9efef58ddb3f + worktree:edbcc2f9564f` | 增量记录事实级合并的不变量、ADR 与验证，不改无关架构结论 |
| `frontend` | 有变化 | `frontend.md` | `9efef58ddb3f + worktree:edbcc2f9564f` | 增量记录前端记忆终态写入契约；无运行时 UI 变化 |
| `backend` | 有变化 | `backend.md` | `9efef58ddb3f + worktree:edbcc2f9564f` | 增量记录后端契约事实合并与 Schema 优先边界；无运行时 API 变化 |
| `verification` | 有变化 | `verification.md` | `9efef58ddb3f + worktree:edbcc2f9564f` | 增量记录 7/7 语义锚点、错误模型零命中与两组 fresh 场景证据 |
| `release` | 有变化 | `release.md` | `9efef58ddb3f + worktree:edbcc2f9564f` | 增量记录发布执行结果按条目合并及未授权边界；实际安装与发布仍不在授权范围 |

## 交接与失效

- 建议读取顺序：当前用户指令与 Git 差异 → `delivery.md` → 按任务选读其余同名记忆。
- 下一责任角色：无；后续仅在能力结构、正文语义或项目事实变化，或用户授权安装、发布时重新开启相应流程。
- 必须携带的契约 ID：F-007、F-009、F-010、D-005、D-007、D-008、S-011 至 S-013、AC-012 至 AC-014；D-006 为已取代的短暂全覆盖解释，不得恢复。
- 尚未解决：无源码交付阻塞；真实安装后的触发率仅为可选后续度量，不属于本轮授权范围。
- 重新核验触发器：任一 Skill、模板、记忆、manifest 或校验器变化。
- 本记忆失效条件：受影响事实的证据基线与当前仓库不一致，或用户改变命名、事实卡字段、模板用途、记忆写入时机与事实合并要求；无关 revision 变化不使整份记忆自动失效。
