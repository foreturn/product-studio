# frontend-engineering 当前产品事实

## 前端实现职责

- **当前事实**：`frontend-engineering` 将已确认的产品体验落实为路由、页面、请求适配、客户端状态、组件、表单、设计令牌、响应式、无障碍、安全与性能代码，并以真实浏览器、视口、输入方式、网络和控制台证据自检；用户旅程、信息架构、动作语义和用户可见恢复由 `product-experience` 裁定。
- **权威依据**：`skills/frontend-engineering/SKILL.md#输入与证据门槛`；`skills/frontend-engineering/SKILL.md#实施方法`；`skills/frontend-engineering/references/principles.md#核心能力`
- **影响边界**：页面、路由、组件、样式、请求层与浏览器行为由本技能实现；产品政策、体验契约、服务端语义、最终质量结论和生产状态不由前端实现反向决定。
- **复核入口**：以 4px 样式修复、移动表格信息取舍、部分成功恢复、无障碍与服务不可用五类场景检查直接实现、语义缺口暴露与越权停止；实现自检不得以构建、自动扫描或单张截图代替独立质量裁决。

## 前端事实稳定入口

- **当前事实**：`frontend-engineering` 唯一裁决稳定 locator `docs/product-studio/<product-id>/frontend.md` 中的前端实现事实；它只形成 `ADD`、`UPDATE`、`DELETE` 或 `NO_CHANGE` 候选，`fact-sync` 在终态与质量门禁通过后机械落盘。
- **权威依据**：`skills/frontend-engineering/SKILL.md#当前产品事实`；`skills/frontend-engineering/references/memory.md#产品定位与事实实例`
- **影响边界**：外部项目既有 `frontend.md` 保持可达；用户旅程和体验约束正文进入 `product-experience.md`，服务端、安全和质量事实各归其 Owner。
- **复核入口**：核对稳定 locator、唯一语义 Owner、真实渲染证据要求与四态裁决包；用组件实现搬移、状态能力消失及零变化场景检查最小更新与不触碰文件行为。
