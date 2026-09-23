# release-engineering 当前产品事实 · 版本范围与对象身份

## 多端插件发布身份契约

- **当前事实**：Codex、Claude Code、Antigravity 与 OpenCode 各端清单共同声明名称 `product-studio`、各自的版本字段和技能根 `./skills/`（或 `./skills`），名称与版本必须相等；清单不声明额外运行组件，发布源中每项 Skill 都携带自身的执行与项目记忆协议。
- **权威依据**：`plugin.json`；`opencode.json`；`.codex-plugin/plugin.json`；`.claude-plugin/plugin.json`；`skills/*/SKILL.md`。
- **影响边界**：具体当前版本由清单即时读取，不复制进事实册。专业集合见 `docs/product-studio/product-studio/product-management/scope-priority.md#十一项通用专业底座`；安装与缓存链路的证据边界见 `docs/product-studio/product-studio/release-engineering/distribution-communication.md`。
- **复核入口**：运行 `python scripts/check.py` 比较各清单的名称、版本和技能根，检查打包的技能入口与引用资源；实际发布再分别验证渠道安装与新上下文发现。发布身份、资源布局或客户端加载方式变化时重审。

## 无兼容别名的结构边界

- **当前事实**：当前插件不提供客户端 Hook、公共记忆协议、旧技能入口、旧事实文件名或命令级别名，不维护双写事实或隐藏重定向；依赖旧名称或单册事实路径的使用方须显式调整。
- **权威依据**：`README.md#项目记忆`；`skills/`；`.codex-plugin/plugin.json`；`.claude-plugin/plugin.json`。
- **影响边界**：当前事实目录与协议布局见 `docs/product-studio/product-studio/software-architecture/decomposition-cohesion.md#项目记忆边界`。源码检查不证明外部仓库已迁移，未读取的外部事实册也不自动改写。
- **复核入口**：检查技能目录、清单、资源引用和当前事实根；事实簇改名或拆分时核对原有事实归属及引用，兼容承诺或迁移机制变化时重审。
