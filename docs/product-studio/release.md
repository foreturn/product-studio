# release 当前项目事实

## 发布与运行职责

- **当前事实**：`release` 对已验收变更通过发布对象与变更范围、版本提交与 Tag 治理、发布说明与追溯、制品与供应链、环境与依赖就绪、兼容与迁移编排、发布策略与执行门禁、可观测与健康判断、回滚事故与反馈闭环九项能力，分别裁定仓库准备、发布就绪、操作授权、实际执行和运行健康；五种状态不互相替代。
- **权威依据**：`skills/release/SKILL.md#输入门禁`；`skills/release/SKILL.md#执行流程`；`skills/release/references/principles.md#核心能力`
- **影响边界**：仓库版本与 Tag、远端 Release、不可变制品、目标环境、迁移与配置、发布批次、健康门禁、恢复处置及后续反馈。
- **复核入口**：以只读版本准备、未授权部署、已授权分批发布和门禁失败恢复四类全新请求试用 `release`，核对五轴结论、能力按需加载、精确授权停止点与逐步证据；静态校验不证明真实仓库或环境动作。

## 生产操作授权边界

- **当前事实**：生产部署、生产迁移、切流、生产配置、回滚与事故环境操作只由 `release` 在明确授权绑定当前制品、目标环境、范围、动作与有效时窗后执行；代码权限、验收通过、方案、旧授权和准备就绪均不能替代当前生产授权。
- **权威依据**：`skills/release/SKILL.md#输入门禁`；`skills/release/SKILL.md#执行流程`；`skills/router/SKILL.md#裁决边界`
- **影响边界**：七技能路由、验收制品交接、项目既有发布工具的使用，以及所有会改变外部环境状态的操作与结论。
- **复核入口**：分别以只读生产就绪审计和明确绑定制品、环境、范围、动作及时窗的发布请求作全新上下文试用；前者必须停在门禁与下一动作，后者也须逐步绑定执行证据，静态清单校验不证明环境行为。

## 仓库与版本治理

- **当前事实**：`release` 先固定仓库根、比较基线、目标提交与工作区状态，再依据项目既有版本权威、版本政策和 Tag 约定准备版本与发布说明；相关未提交内容阻塞 Tag，提交、Tag、推送和远端 Release 必须分别取得精确授权，已发布 Tag 默认不可移动、复用或强制覆盖。
- **权威依据**：`skills/release/SKILL.md#输入门禁`；`skills/release/references/principles.md#发布对象与变更范围`；`skills/release/references/principles.md#版本提交与-tag-治理`
- **影响边界**：版本文件与镜像、发布说明、提交、分支与 Tag、远端 Release、Tag 触发的构建发布流水线，以及由源码到不可变制品的追溯关系。
- **复核入口**：以脏工作区、版本来源冲突、同名 Tag、只授权本地 Tag、授权推送 Tag 及 Tag 触发部署等全新上下文分别试用；必须区分本地提交或 Tag、远端 Tag、制品发布与环境部署证据，静态清单校验不证明仓库或远端动作已执行。

## Codex 与 Claude Code 双端分发

- **当前事实**：仓库以独立的 Codex 与 Claude Code 插件清单分发同一 `product-studio` 技能根，两份 `plugin.json` 共同声明同一发布身份、版本和 `skills` 路径；两套 marketplace 安装与发现链路必须分别验证，任一端通过不能替代另一端证据。
- **权威依据**：`.codex-plugin/plugin.json#version`；`.claude-plugin/plugin.json#version`；`README.md#安装`
- **影响边界**：插件名称、版本、七个 Skill、Codex marketplace、Claude Code marketplace、安装文档与发布验收；修改版本或技能入口时两份插件清单必须保持一致。
- **复核入口**：解析并比较两份 `plugin.json` 的 `name`、`version` 与 `skills`，运行 `claude plugin validate --strict .`，再分别通过两套 marketplace 在隔离环境实际安装并核对新线程中的技能发现；未执行的分发面保持未验证。
