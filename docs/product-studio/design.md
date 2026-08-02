# design 当前代码事实

## 最短产品使用路径

- **当前事实**：边界清楚的单一任务直达对应专业 Skill；只有目标用户、业务闭环、产品规则、交互体验、范围或验收仍不明确时才加入 `design`，系统架构与技术契约直接由 `backend` 承接。
- **代码定位**：`skills/router/SKILL.md#直达与触发`；`skills/router/SKILL.md#最小调用链`；`README.md#路由`
- **影响范围**：使用插件的编码者、`router` 选链、`backend` 与 `frontend` 输入门禁；错误路由会增加无消费者设计或让实现技能猜测产品语义。
- **验证入口**：`python3 -X utf8 scripts/validate_project.py --self-test` 检查产品设计与系统架构归属、常规终端验证不触发 router 及 API 契约里程碑；真实选链仍需全新上下文试用。

## 产品设计职责

- **当前事实**：`design` 从目标用户与业务结果出发，定义最短任务路径、必要信息与动作、状态反馈、失败恢复、端到端业务闭环、范围和可观察验收；不裁定系统架构、API、Schema、组件或视觉实现。
- **代码定位**：`skills/design/SKILL.md#产品设计原则`；`skills/design/SKILL.md#产品契约`；`skills/design/SKILL.md#边界`
- **影响范围**：`frontend` 接收任务顺序、信息、动作和状态契约，`backend` 接收业务对象、规则与产品结果，`verification` 接收验收条件和异常路径。
- **验证入口**：`python3 -X utf8 scripts/validate_project.py --self-test` 检查产品设计必需语义与技术越界反例；静态检查不证明具体任务中的产品判断质量。
