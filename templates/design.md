---
schema: 3
memory: design
scope: current-project-code
project_root: ""
updated_at: ""
---

# design 代码事实

<!-- 仅在项目首次产生值得跨会话保留的产品或系统事实时复制本模板。实例化后填写项目根和带时区时间，删除本说明、事实键目录、示例与所有占位。同一语义键原位更新，新增代码事实时新增键，源码及消费者删除后删除键；Git 承担历史，既有事实文件不再次套用模板。 -->

## 事实键

- `design:product:journey:<name>`：代码实际支持的用户任务、状态反馈与恢复路径。
- `design:product:rule:<name>`：已实现的业务规则、例外、权限差异与边界。
- `design:product:acceptance:<name>`：当前产品行为可观察、可复核的验收契约。
- `design:system:boundary:<name>`：实际模块或领域边界、数据所有权与写入责任。
- `design:system:contract:<name>`：跨模块、前后端或外部系统间的实际契约与兼容关系。
- `design:system:invariant:<name>`：实现必须维持的一致性、安全、可靠性或性能不变量。
- `design:system:decision:<name>`：已采纳并在当前代码生效的架构决定与取舍。
- `design:system:migration:<name>`：现行兼容阶段、数据演进顺序与不可逆边界。

## 当前代码事实

### design:system:contract:order-creation

- **当前实现**：<从当前代码与已确认产品契约中可直接证明的行为、边界或不变量>
- **源码锚点**：<相对项目根的文件路径、符号、契约、路由或 schema 定位>
- **关联与消费者**：<受该事实约束的模块、接口、页面或相关事实键；无则写“无”>
- **验证证据**：<源码检查、契约测试、架构测试或可复现运行证据>
- **重验条件**：<哪些产品契约、边界、数据流或实现变化后必须重新核验>
