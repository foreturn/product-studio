# software-architecture 当前产品事实 · 驱动因素与演进验证

## 十一项专业的决策反思与局部纠偏

- **当前事实**：各专业执行协议均把已裁定目标与政策、当前事实、因果推断和待证假设分开；具体方案不因提出者、现有实现或测试通过而自动成立。前提被证伪，或修复依赖新增例外、重复规则与状态、绕过职责边界时，重审受影响决定及完整结果，保留仍成立的无关决定。
- **权威依据**：`skills/*/SKILL.md#执行协议`；`skills/software-architecture/references/principles/drivers-evolution.md`。
- **影响边界**：纠偏不改变专业所有权，超出本专业时只说明矛盾、影响和待裁决选项。该方法在技能中的承载位置见 `docs/product-studio/product-studio/software-architecture/decomposition-cohesion.md#方法论与专业编码约束的归属`。
- **复核入口**：以实现偏离决定、决定前提证伪、适用条件变化三类场景核对归因及重审范围；决策方法、失败归因或专业所有权变化时重审。

## 任务拆解与阶段证据

- **当前事实**：复杂工作按真实依赖和本专业可验证结果拆解，每步保持契约、状态或结果不变量；简单任务直接处理。阶段检查与风险相称，确认后才推进依赖该结果的工作，最终仍核对完整结果与证据范围；验证设计和只读证据审查本身也会命中验证准则。
- **权威依据**：`skills/*/SKILL.md#执行协议`；`skills/product-management/references/principles/scope-priority.md`；`skills/quality-engineering/references/principles/evidence-automation.md`；`skills/release-engineering/references/principles/version-scope.md`。
- **影响边界**：不强制计划文档、固定技术顺序或每次编辑全量检查。证据复用取决于对象、依赖和环境是否仍有效；任务含提交时，以可审查、可验证且可恢复的完整变更单元组织。
- **复核入口**：用简单调整、跨模块依赖、兼容迁移和只读审查核对任务粒度与证据效力；完成定义、验证对象或提交边界变化时重审。
