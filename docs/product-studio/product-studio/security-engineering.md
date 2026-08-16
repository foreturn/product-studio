# security-engineering 当前产品事实

## 事实册最小披露边界

- **当前事实**：十一位 Owner 的 memory 契约只允许同时满足当前终态、稳定、非显然、影响后续判断、重查成本高、唯一 Owner、可复核与安全留存的专业语义，并统一禁止秘密、令牌、用户数据、生产授权、原始载荷、任务历史和原始 diff；源码或配置摘要、迁移进度、单次版本、摘要、指标、时点、部署快照和可生成清单不得冒充当前事实。
- **权威依据**：`skills/security-engineering/references/memory.md`；`skills/release-engineering/references/memory.md`；`scripts/validate-project.mjs#validateSkill`
- **影响边界**：该边界约束所有目标仓库的 Product Studio 事实册和最终答复中的终态事实报告；提示契约不自动净化权威源码、配置、环境系统或代理输出中的敏感内容，仍依赖最小化读取、脱敏表达与最终差异复核。
- **复核入口**：枚举十一份 memory 的通用入册门禁、全册安全规则与事实写法，执行项目校验、秘密模式扫描，并以前向任务检查事实册与最终报告不含禁入内容；新增 Owner、事实字段、入册门禁或终态报告语义时重审。
