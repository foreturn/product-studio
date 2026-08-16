# release-engineering 当前产品事实

## 双端插件发布身份契约

- **当前事实**：Codex 与 Claude Code 两份插件清单共同声明名称 `product-studio`、各自的版本字段和技能根 `./skills/`，名称与版本必须相等，源树固定暴露十一项 Skill；每项 Skill 自身携带 Owner 专属的项目记忆指令，清单不声明额外运行组件。
- **权威依据**：`.codex-plugin/plugin.json`；`.claude-plugin/plugin.json`；`skills/*/SKILL.md#项目记忆`；`scripts/validate-project.mjs`
- **影响边界**：名称、版本字段、技能集合和项目记忆提示共同构成源树发布身份契约；具体当前版本由清单即时读取，不复制进事实册。两类 marketplace 的安装、缓存和发现链路彼此独立，任一清单通过不能证明另一客户端已安装或遵循项目记忆指令。
- **复核入口**：解析比较两份 `plugin.json` 的名称、版本和技能根，运行项目与 Claude 严格校验；实际发布时分别从对应 marketplace 安装并在新上下文核对十一项技能的发现、专业选择和项目记忆读取维护行为。

## 无兼容别名的结构边界

- **当前事实**：当前结构采用十一项 Owner 同名事实 locator 和各 Skill 内置的项目记忆提示，不提供客户端 Hook、公共记忆协议、旧技能入口、旧事实文件名或命令级别名；不得同时维护双写事实或隐藏重定向。
- **权威依据**：`README.md#当前项目事实`；`README.md#项目记忆`；`scripts/validate-project.mjs#REMOVED_SKILLS`；`scripts/validate-project.mjs#REMOVED_FACT_BOOKS`；`scripts/validate-project.mjs#REMOVED_RUNTIME_ASSETS`
- **影响边界**：依赖先前技能名或事实 locator 的使用方需要显式采用当前主版本结构；源树校验只证明旧入口不存在，不证明外部仓库已经完成任何调整。
- **复核入口**：运行项目校验并扫描技能目录、README、双端清单和当前事实根；未来决定提供别名、迁移工具或双写策略时必须重新裁定并重审。

## 双渠道分发证据边界

- **当前事实**：Codex 通过 `.agents/plugins/marketplace.json` 描述远端可安装源，Claude Code 通过 `.claude-plugin/marketplace.json` 描述仓库内插件源；README 分别给出安装命令，源树静态通过不等于任一远端渠道已发布或缓存已刷新。
- **权威依据**：`.agents/plugins/marketplace.json`；`.claude-plugin/marketplace.json`；`README.md#安装`
- **影响边界**：双端清单、marketplace、安装发现、Skill 选择和新上下文项目记忆行为必须分别取证；源树修改与静态校验本身既不会触发外部发布或安装，也不能证明远端渠道已更新。
- **复核入口**：先运行两类清单校验，再在明确授权后分别执行渠道安装与新线程发现、项目记忆读取维护及后续复用检查；marketplace 地址、来源格式、版本或客户端 Skill 发现机制变化时重审。
