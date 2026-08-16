# security-engineering 当前产品事实

## 事实册最小披露边界

- **当前事实**：十一位 Owner 的 memory 只列未来 AI 作出正确专业判断所需的项目核心认知，并统一禁止秘密、令牌、用户数据、任务过程和一次性结果；各 Skill 还要求只保留当前仍成立的事实，当前权威与旧记忆冲突时以前者为准，记忆维护不得扩大原任务写权限。
- **权威依据**：`skills/security-engineering/references/memory.md`；`skills/release-engineering/references/memory.md`；`scripts/validate-project.mjs#validateSkill`
- **影响边界**：该边界约束所有目标仓库的 Product Studio 事实册；Skill 指令不自动净化权威源码、配置、环境系统或代理输出中的敏感内容，仍依赖最小化读取、脱敏表达与最终差异复核。
- **复核入口**：枚举十一份 memory 的“使用方式”和核心主题，执行项目校验、秘密模式扫描，并以前向任务检查事实册不含禁入内容；新增 Owner、记忆主题、存储位置或安全边界时重审。
