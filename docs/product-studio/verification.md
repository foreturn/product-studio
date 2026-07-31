---
schema: 1
memory: verification
scope: current-project
project_root: "current product-studio repository"
status: done
updated_at: "2026-07-31T15:37:46+08:00"
verified_at: "2026-07-31T15:37:46+08:00"
verified_revision: "9efef58ddb3f + source-worktree:f0cd0325d657"
confidence: high
supersedes: [MIG-001]
---

# verification

- 固定责任角色：`verification`（独立验收负责人）
- 项目根：当前 `product-studio` 仓库
- 记忆路径：`docs/product-studio/verification.md`

## 恢复摘要

- 当前验收对象：保留八字段能力恢复、终态增量与轻量首建模板的既有证据，并验收两份根级 reference 删除、七职项目记忆契约自包含、delivery 跨角色总路由及模板只加载同角色能力手册。
- 总体结论：通过；`AC-014` 至 `AC-021` 的既有结论仍有效，`AC-022` 已取得当前正向、负向与冷启动直接证据。
- 首个可执行验证：无；后续仅在 Skill、reference、记忆、manifest、校验器或专业语义变化时重验。
- 阻塞：无源码验收阻塞；真实安装与发布未获授权，且不属于当前源码验收范围。

## 验收对象

- 原始意图来源：用户指令（2026-07-30 至 2026-07-31）。
- 差异或制品：当前工作区中 `skills/`、`templates/`、`docs/product-studio/`、references、README、scripts 与 UI 元数据。
- Git / 制品修订：当前未提交 worktree；本轮核验基线为 `9efef58ddb3f + source-worktree:f0cd0325d657`，旧修订仍只保留在历史 V 行。
- 环境：本地 Windows PowerShell 工作区；未安装或发布插件。
- 适用记忆：七份同名项目记忆。

## 依据账本

| ID | 类型 | 内容 | 精确来源 | 置信度 | 状态 | 取代关系 | 失效条件 |
|---|---|---|---|---|---|---|---|
| F-001 | 用户确认 | AC-001 至 AC-010 均为必需验收范围 | `discovery.md#验收标准` | 高 | active | 无 | 用户缩减范围 |
| F-002 | 仓库事实 | Skill Creator 与项目校验器可提供结构证据，前向场景提供行为证据 | 校验脚本与 fresh subagent | 高 | active | 无 | 工具不可用 |
| F-003 | 用户确认 | “只读取”“不得从”等来源白名单式措辞会造成上下文缺失，其他位置的同类问题也须修正 | 本轮用户指令（2026-07-30） | 高 | active | supersedes 旧来源白名单措辞 | 用户改变来源模型 |
| F-004 | 用户确认 | 七份 Skill 删除职责、核心能力、专业决策顺序，角色 reference 按原核心能力详细扩充并由 Skill 引用 | 用户指令（2026-07-31，早先轮次） | 高 | superseded | 被 F-005 取代 | 用户改变能力分层 |
| F-005 | 用户确认 | 删除宽泛角色职责与重复章节，保留现有核心能力并压缩为四字段能力卡 | 早先用户指令（2026-07-31） | 高 | superseded | supersedes F-004；superseded by F-006 | 用户实读证明压缩正文更宽泛、细节不足 |
| F-006 | 用户反馈 | 上一版能力卡更宽泛且不如 HEAD 改前版本详细；须恢复旧版独有的专业判断、证据、失败模式与反例，同时不恢复空泛“角色职责” | 本轮用户指令（2026-07-31） | 高 | active | supersedes F-005 的四字段压缩型质量结论 | 用户明确接受降低专业细节密度 |
| F-007 | 用户确认 | 项目记忆不得在过程阶段写入；仅在任务终态且适用验证完成后，按受影响角色和事实增量合并，保留仍有效事实与无关章节，不得全量覆盖 | 本轮用户指令（2026-07-31） | 高 | active | supersedes 过程写入与整卷重写的记忆方式 | 用户改变项目记忆生命周期 |
| F-008 | 用户确认 | 项目记忆应保存已成立的详细事实，使 AI 可直接理解项目；首建模板只提供事实家族索引与一张通用骨架，不预铺各家族空卡。恢复摘要、任务快照、动作队列、未来计划与未证实假设不作为项目事实 | 本轮用户确认（2026-07-31） | 高 | active | 补充 F-007 的内容、质量要求与模板边界 | 用户改变项目记忆用途或允许过程内容入册 |
| F-009 | 用户确认 | 根级 `references/project-memory.md` 与 `references/platform-compatibility.md` 没有独有运行消费者且与现行契约重复，应删除；每个角色的事实准入、稳定 ID、终态增量与 schema 规则由同名 Skill 的“项目记忆”自包含定义，跨角色总路由只由 delivery Skill 定义，首建模板只加载同角色能力手册 | 本轮用户确认（2026-07-31） | 高 | active | supersedes 根级共享记忆契约作为运行权威 | 用户重新引入根级共享契约或改变角色所有权 |
| D-001 | 验收决定 | reference 统一使用能力目录、四字段核心能力卡、能力组合与完成判据；Skill 按目录加载适用能力卡 | 历史 Skill/reference 修订 | 高 | superseded | supersedes 旧五章节结构；superseded by D-004 | 用户实读证明四字段压缩丢失专业语义 |
| D-002 | 验收边界 | 逐项结论仅为失败、阻塞、通过；总体按“失败 > 阻塞 > 通过”收口。未执行不是结论：外部前置条件不可满足判阻塞，本可执行却漏验或跳过必需验证判失败 | `skills/verification/` 当前差异 | 高 | active | supersedes 未执行语义缺口 | 验收状态规则变化 |
| D-003 | 验收边界 | 风险清单只决定验证优先级与不确定性，不得把候选风险、惯例或改进建议暗造为新需求 | `verification-principles.md#风险建模` | 高 | active | 无 | 权威验收要求变化 |
| D-004 | 验收决定 | 保留四章与按需加载，以 HEAD 改前版本为最低语义基线；52 张卡各依次且仅一次包含启用、输入、执行、裁决、产出、验证、完成、边界，目录仅导航且不得替代正文，不恢复空泛“角色职责” | 当前 Skill/reference 差异与用户反馈 | 高 | active | supersedes D-001 的四字段压缩正文，保留四章与单向引用 | 语义审计或真实使用发现改前独有判断仍缺失 |
| D-005 | 验收决定 | schema 2 只允许事实有效性状态 `current`、`conditional`、`stale`、`superseded`；schema 1 文件头只接受终态 `done`、`failed`、`blocked`、`not_applicable`。校验器不得因正文中合法的业务/API 状态名含 `pending`、`in_progress` 或 `draft` 而误判；schema 1 结论只从唯一当前 `## 最终结论` 块解析，schema 2 验收记忆必须恰有一张状态为 `current` 且明确写出通过、失败、阻塞或不适用的 `VER-CONCLUSION-*` 卡 | verification Skill／模板、项目校验器与本轮用户确认 | 高 | active | supersedes 全文子串拒绝与全文推断结论 | 结论解析、业务状态或记忆状态契约变化 |
| D-006 | 验收决定 | 每份 schema 2 首建模板必须按角色列出完整且有说明的 ID 家族，并且只含一张带可读标题占位的十三字段通用骨架；不得为各家族预铺空卡，实际记忆才按有证据事实复制骨架。模板仅用于首次创建，且只加载同角色能力手册；既有 schema 1/2 只依据对应 Skill“项目记忆”中的本角色事实卡规则、角色 ID 家族与自身事实卡增量维护，不得被模板变化强制迁移或重建 | 七份 Skill／模板、delivery 跨角色总路由与项目校验器 | 高 | active | supersedes AC-004 的恢复／动作型模板门禁及逐家族空卡，补充 D-005 的版本边界 | 事实字段、ID 家族、模板用途或兼容策略变化 |

## 要求与证据矩阵

| AC-ID | Requirement source | Implementation | Current evidence | Result | Evidence expires when |
|---|---|---|---|---|---|
| AC-001 | `discovery.md` | 七个 `skills/<name>/` | 精确集合、单词正则与七次 `quick_validate.py` 均通过 | passed | 任一 Skill 改名 |
| AC-002 | `discovery.md` | 七份同名模板与项目记忆 | Skill / template / memory 三处集合恒等断言通过 | passed | 任一文件改名 |
| AC-003 | `discovery.md` | 七份 `agents/openai.yaml` | 官方生成器产物经逐职 YAML、身份与 `$<skill>` 断言通过 | passed | 默认提示词变化 |
| AC-004 | `discovery.md` | 七份 AI 记忆模板 | schema 2、五字段文件头、恰好两个二级章节、完整角色家族索引、单张通用骨架、13 项事实语义与禁止过程章节均通过 | passed | 模板、字段或 ID 家族变化 |
| AC-005 | `discovery.md` | 全仓引用 | 活跃路径旧名检索零命中，校验器旧名门禁通过 | passed | 新增旧引用 |
| AC-006 | `discovery.md` | 完整差异与七职记忆 | 项目 / 插件校验、`py_compile`、diff 检查、两次前向试用与独立一致性审校通过 | passed | 任一相关差异变化 |
| AC-007 | `discovery.md` | 七职 Skill 与模板的来源分层 | 当前项目事实、带来源外部参考、适用性与采纳状态语义门禁通过 | passed | 任一来源契约变化 |
| AC-008 | `discovery.md` | 活跃提示词与来源退化防护 | 旧硬辞零残留；注入旧硬辞、删除来源字段的内存变体均被拒绝 | passed | 新增绝对来源限制或校验器变化 |
| AC-009 | `discovery.md` | 七份 Skill 的专业能力来源 | superseded：旧直达引用与章节规则仅证明 `worktree:186d7c03e713` | superseded | 已命中：Skill 结构与引用变化 |
| AC-010 | `discovery.md` | 七份详细角色能力手册 | superseded：旧五章节、角色能力词与百行门禁已被本轮能力卡结构取代 | superseded | 已命中：reference 与校验器变化 |
| AC-011 | 早先用户指令 | 七份 reference 的四字段能力驱动结构 | 历史四章、52 张四字段卡与旧标题零命中证据 | superseded | 已命中：用户实读判定更宽泛、不如改前详细 |
| AC-012 | 早先用户指令 | 四字段能力卡的执行边界 | 历史字段与角色边界审校 | superseded | 已命中：能力卡字段及正文语义变化 |
| AC-013 | 早先用户指令 | 四字段 verification 的验收状态行为 | 历史 fresh 验收场景 | superseded | 已命中：verification reference 语义变化 |
| AC-014 | 本轮用户反馈 | 七份 reference 的八字段结构与导航边界 | 四个统一章节、52 个原能力 H3、416 个字段、目录仅导航、旧空泛角色职责零恢复；七 refs 共 2255 行，HEAD 旧版 1015 行，行数仅作完整性旁证 | passed | 任一 reference、Skill 或校验器变化 |
| AC-015 | 本轮用户反馈 | 改前专业语义完整恢复 | 三组独立语义审计逐职对照 HEAD 独有判断、证据、失败模式与反例；发现的架构证据、后端顺序／调用图、交付外部材料溯源、前端禁用原因缺口均修复并复核 | passed | 任一能力卡正文或语义基线变化 |
| AC-016 | 本轮用户反馈 | 八字段 reference 在新会话中产生具体专业裁决 | fresh discovery、architecture、backend、verification 四组前向测试均使用当前 reference，分别产出可追溯产品契约、架构证据分类、支付回调一致性设计和严格验收失败判定 | passed | 任一相关 Skill/reference、场景或模型加载行为变化 |
| AC-017 | 本轮用户确认 | 七职 Skill 与记忆模板的落盘时机 | 过程阶段不得创建或更新项目记忆；只有任务终态且适用验证完成后才进入记忆合并 | passed | 任一 Skill、模板或记忆生命周期规则变化 |
| AC-018 | 本轮用户确认 | 终态记忆的角色级与事实级增量合并 | 仅修改受影响条目，保留仍有效事实、无关章节及未受影响角色，禁止全量覆盖 | passed | 任一 Skill、模板或合并规则变化 |
| AC-019 | 本轮用户确认 | 终态状态与最终结论解析门禁 | schema 2 只接受事实有效性状态，schema 1 只接受终态文件头；合法业务/API 状态值不因名称被拒绝。schema 1 从唯一当前结论块解析，schema 2 验收记忆要求唯一 `current` 的 `VER-CONCLUSION-*` 卡及明确终态结果 | passed | 记忆状态、业务状态或结论解析规则变化 |
| AC-020 | 本轮用户确认 | 两组 fresh 记忆行为场景 | 成功场景保留 F-001、只更新 F-002、增加 F-003；中断场景在终态前停止且 `docs/product-studio/` 零文件变化 | passed | Skill、模板、校验器或 fresh 场景变化 |
| AC-021 | 最新用户确认 | 轻量首建模板、实际详细事实卡与既有记忆兼容 | 七份 schema 2 首建模板各保留完整角色家族索引与一张通用骨架，共七张骨架、91 个必需字段；专业能力细节仅在角色 references，实际记忆仍按证据生成十三字段详细事实卡。缺家族、重复家族、多骨架、缺字段、额外章节与模板复用均被拒绝；实例中的伪家族、第十四字段、残留家族索引、非 RFC 3339 时间及不确定终态也被拒绝，合法泛型定位不误判；fresh discovery 首建只生成两个有证据事实卡，未铺其余家族空卡；既有 schema 1/2 不读取模板且不迁移 | passed | 共享契约、模板、Skill、校验器或兼容策略变化 |
| AC-022 | 最新用户确认 | 根级 reference 删除、七职项目记忆自包含、delivery 总路由与模板单角色加载 | 正向校验确认根级 `references/` 不存在、活跃运行文件无根级 reference 链接、七份 Skill 的“项目记忆”各自完整声明事实准入、稳定 ID、终态增量、原样边界与 schema 1/2 规则，delivery 另行声明受影响角色顺序、禁止代写、写入失败隔离及悬空引用防护，七份模板各只加载同角色能力手册。根 reference 回添或链接、模板跨角色／多链接、角色记忆必需语义缺失及 delivery 路由退化的内存负向变体均被拒绝；fresh backend 仅读 backend Skill 与能力手册即可完整裁定终态增量、稳定 ID、schema 1/2 与首建模板规则，但因只读且缺少项目事实不落盘；fresh delivery 仅读 delivery Skill 与能力手册即可给出总路由、禁止代写、写入失败后的依赖暂缓及无悬空引用规则 | passed | 任一根级 reference、Skill 项目记忆、delivery 路由、模板能力链接或校验器变化 |

## 失败分类

| ID | 分类 | 现象 | 责任角色 | 复现证据 | 状态 |
|---|---|---|---|---|---|
| E-001 | 已解除 | 初始阶段缺少新命名最终证据 | `verification` | AC-001 至 AC-006 当前证据齐备 | resolved |
| E-002 | 证据失效 | 旧能力分层证据对应已变化的 Skill/reference 与校验器 | `verification` | V-009 已由当前 V-011 取代 | resolved |
| E-003 | 专业语义退化 | 四字段卡虽通过结构门禁，但用户实读判定比改前更宽泛、细节不足 | 七职责任角色 | 用户反馈、HEAD 语义映射与三组独立审计 | resolved：由八字段正文与 V-012 取代 |

## 动作队列

| 优先级 | 动作 | 前置条件 | 责任角色 | 完成判据 |
|---|---|---|---|---|
| P2 | 任一能力卡、加载语义、事实卡、模板版本边界、记忆生命周期或验收状态规则变化后重验 | 相关 Skill/reference、模板或校验器变化 | `verification` | AC-014 至 AC-022 在新修订重新获得直接证据 |
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
| V-009 | 能力分层正向与负向 | 项目校验、七次 Skill Creator、插件校验、结构检索与四类内存变体 | 本地 Linux，`347c769c5e9b + worktree:186d7c03e713` | superseded：该证据支持旧章节结构，当前 Skill/reference 与校验器变化已使其失效 | 2026-07-31T00:22:11+08:00 | 已命中：Skill、reference 与校验器变化 |
| V-010 | reference 前向行为 | fresh `$backend` 支付捕获幂等、并发与未知态只读场景 | 旧 Skill、reference 与项目记忆 | superseded：保留为历史行为证据，不外推到当前能力卡结构 | 2026-07-31T00:12:40+08:00 | 已命中：backend 能力来源变化 |
| V-011 | 四字段能力卡结构与行为 | `py_compile`、项目校验、七次 Skill Creator、Claude strict、结构检索、内存负向变体、独立审校、四类 fresh 场景与 `git diff --check` | `9efef58ddb3f + worktree:78def6775d85`，Windows PowerShell | superseded：历史结构门禁曾通过，但用户实读判定正文更宽泛且不如改前详细，不能继续作为当前专业质量证据 | 2026-07-31T10:09:16+08:00 | 已命中并由 V-012 取代 |
| V-012 | 八字段语义恢复与最终验收 | `py_compile`、项目校验、七次 Skill Creator、Claude strict、52 卡／416 字段门禁、七类负向变体、三组独立语义审计、四组 fresh 前向测试与 `git diff --check` | `9efef58ddb3f + worktree:babe95b0ce48`，Windows PowerShell | 通过：七 refs 共 2255 行（HEAD 旧版 1015 行，仅作完整性旁证）；结构、改前语义、负向防退化与新会话专业裁决均取得当前直接证据 | 2026-07-31T10:49:30+08:00 | 任一 Skill、reference、记忆、manifest、校验器或专业语义变化 |
| V-013 | 终态记忆增量、轻量首建模板边界与结论解析回归 | `py_compile`、项目校验、七次 Skill Creator、Claude strict、七模板／七骨架／91 字段、六类模板退化与五类实例反例、fresh discovery 首建、schema 1/2 兼容、增量哨兵与 `git diff --check` | `9efef58ddb3f + source-worktree:bfa1d4812af3`，Windows PowerShell | 通过：模板仅用于 schema 2 首次创建，每份只含家族索引和一张骨架；fresh discovery 场景依据两项产品事实只生成 `DISC-USER-001` 与 `DISC-RULE-001`，未保留模板说明、家族索引、占位或其余空卡。缺家族、重复家族、多骨架、缺字段、额外章节、模板复用、实例伪家族、第十四字段、残留家族索引、日期型时间戳及不确定结论均被拒绝；`Promise<Result<T>>` 合法定位通过。既有 schema 1/2 不读取模板；终态仍按角色及稳定 ID 增量合并，中断与无事实增量场景零写入 | 2026-07-31T14:33:37+08:00 | 任一 Skill、模板、记忆、manifest、校验器或终态场景变化 |
| V-014 | 根级 reference 去重与自包含记忆契约回归 | `py_compile`、项目校验、七次 Skill Creator、Claude strict、根 reference 与活跃链接零残留、模板单角色链接、记忆／路由内存负向变体、fresh backend／delivery 冷启动及 `git diff --check` | `9efef58ddb3f + source-worktree:f0cd0325d657`，Windows PowerShell | 通过：两份根级 reference 已删除，七职记忆规则均由同名 Skill 自包含，delivery 独立承担跨角色总路由，七份模板各只加载同角色能力手册；根 reference 回添或链接、模板跨角色／多链接、角色记忆必需语义缺失与 delivery 路由退化均被拒绝。fresh backend 在只读且缺项目事实时正确不落盘；fresh delivery 正确禁止代写，并在写入失败时暂缓依赖新 ID 的增量而不制造悬空引用。未执行安装或发布 | 2026-07-31T15:37:46+08:00 | 任一根级 reference、Skill、模板、记忆、manifest、校验器或冷启动场景变化 |

## 四组前向测试

| 场景 | 当前专业裁决 | 结果 |
|---|---|---|
| fresh discovery：企业后台批量删除客户按钮 | 给出风险与假设、核心旅程和状态表、MVP／非目标、10 条 AC、指标及四组高影响待决项，明确覆盖租户隔离、逐项部分失败、重复提交幂等和误删恢复 | passed |
| fresh architecture：服务拆分 | 将独立演进、故障隔离、数据主权等边界收益证据与峰值、增长、瓶颈等负载证据分开，未以模式偏好或未来高并发冒充当前依据 | passed |
| fresh backend：支付回调重复／乱序与客户端重试 | 区分支付事实和订单派生状态，给出不变量、状态表、唯一约束、回调事务、请求指纹幂等、单调迁移、补偿对账、Outbox、安全与指标 | passed |
| fresh verification：批量删除完成声明 | 拒绝将类型检查、HTTP 200 截图和单段单测外推为完成，按租户隔离、逐项反馈、幂等与恢复建立 AC，并将可执行漏验判为失败而非阻塞 | passed |

## 两组记忆增量前向测试

| 场景 | 当前专业裁决 | 结果 |
|---|---|---|
| fresh 成功终态：基线含 F-001、F-002 | 完成适用验证后增量合并；保留 F-001，只更新受影响的 F-002，新增 F-003，其他事实与无关章节逐字保持 | passed |
| fresh 终态前中断 | 在进入终态前停止；不创建或更新项目记忆，`docs/product-studio/` 保持零文件变化，原记忆不变 | passed |

## 最终结论

- 结论：通过；AC-014 至 AC-022 及本轮受影响的源码门禁均有当前直接证据。
- 结论依据：既有 52 卡／416 字段、HEAD 改前语义映射、三组独立语义审计及四组专业前向测试仍有效；根级两份 reference 已删除，七职项目记忆契约自包含、delivery 总路由、模板单角色能力链接、正负向门禁及 fresh backend／delivery 冷启动共同成立；schema 1/2 兼容、终态角色增量、合法业务状态保留及唯一当前结论继续成立。
- 未执行项：真实插件安装后的触发率与实际发布；二者不属于本轮源码验收要求，也未获安装或外部变更授权。
- 剩余风险：后续能力内容或平台加载机制变化可能使当前证据失效，届时须按失效条件重新验收，不得据风险清单新增产品要求。

## 交接与失效

- 应退回角色：无；七职提示词、首次建档模板与既有记忆增量已按当前修订收口。
- 必须携带的证据 ID：AC-001 至 AC-010、ADR-002 至 ADR-006。
- 尚未解决：无源码验收缺口；真实安装后的触发率只在后续获得安装授权时重新适用。
- 重新核验触发器：任何相关源码、模板、记忆、manifest 或校验器变化。
- 本记忆失效条件：验收对象修订或环境变化。
