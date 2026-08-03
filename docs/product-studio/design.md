# design 当前代码事实

## 最短产品使用路径

- **当前事实**：边界清楚的单一任务直达对应专业 Skill；只有目标用户、业务闭环、产品规则、交互体验、范围或验收仍不明确时才加入 `design`，系统架构由 `architecture` 承接，具体服务端实现由 `backend` 承接。
- **代码定位**：`skills/router/SKILL.md#直达与触发`；`skills/router/SKILL.md#最小调用链`；`README.md#路由`
- **影响范围**：使用插件的编码者、`router` 选链、`architecture`、`backend` 与 `frontend` 输入门禁；错误路由会增加无消费者设计或让下游猜测产品语义。
- **验证入口**：分别用明确单项、产品语义未定和跨端高风险三类原始请求作全新上下文试用，核对实际命中的 Skill 链、直达路径与越界情况；平台格式校验不证明真实选链。

## 产品设计职责

- **当前事实**：`design` 通过自有 `references/principles.md` 的现状与问题定义、用户角色任务建模、业务规则与闭环、任务旅程与信息动作、状态异常与恢复、范围与优先级、成功衡量与验收、假设未决与决策管理八项能力，形成下游可直接消费的产品设计结论；不裁定系统架构、具体 API、Schema、组件或视觉实现。
- **代码定位**：`skills/design/SKILL.md#专业能力`；`skills/design/references/principles.md#核心能力`；`skills/design/SKILL.md#输出与交接`
- **影响范围**：`architecture` 接收共享规则与质量期望，`frontend` 接收任务顺序、信息、动作和状态契约，`backend` 接收业务动作与结果，`verification` 接收验收条件和异常路径。
- **验证入口**：以未指定技术方案的产品请求调用 `design`，核对命中的能力能形成下游直接消费的产品设计结论，且不擅自决定 API、Schema、组件或视觉实现；结论只对绑定的上下文与输出成立。
