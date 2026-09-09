# product-management 当前产品事实 · 问题、角色与政策裁决

## 产品意图与体验的一体化裁决

- **当前事实**：产品管理共同裁定产品问题、用户与商业结果、业务资格、预期结果政策及体验语义；资格与结果政策先于界面表达。高影响政策缺失时保留未裁决状态，说明选项、后果和所需权威。可信主体、对象级授权强制、默认拒绝与租户隔离由安全工程依据产品政策独立裁定。
- **权威依据**：`README.md#十一项通用底座`；`skills/product-management/SKILL.md#执行协议`；`skills/product-management/references/principles/problem-users-policy.md`；`skills/security-engineering/references/principles/identity-access.md`。
- **影响边界**：纯内部实现且已证实产品与体验语义均未改变时，不触发新的产品裁决。内容与客户端分工见 `docs/product-studio/product-studio/product-management/content-interaction.md`；范围与整体成本取舍见 `docs/product-studio/product-studio/product-management/scope-priority.md`。
- **复核入口**：以政策缺失、资格与授权强制冲突、政策已定但可见结果不清及纯内部重构核对裁决边界；产品、体验或安全所有权改变时重审。

## 项目核心记忆政策

- **当前事实**：项目记忆帮助后续任务理解持续影响判断的项目核心认知，只接纳实际核验、属于本专业且难从局部代码直接看清的事实；新确认的既有事实同样适用，不以 Git 差异为限。事实册保留当前认知，当前权威优先。只读任务不写，除非用户明确要求维护记忆；可写任务的同根事实册维护随证据闭环进行，并在结束前收口，用户排除的路径与资源仍受保护。
- **权威依据**：`README.md#项目记忆`；`skills/product-management/SKILL.md#项目记忆`；其余专业 SKILL 的同名章节。
- **影响边界**：该政策适用于命中专业的事实维护，不把记忆变成事实权威，也不扩张任务写权限。定位、按簇存储与引用机制见 `docs/product-studio/product-studio/software-architecture/decomposition-cohesion.md#项目记忆边界`；敏感内容排除见 `docs/product-studio/product-studio/security-engineering/privacy-data-lifecycle.md`。
- **复核入口**：用只读审查、可写修改、核验既有事实和旧认知失效场景检查准入、授权与维护时点；记忆目的、准入或写权限政策变化时重审。
