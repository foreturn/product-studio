# security-engineering 当前产品事实 · 隐私与数据生命周期

## 事实册最小披露边界

- **当前事实**：十一项 Skill 在自身“项目记忆”章限定事实册只保存项目核心认知，排除秘密、令牌、用户数据、任务过程和一次性结果；对应 `references/memory/` 簇卷界定本专业关注的认知范围，各 Skill 还要求只保留当前仍成立的事实，当前权威与旧记忆冲突时以前者为准，记忆维护不得扩大原任务写权限。
- **权威依据**：`skills/security-engineering/references/memory/`；`skills/release-engineering/references/memory/`；`skills/*/SKILL.md#项目记忆`
- **影响边界**：该边界约束所有当前产品根目录中的 Product Studio 事实册，不以产品是否初始化 Git 为前提；Skill 指令不自动净化权威源码、配置、环境系统或代理输出中的敏感内容，仍依赖最小化读取、脱敏表达与最终差异复核。
- **复核入口**：枚举十一份 SKILL 的“项目记忆”章与 `references/memory/` 各簇卷，对照实际任务与已生成事实册检查最小披露、内容准入和授权边界；新增 Owner、记忆簇卷、存储位置或安全边界时重审。
