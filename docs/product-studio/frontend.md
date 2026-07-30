---
schema: 1
memory: frontend
scope: current-project
project_root: "current product-studio repository"
status: done
updated_at: "2026-07-31T00:22:11+08:00"
verified_at: "2026-07-31T00:22:11+08:00"
verified_revision: "347c769c5e9b + worktree:186d7c03e713"
confidence: high
supersedes: [MIG-001]
---

# frontend

- 固定责任角色：`frontend`（前端与体验负责人）
- 项目根：当前 `product-studio` 仓库
- 记忆路径：`docs/product-studio/frontend.md`

## 恢复摘要

- 当前用户任务：让 `$frontend` 主卷只定义约束和执行契约，由前端能力手册完整承载体验职责与专业判断。
- 当前界面结论：本轮没有产品运行时 UI 变化；前端 reference 已扩展任务效率、交互、信息架构、响应式、视觉、可访问性、状态工程、性能与真实渲染证据。
- 首个可执行动作：真实 UI 任务进入时先由 Skill 加载能力手册，再把相关专业判断映射到用户任务、状态矩阵、实现与浏览器证据。
- 阻塞：无；真实安装后的 UI 触发验证未获授权。

## 输入来源与适用性

| 来源 ID | 类型 | 记忆、路径或链接 | 提取内容与用途 | 采纳状态 | verified_revision | 失效条件 |
|---|---|---|---|---|---|---|
| SRC-001 | 当前项目事实 | `discovery.md` AC-001..010 | 一词命名、同名文件、来源分层与能力分层验收 | adopted | `347c769c5e9b + worktree:186d7c03e713` | 产品标准变化 |
| SRC-002 | 当前项目事实 | `architecture.md` ADR-002..006 | 使用 `$frontend`、AI 恢复骨架、来源分层及 Skill/reference 两层契约 | adopted | `347c769c5e9b + worktree:186d7c03e713` | 架构决定被取代 |
| SRC-003 | 外部参考 | `https://github.com/settings/profile`，fresh `$frontend` 前向测试输入 | 目标页跳转登录，受保护界面细节未被观察；仅以导航层级、带标签表单和完整状态作为候选设计方向 | reference-only | `347c769c5e9b + worktree:7052a4ba756b` | 获得可访问页面、截图或用户明确采纳 |

## 依据账本

| ID | 类型 | 内容 | 精确来源 | 置信度 | 状态 | 取代关系 | 失效条件 |
|---|---|---|---|---|---|---|---|
| F-001 | 仓库事实 | 本仓库没有本轮需渲染的运行时前端界面 | `.codex-plugin/`、`skills/`、`templates/` 目录边界 | 高 | active | 无 | 新增运行时 UI |
| D-001 | 决定 | 前端模板聚焦用户任务、输入来源、状态矩阵、交互/可访问性、实现映射与真实渲染证据 | `templates/frontend.md` | 高 | active | 旧综合功能规格模板 | 模板职责改变 |
| D-002 | 决定 | 显式页面、截图与设计稿可供读取、分析和仿照；品牌、字段、文案、权限与未观察细节保持参考或未知，直至当前项目证据采纳 | `skills/frontend/SKILL.md`、ADR-005 | 高 | active | 旧来源白名单措辞 | 来源模型变化 |
| D-003 | 决定 | 前端职责、八项核心能力、决策顺序、证据与误判唯一存于 `frontend-design-principles.md`，Skill 只保存直达入口和工作约束 | `skills/frontend/`、ADR-006 | 高 | active | 主卷三段专业正文 | 能力手册或加载模型变化 |

## 实现映射

| 行为或状态 | 文件 / 组件 / Symbol | 数据依赖 | 状态来源 | 测试位置 | Owner |
|---|---|---|---|---|---|
| `$frontend` 角色触发 | `skills/frontend/SKILL.md` | 无 | frontmatter description | Skill 快速校验、项目校验 | `frontend` |
| Codex 默认入口 | `skills/frontend/agents/openai.yaml` | 无 | `default_prompt` | 项目 YAML 断言 | `frontend` |
| 前端项目记忆骨架 | `templates/frontend.md` | `discovery.md`、`backend.md` 引用 | memory schema 1 | 模板语义门禁 | `frontend` |
| 前端专业能力 | `skills/frontend/references/frontend-design-principles.md` | 当前产品、设计系统与实现证据 | Skill 直达引用 | 结构、角色能力词与前向行为门禁 | `frontend` |

## 动作队列

| 优先级 | 动作 | 前置条件 | 责任角色 | 完成判据 |
|---|---|---|---|---|
| P2 | 真实 UI 或上游契约变化后重验前端记忆 | 新界面差异或 AC / ADR 变化 | `frontend` | 状态矩阵、实现映射与渲染证据反映当前修订 |

## 当前验证

| ID | 验证目标 | 命令或制品 | 修订与环境 | 结果及退出码 | 核验时间 | 失效条件 |
|---|---|---|---|---|---|---|
| V-001 | 前端影响边界与角色恢复 | 当前工作区差异、Skill / 模板门禁、fresh `$frontend` 前向试用 | `347c769c5e9b + worktree:7052a4ba756b` | 无运行时 UI 变化；新会话读取同名记忆并将缺失产品语义退回 `discovery` | 2026-07-30T23:03:19+08:00 | 新增运行时前端文件或 Skill 提示词变化 |
| V-002 | 外部页面参考行为 | fresh `$frontend` 使用 GitHub 设置页仿照场景 | 只读前向试用，当前 Skill 与记忆 | 页面可作为外部参考；登录阻断被明确记录，未臆造受保护界面，也未把品牌、字段和权限语义记作当前事实 | 2026-07-30T23:42:45+08:00 | Skill 来源语义或参考页面证据变化 |
| V-003 | 前端来源契约回归 | frontend Skill Creator 校验、项目校验与三类来源负向变体 | 本地 Linux，当前 worktree | 正向通过；旧硬辞与来源字段缺失均被拒绝 | 2026-07-30T23:54:16+08:00 | frontend Skill、模板、记忆或校验器变化 |
| V-004 | 前端能力分层 | frontend Skill Creator、项目校验、旧标题零命中、reference 五章节与角色能力词 | `347c769c5e9b + worktree:186d7c03e713` | 主卷无重复，155 行能力手册可达且语义门禁通过 | 2026-07-31T00:22:11+08:00 | frontend Skill 或能力手册变化 |

## 交接与失效

- 下游先读：`discovery.md` 的 AC-001 至 AC-010、`architecture.md` 的 ADR-002 至 ADR-006。
- 已知体验缺口：未在已安装插件 UI 中实测触发显示；本轮不安装。
- 尚未解决：真实安装插件后的 UI 展示仅为可选后续度量。
- 重新核验触发器：前端 Skill、默认提示词、模板或 manifest 变化。
- 本记忆失效条件：出现运行时 UI 改动或上游产品/接口契约变化。
