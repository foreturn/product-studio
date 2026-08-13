# product-experience 当前产品事实

## 产品体验裁决边界

- **当前事实**：`product-experience` 在产品目标、政策与范围明确后，唯一裁定用户入口与任务旅程、信息架构、动作语义与顺序、内容、用户可见状态与恢复、响应式和无障碍体验；它不扩大产品范围、不决定系统机制，也不编写前端代码。
- **权威依据**：`skills/product-experience/SKILL.md#唯一决策权`；`skills/product-experience/references/principles.md#静态所有权边界`
- **影响边界**：`frontend-engineering` 消费体验契约并裁定组件、状态代码、CSS 与浏览器实现，`quality-engineering` 消费角色、数据、设备、步骤、可见断言和恢复路径；产品政策仍归 `product-management` 唯一裁决，系统降级和恢复机制仍归 `software-architecture` 唯一裁决，本册不复制其正文。
- **复核入口**：以“订单页更好用”、移动表格、批量部分失败、无障碍、4px 间距和服务不可用场景检查产品意图、用户侧完成方式、系统机制、代码实现与质量证明各归唯一 Owner。

## 体验事实入口

- **当前事实**：已由最终实现和相称质量证据证实、后续会复用的旅程、信息架构、动作内容、可见状态恢复、响应式和无障碍约束进入 `docs/product-studio/<product-id>/product-experience.md`；产品管理事实仍留在稳定 locator `design.md`，前端实现细节留在 `frontend.md`。
- **权威依据**：`skills/product-experience/SKILL.md#当前产品事实`；`skills/product-experience/references/memory.md#事实册所有权与稳定位置`
- **影响边界**：体验方案、未实施原型、研究流水和单张截图不构成当前体验事实；同一体验语义不跨产品管理与前端实现事实册复制。
- **复核入口**：核对 `product-experience` 的四态裁决与四栏模板，并以纯体验方案、已实现旅程、实现路径搬移、最后消费者删除和零变化场景检查 `DEFERRED`、`ADD`、`UPDATE`、`DELETE` 与 `NO_CHANGE`。
