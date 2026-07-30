---
schema: 1
memory: architecture
scope: current-project
project_root: "current product-studio repository"
status: done
updated_at: "2026-07-31T00:22:11+08:00"
verified_at: "2026-07-31T00:22:11+08:00"
verified_revision: "347c769c5e9b + worktree:186d7c03e713"
confidence: high
supersedes: [MIG-001]
---

# architecture

- 固定责任角色：`architecture`（系统架构师）
- 项目根：当前 `product-studio` 仓库
- 记忆路径：`docs/product-studio/architecture.md`

## 恢复摘要

- 当前架构问题：角色约束与详细专业知识同存于 `SKILL.md`，又在 reference 重复，导致上下文膨胀和双写漂移。
- 当前有效决定：七职采用两层契约，Skill 只保存触发、约束与工作流，reference 是职责、核心能力、专业决策、证据与误判的唯一详细来源。
- 首个可执行动作：相关结构变化时，从 INV-001 至 INV-007 重验 Skill/reference 引用、章节归属与角色能力锚点，并复核 ADR-002 至 ADR-006。
- 阻塞：无。

## 依据账本

| ID | 类型 | 内容 | 精确来源 | 置信度 | 状态 | 取代关系 | 失效条件 |
|---|---|---|---|---|---|---|---|
| F-001 | 仓库事实 | 双端 manifest 均从 `./skills/` 自动发现 Skill | `.codex-plugin/plugin.json`、`.claude-plugin/plugin.json` | 高 | active | 无 | manifest schema 变化 |
| F-002 | 仓库事实 | 项目根已提供记忆隔离，固定目录为 `docs/product-studio/` | `references/project-memory.md` | 高 | active | 无 | 记忆根策略变化 |
| D-001 | 决定 | 名称恒等式为 `skill == template stem == memory stem` | 本文件 ADR-002 | 高 | active | supersedes MIG-001 | 平台增加强制命名 |
| D-002 | 决定 | 项目根界定当前事实与记忆归属，不界定全部可读上下文 | 本文件 ADR-005 | 高 | active | supersedes 旧来源白名单措辞 | 来源模型变化 |
| D-003 | 决定 | 角色约束规范与专业能力采用单向引用的两层契约 | 本文件 ADR-006 | 高 | active | supersedes Skill/reference 双写 | Skill 资源模型变化 |

## 架构上下文

- 共享内核：七个 `skills/<name>/SKILL.md`、角色 references 与七份 `templates/<name>.md`。
- 平台适配：Codex 使用 `agents/openai.yaml`，Claude Code 共享 SKILL.md 与插件 manifest。
- 项目状态：目标项目在自身 `docs/product-studio/` 保存七份同名记忆；外部项目材料保持可追溯的参考身份，经当前项目核验后再形成适用决定。

## 不变量与质量属性

| ID | 不变量或质量目标 | 优先级 | 证据 | 破坏后果 | 验证方式 |
|---|---|---|---|---|---|
| INV-001 | 每个 Skill、模板、记忆三处主干名完全一致 | P0 | 用户指令 | 阅读映射成本与漂移复发 | 集合恒等断言 |
| INV-002 | Skill 名匹配 `^[a-z][a-z0-9]*$` 且七名唯一 | P0 | 用户指令、Skill 规范 | 非单词名或触发冲突 | 正则与唯一性检查 |
| INV-003 | 每份记忆的持久化更新由同名 Skill 负责；跨角色发现以证据交接给该 Owner | P0 | `references/project-memory.md` | 双事实源 | owner 与 frontmatter 门禁 |
| INV-004 | 旧记忆与旧调用不作为活跃兼容层保留 | P0 | 单一真相原则 | 重复触发和双写 | 零残留检查 |
| INV-005 | 当前用户指令、仓库与运行证据决定当前事实；读取任务与持久写入授权分别判断，秘密值不属于记忆正文 | P0 | 既有安全契约 | 陈旧事实或敏感泄露 | Skill 与模板语义门禁 |
| INV-006 | 外部材料可按任务读取、比较或仿照，并保留精确来源、用途、适用性与采纳状态；参考身份不会自动升级为当前事实 | P0 | 用户指令、`references/project-memory.md` | 上下文缺失或事实污染 | 来源语义与前向场景门禁 |
| INV-007 | `SKILL.md` 不保存职责、核心能力、专业决策顺序正文；每个 Skill 直达一个同角色 reference，reference 保留五个统一章节和全部角色能力锚点 | P0 | 用户指令、Skill Creator 渐进披露原则 | 双写漂移或专业上下文缺失 | 结构、语义与负向门禁 |

## 边界与所有权

| 边界 | Owner | 输入 | 输出 | 来源与归属约束 | 受影响调用方 |
|---|---|---|---|---|---|
| Skill 触发 | 各 Skill | frontmatter description | 对应角色行为 | 其他角色决策权 | Codex、Claude Code |
| 项目记忆 | 同名 Skill | 当前仓库事实、验证与带来源的外部参考 | `docs/product-studio/<name>.md` | 外部材料保留参考身份；秘密值不属于正文 | 后续会话与下游角色 |
| 模板 | 同名 Skill | 可复用结构 | `templates/<name>.md` | 当前项目具体事实 | 首次记忆创建者 |
| 专业能力 | 同名 reference | 角色领域知识 | `skills/<name>/references/*.md` | Skill 单向引用，专业正文唯一维护 | 触发后的角色 Skill |

## 决策索引

| ADR | Status | Decision | Reason | Affected boundaries | Supersedes | Revisit when |
|---|---|---|---|---|---|---|
| ADR-001 | accepted | 继续使用当前项目固定记忆根 `docs/product-studio/` | 项目根已经隔离，目录无需产品层 | 项目记忆 | 无 | 多项目工作区需要显式协调 |
| ADR-002 | accepted | 七职使用 `delivery / discovery / architecture / frontend / backend / verification / release`，模板与记忆严格同名 | 可读、可推导、消除单复数和语义映射 | Skill、模板、记忆、提示词、校验器 | MIG-001 | 用户指定别名机制或出现触发冲突 |
| ADR-003 | accepted | 记忆模板采用 schema、revision、恢复摘要、依据、动作、验证、失效和角色专属章节 | AI 可快速判断何为真、下一步和何时重验 | 七份模板与项目记忆 | 旧报告式模板 | 恢复测试显示信息仍不足或冗余 |
| ADR-004 | accepted | 不保留旧名转发 Skill 或旧记忆副本 | 避免重复触发与双事实源 | 兼容策略 | 旧“名称保持兼容”决定 | 平台提供正式 alias 且用户要求兼容 |
| ADR-005 | accepted | 将当前项目事实、外部参考与已采纳决定分层；项目根用于事实归属和持久化隔离，而非上下文读取白名单 | 支持显式页面仿照与跨来源分析，同时保持项目事实可追溯 | 七职 Skill、模板、共享契约与校验器 | 旧绝对来源限制 | 来源分层仍造成遗漏或误采纳 |
| ADR-006 | accepted | 将职责、核心能力和专业决策顺序从七份 Skill 移至同角色 reference；Skill 以“专业能力来源”单向引用 | 主提示词保持精练，专业知识详细且只有一个真相源 | 七职 Skill、reference、README 与校验器 | Skill/reference 双写 | 平台资源加载或角色能力组织方式变化 |

## 候选方案与权衡

| ADR | 方案 | 收益 | 代价与风险 | 结论 |
|---|---|---|---|---|
| ADR-002 | 单词领域名词 | 短、可读、角色语义稳定 | 通用名可能误触发 | 采用，以精确 description 缓解 |
| ADR-002 | 单词动词 | 行动导向 | `architect`、`discover` 与记忆名不如领域名自然 | 不采用 |
| ADR-004 | 保留旧目录作转发 | 兼容旧调用 | Skill 数翻倍、触发与记忆所有权歧义 | 不采用 |
| ADR-005 | 项目材料作为唯一可读来源 | 事实边界简单 | 丢失用户显式参考与外部上下文，无法可靠仿照或比较 | 不采用 |
| ADR-005 | 来源分层并显式记录采纳状态 | 上下文完整且事实身份清晰 | 需要多记录来源与适用性 | 采用 |
| ADR-006 | Skill 保留能力摘要，reference 再写细则 | 首屏可见能力名 | 重复内容会漂移，AI 不清楚以何处为准 | 不采用 |
| ADR-006 | Skill 只给约束与直达引用，reference 完整定义专业能力 | 渐进披露、单一真相且易扩展 | 运行时必须正确加载引用 | 采用，以校验和前向试用守护 |

## 失败模式

| ID | 触发条件 | 影响 | 检测信号 | 隔离或恢复动作 | Owner |
|---|---|---|---|---|---|
| FM-001 | 任一旧名残留在活跃提示词 | 触发失败 | 旧名检索命中 | 更新引用并重跑校验 | `verification` |
| FM-002 | 模板或记忆主干名与 Skill 不同 | AI 无法直接定位 | 三处集合不等 | 从 Skill 集合派生路径 | `architecture` |
| FM-003 | `done` 结论对应旧 revision | AI 沿用陈旧证据 | revision 不匹配 | 标记 stale 并重验 | 各 Skill |
| FM-004 | 不适用角色生成完整空壳 | 上下文噪声 | 空表或孤立占位 | 只记原因、依据与重启条件 | 各 Skill |
| FM-005 | 将外部页面静默当作当前实现事实，或因项目隔离拒绝读取 | 产品偏离或上下文缺失 | 缺少来源、用途、适用性或采纳状态 | 恢复参考身份并以当前项目证据重新核验 | 各 Skill |
| FM-006 | Skill 重现三段专业正文、reference 缺章节或直达路径失效 | 上下文重复或角色只能凭常识判断 | 结构门禁、角色能力词或前向试用失败 | 恢复单向引用并在 reference 补齐唯一专业定义 | `architecture` / `verification` |

## 迁移与回滚

| Step | 前置条件 | 向前动作 | 兼容窗口 | 回滚触发器 | 回滚动作 |
|---|---|---|---|---|---|
| M-001 | ADR-002 已接受 | 原子迁移七个 Skill、模板与记忆，并更新全仓引用 | 无双写窗口 | 新命名无法被平台发现 | 仅在用户确认后恢复旧命名 |
| M-002 | 新 frontmatter 就绪 | 重新生成七份 Codex UI 元数据 | 同一变更集 | 默认提示词未调用新 Skill | 修复元数据后再验收 |
| M-003 | 模板重构完成 | 校验三处同名、模板语义和旧名零残留 | 同一变更集 | 任一门禁失败 | 保持未完成并修正，不保留两套文件 |
| M-004 | ADR-006 已接受 | 先扩充七份 reference，再删除 Skill 三段正文并加入直达引用，最后切换校验器 | 同一变更集 | 前向试用未读取 reference 或专业判断退化 | 恢复结构门禁并修正引用/能力内容，不双写两套正文 |

## 动作队列

| 优先级 | 动作 | 前置条件 | 责任角色 | 完成判据 |
|---|---|---|---|---|
| P2 | Skill 发现、命名、模板 schema 或记忆根变化时重审不变量 | 边界变化 | `architecture` | 新决定有 ADR、迁移与回滚证据 |

## 当前验证

| ID | 验证目标 | 命令或制品 | 修订与环境 | 结果及退出码 | 核验时间 | 失效条件 |
|---|---|---|---|---|---|---|
| V-001 | 命名与记忆架构完整性 | ADR-001 至 ADR-004、项目校验器正向与负向断言 | `347c769c5e9b + worktree:7052a4ba756b` | 四项决定均已实现并回证 | 2026-07-30T23:42:45+08:00 | 用户或平台命名约束变化 |
| V-002 | 来源分层架构 | ADR-005、INV-006、来源语义门禁与 `$frontend` 外部页面前向场景 | `347c769c5e9b + worktree:7052a4ba756b` | 外部材料可进入上下文且未自动升级为当前事实 | 2026-07-30T23:42:45+08:00 | 来源契约或角色提示词变化 |
| V-003 | 架构契约回归 | 项目校验、七次 Skill Creator 校验与插件校验 | 本地 Linux，当前 worktree | ADR-001 至 ADR-005 对应结构均通过，退出码 0 | 2026-07-30T23:54:16+08:00 | Skill、模板、记忆根或校验器变化 |
| V-004 | 能力分层架构 | ADR-006、INV-007、七份能力手册、四类负向变体与 fresh `$backend` 前向场景 | `347c769c5e9b + worktree:186d7c03e713` | 单向引用与唯一专业来源成立，AI 已实际读取并运用 reference | 2026-07-31T00:22:11+08:00 | Skill/reference 结构或加载模型变化 |

## 交接与失效

- 实现角色先读的 ADR / INV：ADR-002、ADR-003、ADR-005、ADR-006、INV-001 至 INV-007。
- 尚未解决：真实平台安装后的触发冲突率，本轮不安装故作为后续度量。
- 重新核验触发器：Skill 发现机制、模板 schema、项目记忆根或 alias 支持变化。
- 本记忆失效条件：manifest 不再自动发现 `skills/`，或用户要求兼容旧显式调用。
