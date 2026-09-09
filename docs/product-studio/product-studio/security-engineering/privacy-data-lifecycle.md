# security-engineering 当前产品事实 · 隐私与数据生命周期

## 事实册最小披露边界

- **当前事实**：各 Skill 的项目记忆协议排除秘密、令牌与用户数据；事实册只描述经核验的约束、控制关系及权威核验入口，不以凭据值、真实用户样本或敏感运行内容作为后续任务的记忆材料。
- **权威依据**：`skills/*/SKILL.md#项目记忆`；`skills/security-engineering/references/principles/privacy-data-lifecycle.md`；`skills/security-engineering/references/memory/privacy-data-lifecycle.md`。
- **影响边界**：提示约束不会自动净化源码、配置、环境或代理输出，仍须最小化读取、脱敏表达和差异复核。一般准入与授权政策见 `docs/product-studio/product-studio/product-management/problem-users-policy.md#项目核心记忆政策`；存储和引用机制见 `docs/product-studio/product-studio/software-architecture/decomposition-cohesion.md#项目记忆边界`。
- **复核入口**：对照实际任务和事实册检查敏感字段、副本及引用内容的披露范围；数据类别、保留用途、存储位置或安全边界变化时重审。
