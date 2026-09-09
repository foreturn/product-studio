# software-architecture 当前产品事实 · 契约与交互

## 语义解释与确定性规则边界

- **当前事实**：Product Studio 的软件架构与后端工程准则要求每项业务判断先区分封闭且可完整枚举的确定性规则，与依赖上下文、组合关系、表达差异或无法穷举知识的语义解释。语义解释必须由产品明确的责任边界承担并以结构化结果跨界传递；确定性执行只负责结构、协议、权限、作用域、资源、证据和副作用约束，不得以业务关键词、句式正则、删词表或少量示例近似语义责任。
- **权威依据**：`skills/software-architecture/references/principles/contracts-interactions.md#语义解释与确定性规则边界`；`skills/backend-engineering/references/principles/contract-validation.md#语义解释与确定性规则边界`；`skills/software-architecture/references/memory/contracts-interactions.md`；`skills/backend-engineering/references/memory/contract-validation.md`。
- **影响边界**：该约束不绑定输入形态、交互方式或具体实现；只要业务含义依赖上下文便适用。协议结构、标识符、格式、封闭词表和正式规则仍可使用正则、枚举或固定映射，但须有完备权威和明确作用域。证据不足或解释冲突时回到既定语义责任边界补证、重释或请求澄清，责任不可用时进入显式保守降级。
- **复核入口**：对照两项专业的契约准则与记忆范围，以等价表达、相邻含义、歧义、证据不足和语义责任不可用场景核验结构化结果与确定性守卫；语义所有权、规则完备性、证据标准、降级政策或专业边界变化时重审。
