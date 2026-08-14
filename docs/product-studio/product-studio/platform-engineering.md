# platform-engineering 当前产品事实

## Hook 注册与插件数据隔离

- **当前事实**：插件在默认 `hooks/hooks.json` 以 `${CLAUDE_PLUGIN_ROOT}` 注册 `UserPromptSubmit`、`PreToolUse`、`PostToolUse` 与 `Stop` 四类命令 Hook，均执行同一无第三方依赖的 Node 脚本并使用 180 秒处理时限；状态、仓库 journal 与回执位于客户端插件数据目录，Hook 注入的普通 Shell 命令必须显式携带 `--data-dir` 与 `--session`，不依赖环境变量偶然继承。
- **权威依据**：`hooks/hooks.json`；`scripts/terminal-hook.mjs#dataRoot`；`scripts/terminal-hook.mjs#journalPath`；`README.md#终态-Hook`
- **影响边界**：Codex 与 Claude Code 的插件运行时可发现默认 Hook 路径，Codex 提供兼容的 Claude 根变量；客户端是否实际启用、信任和执行 Hook 仍需分别在安装态验证，源树静态结构不能外推。
- **复核入口**：逐事件解析 `hooks/hooks.json`，在 Hook 有插件环境而普通 CLI 无插件环境的临时仓库中运行会话与 Pre/Post 配对测试，并在两类客户端安装后检查信任与事件执行；Hook API、根变量、超时、matcher 或插件数据契约变化时重审。

## 非 Git 工作区降级

- **当前事实**：当会话目录不属于 Git 仓库时，`UserPromptSubmit` 返回明确停用说明，工具事件无活动状态即空操作，`Stop` 报告没有匹配基线而不阻断普通非仓库任务；`status`、`begin` 和 `record` 命令仍要求可选择的有效 Git 会话状态。
- **权威依据**：`scripts/terminal-hook.mjs#handlePrompt`；`scripts/terminal-hook.mjs#handleToolEvent`；`scripts/terminal-hook.mjs#handleStop`；`tests/terminal-hook.test.mjs`
- **影响边界**：降级只避免插件破坏非 Git 工作流，不提供这些目录的变更或事实处置保证；任何完成声明仍只能使用实际取得的证据。
- **复核入口**：运行非 Git 目录四类 Hook 行为测试，并分别检查事件模式与三个显式命令的退出语义；仓库发现、活动状态或客户端工作目录规则变化时重审。
