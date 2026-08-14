# backend-engineering 当前产品事实

## 仓库与事实册内容指纹

- **当前事实**：终态 Hook 同时计算完整仓库指纹与实现指纹：两者均组合已存在或尚未出生的 `HEAD` 身份、porcelain 状态、相对 `HEAD` 的 raw diff、索引条目与索引标志，并以 1 MiB 缓冲流式哈希所有脏、未跟踪、`assume-unchanged` 或 `skip-worktree` 路径的实际内容，嵌套 Git 工作树递归计算同类指纹；实现指纹只排除合法 `docs/product-studio/<product-id>/<owner>.md` 路径。事实册另逐册计算 SHA-256。
- **权威依据**：`scripts/terminal-hook.mjs#repositorySnapshot`；`scripts/terminal-hook.mjs#hashWorkingPath`；`scripts/terminal-hook.mjs#specialIndexPaths`；`scripts/terminal-hook.mjs#factBookFingerprints`
- **影响边界**：完整指纹用于解释工具前后变化、绑定回执并核对事实册动作，实现指纹用于判定验证是否因代码或其他非事实变更而陈旧，逐册指纹用于核对实际变化是否与声明的产品及 Owner 一致；Git 忽略文件、仓库外部状态和未被查询的外部系统不在证明范围内，单次指纹超过安全时限会失败而非降级为弱摘要。
- **复核入口**：运行无首提交仓库、暂存与工作树变化、未跟踪路径、`assume-unchanged`、`skip-worktree`、同尺寸大文件、逐册变化和已脏子模块继续改动场景；Git 摘要来源、索引语义、事实路径、缓冲或超时策略变化时重审。

## 有界终态状态机

- **当前事实**：每个会话保存当前 Git 根、turn key、仓库与逐册事实基线、账本序号、续写状态及最小回执结果；同一仓库另以带锁原子写的有界 journal 配对 `session + turn + toolUseId` 的 Pre/Post 指纹边。每个会话与 turn 使用独立回执路径，新 `turn_id` 不继承旧续写；首次缺回执的 `Stop` 最多阻断一次，随后只报告协议失败。回执无论记录成功或拒绝均立即删除，孤儿回执保留不超过一日、状态不超过七日、账本最多 1024 边。
- **权威依据**：`scripts/terminal-hook.mjs#withJournal`；`scripts/terminal-hook.mjs#recordToolPre`；`scripts/terminal-hook.mjs#recordToolPost`；`scripts/terminal-hook.mjs#pruneStorage`；`scripts/terminal-hook.mjs#handleStop`
- **影响边界**：事件链只把非并发且可连续解释的当前会话边归给本回合；其他会话的顺序边只解释共享工作树漂移，同册交叠、账本缺口、活动工具或无 Pre 的 Post 均不能静默放行。协议失败仍不构成同步成功或交付完成证据。
- **复核入口**：运行新 turn、独立回执、续写基线、顺序异会话、同册并发、跨进程锁、活动工具、账本裁剪缺口、回执删除、过期清理、`stop_hook_active` 和重复停止场景；会话键、turn、锁、保留或重试政策变化时重审。

## 证据回执一致性校验

- **当前事实**：终态回执必须绑定 Git 根、会话、turn、最终完整仓库指纹，并以 `toolUseId + inputDigest + commandHash + expectedExitCodes` 引用 Hook 实际观察且发生在最后实现变更之后的 `Bash`、`exec_command` 或 `shell_command` 验证候选；验证后的合法 Owner 事实册变更不使该候选失效，协议控制命令与编辑工具都不能成为验证证据。唯一活动工具是当前会话和 turn 的非并发 `record` 外层调用时允许闭合回执；其他活动或多个 `record` 均拒绝。`NO_CHANGE` 要求至少一项显式无变化 Owner 动作且本回合归属事实册未变，`SYNCED` 要求每本归属当前会话的事实册变化与增改删声明精确对应。`DEFERRED` 与 `BLOCKED` 必须写明原因且不得保留本回合事实变更；`DEFERRED` 仍需观测验证，`BLOCKED` 可因尚未形成可验证终态而不提供。
- **权威依据**：`scripts/terminal-hook.mjs#validateEnvelope`；`tests/fixtures/terminal-envelope.json`；`references/terminal-protocol.md#回执格式`
- **影响边界**：一致性校验证明回执结构、观测工具身份、退出语义、仓库事件链和逐册动作关系自洽；它不能判断命令是否足以验证业务、专业事实正文是否正确，也不能证明未列出的产品、Owner、浏览器、设备、服务或生产范围新鲜。
- **复核入口**：运行三类 Shell 验证候选、编辑工具非证据、自报与伪造证据、Pre/Post 不匹配、无 Pre、超时取消、验证后漂移、预期与非预期退出码、`NO_CHANGE`、`SYNCED`、冒名 Owner、未知归属 `DEFERRED` 及逐册变化测试；回执 Schema、事件字段、工具名、事实动作或终态结果变化时重审。
