---
schema: 1
memory: delivery
scope: current-project
project_root: "current product-studio repository"
status: done
updated_at: "2026-07-31T00:22:11+08:00"
verified_at: "2026-07-31T00:22:11+08:00"
verified_revision: "347c769c5e9b + worktree:186d7c03e713"
confidence: high
supersedes: [MIG-001]
---

# delivery

- 固定责任角色：`delivery`（产品交付负责人）
- 项目根：当前 `product-studio` 仓库
- 记忆路径：`docs/product-studio/delivery.md`

## 恢复摘要

- 当前目标：让七份 `SKILL.md` 专注角色约束与执行契约，由各自 `references/` 独立承载详细职责、核心能力和专业决策顺序。
- 当前阶段：七份主 Skill 已删除三段重复正文并建立单层直达引用；七份能力手册已扩展职责、能力、决策、交付证据与常见误判，正向、负向及 fresh `$backend` 前向试用通过。
- 当前结论：角色行为采用“精练 Skill 约束层 + 详细 reference 专业层”；专业知识只保留一份，Skill 明确何时完整加载并把判断绑定当前项目证据。
- 首个可执行动作：后续新增角色能力时先扩展对应 reference，再以 Skill 引用和项目校验确认可达性，不在主 Skill 复制专业正文。
- 阻塞：无源码阻塞；实际安装与发布不在授权范围。

## 原始意图与范围

- 本轮包含：既有命名、记忆与来源契约，以及七职 Skill/reference 职责分层、能力手册扩写、校验器、前向试用与动态记忆收口的本次修正。
- 本轮不包含：插件安装、缓存刷新、Marketplace 外部更新、部署或生产变更。
- 授权边界：可修改并验证当前仓库；不得把源码修改许可外推为外部状态变更许可。

## 依据账本

| ID | 类型 | 内容 | 精确来源 | 置信度 | 状态 | 取代关系 | 失效条件 |
|---|---|---|---|---|---|---|---|
| F-001 | 用户确认 | 每个 Skill 名收紧为一个符合职责的单词 | 本轮用户指令（2026-07-30） | 高 | active | supersedes MIG-001 | 用户另行更改命名策略 |
| F-002 | 用户确认 | 每个 Skill 的项目记忆与 Skill 名一致 | 本轮用户指令（2026-07-30） | 高 | active | 无 | 用户另行指定映射 |
| F-003 | 用户确认 | 记忆模板须提升对 AI 恢复与氛围编程的价值 | 本轮用户指令（2026-07-30） | 高 | active | 无 | 模板目标改变 |
| D-001 | 决定 | 三处命名满足 `skills/<name>/`、`templates/<name>.md`、`docs/product-studio/<name>.md` | `references/project-memory.md` | 高 | active | supersedes MIG-001 | 平台新增别名或命名约束 |
| F-004 | 用户确认 | “只读取”“不得从其他项目继承”等绝对来源措辞会造成上下文缺失，页面仿照等外部参考应可进入分析 | 本轮用户指令（2026-07-30） | 高 | active | supersedes 旧来源白名单措辞 | 用户重新定义来源边界 |
| D-002 | 决定 | 项目根界定事实归属与写入位置；读取范围按任务相关性开放，外部材料以来源、用途、适用性和采纳状态管理 | `references/project-memory.md#信息来源与适用性` | 高 | active | 无 | 来源模型变化 |
| F-005 | 用户确认 | `SKILL.md` 删除职责、核心能力、专业决策顺序，详细专业能力由同角色 reference 承载并被 Skill 引用 | 本轮用户指令（2026-07-31） | 高 | active | supersedes 主卷与 reference 双写 | 用户改变能力分层 |
| D-003 | 决定 | 七职采用约束层与专业层分离；reference 统一包含角色职责、核心能力、专业决策顺序、交付证据与常见误判 | `skills/*/SKILL.md`、`skills/*/references/*.md` | 高 | active | 无 | Skill 资源加载模型变化 |

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
| S-003 | 模板提供高信号恢复、依据、动作、验证和失效信息 | 七职责任角色 | S-002 | 七份模板 | done | AI 模板语义门禁通过 |
| S-004 | 校验器能阻止命名、同名关系与模板价值退化 | `verification` | S-001、S-003 | `scripts/` | done | 正向和负向断言均通过 |
| S-005 | 七职记忆反映当前差异与验证 | 七职责任角色 | S-004 | 七份项目记忆 | done | 收口表与当前证据一致 |
| S-006 | 七职不再把项目隔离写成上下文读取禁令 | 七职责任角色 | F-004 | `skills/`、`references/`、`templates/` | done | 显式外部参考可读且不会自动升级为当前事实 |
| S-007 | 校验器阻止旧硬辞复发并验证来源分层 | `verification` | S-006 | `scripts/` | done | 正向、旧硬辞注入与来源字段缺失变体均符合预期 |
| S-008 | 七份 Skill 移除三段专业正文并建立唯一能力来源 | 七职责任角色 | F-005 | `skills/*/SKILL.md` | done | 旧标题零命中且七个引用均可达 |
| S-009 | 七份 reference 扩展为可执行角色能力手册 | 七职责任角色 | S-008 | `skills/*/references/*.md` | done | 五个统一章节、角色专属能力词与目录门禁通过 |

## 风险与阻塞

| ID | 风险或阻塞 | 触发信号 | 影响 | Owner | 缓解或解除动作 | 状态 |
|---|---|---|---|---|---|---|
| R-001 | 旧显式调用失效 | 外部提示仍使用复合旧名 | 触发失败 | `delivery` | 在 CHANGELOG 记录迁移；不留重复 Skill 壳 | accepted |
| R-002 | 通用单词误触发 | 仅凭名称而忽略 description | 路由精度下降 | 各 Skill | 已以角色化 description、默认提示词及两次前向试用缓解；真实安装后持续观察 | monitored |
| R-003 | 旧、新记忆并存 | 旧文件残留 | 双事实源 | `verification` | 已由精确集合与旧名零残留门禁解除 | resolved |
| R-004 | 外部参考被误记为当前事实 | 仿照页面的品牌、字段或权限语义未经核验即落盘 | 产品或实现偏离 | 各 Skill | 记录精确来源、提取特征、用途、适用性与采纳状态 | mitigated |
| R-005 | Skill 与 reference 再次双写或引用失效 | 主卷重现三项详细章节、路径变化或能力词丢失 | 上下文膨胀、职责漂移或专业判断缺失 | `verification` | 校验分层、直达引用、统一章节及角色能力锚点 | mitigated |

## 动作队列

| 优先级 | 动作 | 前置条件 | 责任角色 | 完成判据 |
|---|---|---|---|---|
| P2 | 相关源码变化后重新核验七份同名记忆 | Skill、模板、记忆、manifest 或校验器变化 | 对应责任角色 | 受影响记忆先变为 `stale`，再以新证据收口 |
| P2 | 如需安装或发布，先取得明确授权 | 用户指定制品、环境与动作 | `release` | 授权、门禁与回滚契约齐备 |

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

## 角色记忆收口

| Skill | 影响 | 记忆文件 | verified_revision | 当前证据或说明 |
|---|---|---|---|---|
| `delivery` | 有变化 | `delivery.md` | `347c769c5e9b + worktree:186d7c03e713` | 编排职责、能力来源与本轮收口证据已更新 |
| `discovery` | 有变化 | `discovery.md` | `347c769c5e9b + worktree:186d7c03e713` | 产品职责与能力分层验收标准已更新 |
| `architecture` | 有变化 | `architecture.md` | `347c769c5e9b + worktree:186d7c03e713` | Skill 约束层与 reference 专业层决定已更新 |
| `frontend` | 有变化 | `frontend.md` | `347c769c5e9b + worktree:186d7c03e713` | 前端能力来源与扩展手册证据已更新；无运行时 UI 变化 |
| `backend` | 有变化 | `backend.md` | `347c769c5e9b + worktree:186d7c03e713` | 后端能力来源、扩展手册与前向试用已验证；无运行时 API 变化 |
| `verification` | 有变化 | `verification.md` | `347c769c5e9b + worktree:186d7c03e713` | 能力分层正向、负向与前向证据均通过 |
| `release` | 有变化 | `release.md` | `347c769c5e9b + worktree:186d7c03e713` | 发布能力来源与扩展手册已验证；实际发布仍不适用 |

## 交接与失效

- 建议读取顺序：当前用户指令与 Git 差异 → `delivery.md` → 按任务选读其余同名记忆。
- 下一责任角色：无；本轮源码交付已收口。后续相关变化由对应同名 Skill 先复核其记忆。
- 必须携带的契约 ID：F-005、D-003、AC-009、AC-010、ADR-006。
- 尚未解决：真实安装后的触发率仅为可选后续度量，不属于本轮授权与源码验收范围。
- 重新核验触发器：任一 Skill、模板、记忆、manifest 或校验器变化。
- 本记忆失效条件：`verified_revision` 与当前仓库不一致，或用户改变命名与模板要求。
