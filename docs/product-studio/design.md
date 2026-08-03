# design 当前代码事实

## 最短产品使用路径

- **当前事实**：边界清楚的单一任务直达对应专业 Skill；只有目标用户、业务闭环、产品规则、交互体验、范围或验收仍不明确时才加入 `design`，系统架构由 `architecture` 承接，具体服务端实现由 `backend` 承接。
- **代码定位**：`skills/router/SKILL.md#直达与触发`；`skills/router/SKILL.md#最小调用链`；`README.md#路由`
- **影响范围**：使用插件的编码者、`router` 选链、`architecture`、`backend` 与 `frontend` 输入门禁；错误路由会增加无消费者设计或让下游猜测产品语义。
- **验证入口**：`python3 -X utf8 scripts/validate_project.py --self-test` 检查产品设计、系统架构与服务端实现归属、常规终端验证不触发 router 及契约里程碑；真实选链仍需全新上下文试用。

## 产品设计职责

- **当前事实**：`design` 通过自有 `references/principles.md` 的问题定义、用户与任务建模、证据化联想、旅程与状态设计、范围与优先级、成功衡量及澄清沟通七项能力，从目标用户与业务结果定义可实现、可验收的产品契约；不裁定系统架构、具体 API、Schema、组件或视觉实现。
- **代码定位**：`skills/design/SKILL.md#专业能力`；`skills/design/references/principles.md#核心能力`；`skills/design/SKILL.md#产品契约`
- **影响范围**：`architecture` 接收共享规则与质量期望，`frontend` 接收任务顺序、信息、动作和状态契约，`backend` 接收业务动作与结果，`verification` 接收验收条件和异常路径。
- **验证入口**：`python3 -X utf8 scripts/validate_project.py --self-test` 检查产品设计必需语义与技术越界反例；静态检查不证明具体任务中的产品判断质量。
