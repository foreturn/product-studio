---
schema: 1
memory: backend
scope: current-project
project_root: "current product-studio repository"
status: done
updated_at: "2026-07-31T00:22:11+08:00"
verified_at: "2026-07-31T00:22:11+08:00"
verified_revision: "347c769c5e9b + worktree:186d7c03e713"
confidence: high
supersedes: [MIG-001]
---

# backend

- 固定责任角色：`backend`（后端负责人）
- 项目根：当前 `product-studio` 仓库
- 记忆路径：`docs/product-studio/backend.md`

## 恢复摘要

- 当前后端目标：让 `$backend` 主卷只定义约束和执行契约，由后端能力手册完整承载领域、API、数据、安全、一致性、可靠性、可观测性与测试判断。
- 当前契约结论：本轮没有运行时 API、Schema、数据库、权限或数据变化；153 行后端 reference 已成为专业能力唯一详细来源，并通过 fresh 支付捕获场景。
- 首个可执行动作：真实后端任务进入时先由 Skill 加载能力手册，再把判断绑定权威 Schema、调用方、迁移、失败恢复和验证证据。
- 阻塞或不适用原因：运行时后端契约不适用，依据为仓库差异中无业务服务端文件。

## 输入来源与适用性

| 来源 ID | 类型 | 记忆、Schema、路径或链接 | 提取内容与用途 | 采纳状态 | verified_revision | 失效条件 |
|---|---|---|---|---|---|---|
| SRC-001 | 当前项目事实 | `discovery.md` AC-001..010 | 一词命名、同名文件、来源分层与能力分层验收 | adopted | `347c769c5e9b + worktree:186d7c03e713` | 产品标准变化 |
| SRC-002 | 当前项目事实 | `architecture.md` ADR-002..006 | 使用 `$backend`、Schema 优先、来源分层及 Skill/reference 两层契约 | adopted | `347c769c5e9b + worktree:186d7c03e713` | 架构决定被取代 |

## 依据账本

| ID | 类型 | 内容 | 精确来源 | 置信度 | 状态 | 取代关系 | 失效条件 |
|---|---|---|---|---|---|---|---|
| F-001 | 仓库事实 | 当前仓库是插件指令与模板工程，本轮无运行时 API 或数据实现 | 当前 Git 差异 | 高 | active | 无 | 出现业务后端差异 |
| D-001 | 决定 | 无后端影响时只记影响判断、依据与重新适用条件，不铺设空 API 章节 | `templates/backend.md` | 高 | active | 旧空壳契约写法 | 出现真实 API 变化 |
| D-002 | 决定 | 外部 API 文档、协议与参考实现可参与方案分析；当前项目 Schema、调用链、实现与验证证据决定契约采纳状态 | `skills/backend/SKILL.md`、ADR-005 | 高 | active | 旧来源白名单措辞 | 来源模型变化 |
| D-003 | 决定 | 后端职责、八项核心能力、决策顺序、证据与误判唯一存于 `backend-design-principles.md`，Skill 只保存直达入口和工作约束 | `skills/backend/`、ADR-006 | 高 | active | 主卷三段专业正文 | 能力手册或加载模型变化 |

## 动作队列

| 优先级 | 动作 | 前置条件 | 责任角色 | 完成判据 |
|---|---|---|---|---|
| P2 | 真实后端差异或上游契约变化后重验本记忆 | API、Schema、权限、数据或 ADR 变化 | `backend` | 契约、不变量、恢复、迁移与调用方证据反映当前修订 |

## 当前验证

| ID | 验证目标 | 命令或制品 | 修订与环境 | 结果及退出码 | 核验时间 | 失效条件 |
|---|---|---|---|---|---|---|
| V-001 | 运行时契约影响与 Skill 结构 | 当前工作区差异、七 Skill / 插件 / 项目门禁 | `347c769c5e9b + worktree:7052a4ba756b` | `$backend`、同名文件与专属模板通过；无运行时后端变化 | 2026-07-30T23:03:19+08:00 | 出现 API、Schema、迁移或数据差异 |
| V-002 | 后端来源分层 | Skill / 模板来源语义正向门禁与旧硬辞注入负向变体 | `347c769c5e9b + worktree:7052a4ba756b` | 外部契约材料可作参考，缺少来源或自动升级为当前事实的退化会被识别 | 2026-07-30T23:42:45+08:00 | Skill、模板或校验器变化 |
| V-003 | 后端来源契约回归 | backend Skill Creator 校验、项目校验与完整差异复核 | 本地 Linux，当前 worktree | 结构与来源分层通过，退出码 0；仍无运行时后端变化 | 2026-07-30T23:54:16+08:00 | backend Skill、模板、Schema 或实现变化 |
| V-004 | 后端能力分层与行为 | backend Skill Creator、项目校验、四类负向变体、fresh 支付捕获场景 | `347c769c5e9b + worktree:186d7c03e713` | 主卷无重复；新会话读取 reference 并给出幂等、并发、未知态恢复、迁移与测试交接 | 2026-07-31T00:22:11+08:00 | backend Skill 或能力手册变化 |

## 交接与失效

- 调用方先读：`discovery.md` 的 AC-001 至 AC-010、`architecture.md` 的 ADR-002 至 ADR-006。
- 尚未解决：无；真实后端变更不在本轮差异内。
- 重新核验触发器：后端 Skill、模板、默认提示词或权威 Schema 变化。
- 本记忆失效条件：出现运行时 API、数据、权限、迁移或调用方变化。
