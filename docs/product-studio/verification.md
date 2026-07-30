---
schema: 1
memory: verification
scope: current-project
project_root: "current product-studio repository"
status: done
updated_at: "2026-07-31T00:22:11+08:00"
verified_at: "2026-07-31T00:22:11+08:00"
verified_revision: "347c769c5e9b + worktree:186d7c03e713"
confidence: high
supersedes: [MIG-001]
---

# verification

- 固定责任角色：`verification`（独立验收负责人）
- 项目根：当前 `product-studio` 仓库
- 记忆路径：`docs/product-studio/verification.md`

## 恢复摘要

- 当前验收对象：既有命名、记忆与来源契约，以及七职 Skill/reference 职责分层、能力手册扩写、引用与校验器差异。
- 总体结论：通过；本结论仅覆盖 `347c769c5e9b + worktree:186d7c03e713` 的源码范围。
- 首个可执行验证：后续任一相关文件变化后，先运行项目校验，再逐 Skill 验证受影响角色。
- 阻塞：无源码阻塞；真实安装与发布未获授权，且不属于本轮验收范围。

## 验收对象

- 原始意图来源：本轮用户指令（2026-07-30）。
- 差异或制品：当前工作区中 `skills/`、`templates/`、`docs/product-studio/`、references、README、scripts 与 UI 元数据。
- Git / 制品修订：`347c769c5e9b + worktree:186d7c03e713`。
- 环境：本地 Linux 工作区；未安装或发布插件。
- 适用记忆：七份同名项目记忆。

## 依据账本

| ID | 类型 | 内容 | 精确来源 | 置信度 | 状态 | 取代关系 | 失效条件 |
|---|---|---|---|---|---|---|---|
| F-001 | 用户确认 | AC-001 至 AC-010 均为必需验收范围 | `discovery.md#验收标准` | 高 | active | 无 | 用户缩减范围 |
| F-002 | 仓库事实 | Skill Creator 与项目校验器可提供结构证据，前向场景提供行为证据 | 校验脚本与 fresh subagent | 高 | active | 无 | 工具不可用 |
| F-003 | 用户确认 | “只读取”“不得从”等来源白名单式措辞会造成上下文缺失，其他位置的同类问题也须修正 | 本轮用户指令（2026-07-30） | 高 | active | supersedes 旧来源白名单措辞 | 用户改变来源模型 |
| F-004 | 用户确认 | 七份 Skill 删除职责、核心能力、专业决策顺序，角色 reference 按原核心能力详细扩充并由 Skill 引用 | 本轮用户指令（2026-07-31） | 高 | active | supersedes 主卷/reference 双写 | 用户改变能力分层 |

## 要求与证据矩阵

| AC-ID | Requirement source | Implementation | Current evidence | Result | Evidence expires when |
|---|---|---|---|---|---|
| AC-001 | `discovery.md` | 七个 `skills/<name>/` | 精确集合、单词正则与七次 `quick_validate.py` 均通过 | passed | 任一 Skill 改名 |
| AC-002 | `discovery.md` | 七份同名模板与项目记忆 | Skill / template / memory 三处集合恒等断言通过 | passed | 任一文件改名 |
| AC-003 | `discovery.md` | 七份 `agents/openai.yaml` | 官方生成器产物经逐职 YAML、身份与 `$<skill>` 断言通过 | passed | 默认提示词变化 |
| AC-004 | `discovery.md` | 七份 AI 记忆模板 | 统一骨架、专属章节与 AI 语义正向通过；五种内存破坏变体均被拒绝 | passed | 模板变化 |
| AC-005 | `discovery.md` | 全仓引用 | 活跃路径旧名检索零命中，校验器旧名门禁通过 | passed | 新增旧引用 |
| AC-006 | `discovery.md` | 完整差异与七职记忆 | 项目 / 插件校验、`py_compile`、diff 检查、两次前向试用与独立一致性审校通过 | passed | 任一相关差异变化 |
| AC-007 | `discovery.md` | 七职 Skill 与模板的来源分层 | 当前项目事实、带来源外部参考、适用性与采纳状态语义门禁通过 | passed | 任一来源契约变化 |
| AC-008 | `discovery.md` | 活跃提示词与来源退化防护 | 旧硬辞零残留；注入旧硬辞、删除来源字段的内存变体均被拒绝 | passed | 新增绝对来源限制或校验器变化 |
| AC-009 | `discovery.md` | 七份 Skill 的专业能力来源 | 三个旧标题零命中、七个直达引用存在；正文回流与引用丢失变体被拒绝 | passed | 任一 Skill 结构或引用变化 |
| AC-010 | `discovery.md` | 七份详细角色能力手册 | 五个统一章节、全部原能力词与百行以上目录通过；证据章节/专属能力缺失变体被拒，fresh `$backend` 行为通过 | passed | 任一 reference 或校验器变化 |

## 失败分类

| ID | 分类 | 现象 | 责任角色 | 复现证据 | 状态 |
|---|---|---|---|---|---|
| E-001 | 已解除 | 初始阶段缺少新命名最终证据 | `verification` | AC-001 至 AC-006 当前证据齐备 | resolved |

## 动作队列

| 优先级 | 动作 | 前置条件 | 责任角色 | 完成判据 |
|---|---|---|---|---|
| P2 | 任一相关源码、模板、记忆或 manifest 变化后重跑 AC-001 至 AC-010 | 当前证据失效 | `verification` | 新修订重新取得通过结论 |

## 当前验证

| ID | 验证目标 | 命令或制品 | 修订与环境 | 结果及退出码 | 核验时间 | 失效条件 |
|---|---|---|---|---|---|---|
| V-001 | 项目静态契约 | `python3 -m py_compile scripts/validate_project.py`；`python3 scripts/validate_project.py` | 本地 Linux，`347c769c5e9b + worktree:7052a4ba756b` | 通过，退出码 0 | 2026-07-30T23:03:19+08:00 | 校验器或受检文件变化 |
| V-002 | 七 Skill 与插件规范 | 七次 `quick_validate.py`；一次 `validate_plugin.py` | 官方本地 skill / plugin 工具 | 全部通过，退出码 0 | 2026-07-30T23:03:19+08:00 | Skill 或 manifest 变化 |
| V-003 | 退化防护 | 内存中破坏单词名、同名字段、统一章节、角色章节、AI 语义及跨记忆状态 | 不改当前工作区 | 五个模板/命名变体与一个跨记忆矛盾均被拒绝 | 2026-07-30T23:24:38+08:00 | 校验器逻辑变化 |
| V-004 | 角色恢复与按需编排 | fresh subagent 使用 `$frontend`、`$delivery` 的只读前向试用 | 当前 Skill 与同名记忆 | 能定位同名记忆、守住边界、选出正确角色链与首步 | 2026-07-30T23:03:19+08:00 | Skill 提示词或记忆变化 |
| V-005 | 七职语义一致性 | 独立只读审校与修正后项目复验 | `347c769c5e9b + worktree:7052a4ba756b` | 修正 release 对 verification 的陈旧未来态；其余要求通过 | 2026-07-30T23:24:38+08:00 | 任一项目记忆变化 |
| V-006 | 来源契约正向与负向 | 项目校验、旧硬辞检索、内存注入旧硬辞及删除来源字段变体 | 本地 Linux，当前 worktree | 正向通过；三类来源退化均被拒绝 | 2026-07-30T23:42:45+08:00 | Skill、模板、共享契约或校验器变化 |
| V-007 | 外部页面前向行为 | fresh `$frontend` 规划仿照 GitHub 设置页，只读执行 | 当前 Skill 与同名记忆 | 接受链接为外部参考；登录阻断透明呈现，未臆造或静默采纳页面细节 | 2026-07-30T23:42:45+08:00 | Skill 来源语义或场景证据变化 |
| V-008 | 最终全量回归 | `py_compile`、项目校验、七次 Skill Creator 校验、插件校验、`git diff --check` | 本地 Linux，`347c769c5e9b + worktree:7052a4ba756b` | 全部通过，退出码 0 | 2026-07-30T23:54:16+08:00 | 任一受检文件或环境变化 |
| V-009 | 能力分层正向与负向 | 项目校验、七次 Skill Creator、插件校验、结构检索与四类内存变体 | 本地 Linux，`347c769c5e9b + worktree:186d7c03e713` | 全部正向通过；正文回流、引用丢失、证据章节和角色能力缺失均被拒绝 | 2026-07-31T00:22:11+08:00 | Skill、reference 或校验器变化 |
| V-010 | reference 前向行为 | fresh `$backend` 支付捕获幂等、并发与未知态只读场景 | 当前 Skill、reference 与项目记忆 | 明确报告所读资源，产出状态、约束、迁移、恢复、可观测与验证证据 | 2026-07-31T00:12:40+08:00 | backend 能力来源或前向场景变化 |

## 最终结论

- 结论：通过
- 结论依据：AC-001 至 AC-010 的正向、负向与前向证据均满足；七职项目记忆已按当前 worktree 动态收口。
- 未通过或阻塞项：无源码项。
- 剩余风险：通用单词的真实插件触发率只能在安装后的新会话中度量，本轮未授权安装。

## 交接与失效

- 应退回角色：无；后续差异由对应责任 Skill 先更新，再交本角色重验。
- 必须携带的证据 ID：AC-001 至 AC-010、ADR-002 至 ADR-006。
- 尚未解决：真实安装后的触发率为可选度量；本轮没有安装或发布授权。
- 重新核验触发器：任何相关源码、模板、记忆、manifest 或校验器变化。
- 本记忆失效条件：验收对象修订或环境变化。
