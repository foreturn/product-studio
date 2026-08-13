# release-engineering 当前产品事实

## 发布与运行五轴裁决

- **当前事实**：`release-engineering` 分别裁定仓库准备、发布就绪、当前授权、实际执行和运行健康；它消费已验证的制品、数据库迁移方案与安全门禁，负责版本与 Tag、发布说明、制品供应链、环境就绪、迁移批次、发布策略、观察窗、停止回滚和事故恢复，不在发布现场重写数据库或安全策略。
- **权威依据**：`skills/release-engineering/SKILL.md#输入门禁`；`skills/release-engineering/SKILL.md#执行流程`；`skills/release-engineering/references/principles.md#核心能力`
- **影响边界**：仓库版本、Tag、远端 Release、不可变制品、目标环境、配置、生产迁移、批次、健康门禁和恢复处置分别绑定自身直接证据；五种状态不能相互代替。
- **复核入口**：以只读版本准备、未授权部署、已授权分批发布、数据库迁移和门禁失败恢复场景检查五轴结论、专业输入、精确停止点及逐步证据；静态 Skill 校验不证明任何环境动作已执行。

## 生产操作授权边界

- **当前事实**：提交、Tag、推送、远端 Release、制品晋级、生产部署、生产迁移、切流、生产配置、回滚与事故环境操作，只有在明确授权绑定当前仓库或制品、目标环境、范围、具体动作和有效时窗时方可执行；代码权限、验收通过、准备就绪、方案和旧授权均不能替代当前授权。
- **权威依据**：`skills/release-engineering/SKILL.md#边界`；`skills/release-engineering/references/principles.md#发布策略与执行门禁`
- **影响边界**：任何仓库、远端、制品或环境状态变化及其自动触发副作用均受此边界约束；授权和命令流水不写入事实册供后续复用。
- **复核入口**：分别提出只读生产审计、仅授权本地 Tag、授权推送但不部署和绑定完整发布对象的请求，核对每种动作独立取证、对象漂移后重新授权且健康只能由当前观察证据证明。

## 双端分发身份

- **当前事实**：仓库的 Codex 与 Claude Code 清单共同声明插件名 `product-studio`、版本 `1.0.3` 和技能根 `./skills/`，源树包含十项 Skill；两套 marketplace 安装与发现链路须分别验证，源树或任一平台的结构通过不能证明另一平台已安装当前快照。
- **权威依据**：`.codex-plugin/plugin.json#name`；`.claude-plugin/plugin.json#name`；`README.md#安装`
- **影响边界**：插件身份、版本、十项 Skill、Codex marketplace、Claude marketplace、安装说明和发布验收依赖双清单一致；`CHANGELOG.md#Unreleased` 描述尚未形成正式发布身份的当前源变更。
- **复核入口**：解析并比较两份 `plugin.json` 的 `name`、`version` 与 `skills`，运行两套插件结构校验；实际分发须分别从对应 marketplace 安装并在新线程核对十项技能发现，未执行的分发面保持未验证。
