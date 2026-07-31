---
schema: 3
memory: backend
scope: current-project-code
project_root: ""
updated_at: ""
---

# backend 代码事实

<!-- 仅在项目首次产生值得跨会话保留的后端代码事实时复制本模板。实例化后填写项目根和带时区时间，删除本说明、事实键目录、示例与所有占位。同一语义键原位更新，新增代码事实时新增键，源码及消费者删除后删除键；Git 承担历史，既有事实文件不再次套用模板。 -->

## 事实键

- `backend:api:<method>:<path>`：已注册 API 的方法、路径与实际契约。
- `backend:schema:<store>:<object>`：数据库、缓存或持久化对象的实际结构与约束。
- `backend:auth:<resource>:<action>`：可信服务端校验点上的授权规则。
- `backend:event:<channel>:<name>`：消息、任务、回调或领域事件的实际契约。
- `backend:integration:<system>:<operation>`：外部系统适配、超时、重试、幂等与失败语义。
- `backend:config:<service>:<name>`：影响运行行为的配置、默认值与读取位置。

## 当前代码事实

### backend:api:post:/orders

- **当前实现**：<代码中已经成立的精确行为、契约或约束>
- **源码锚点**：<相对项目根的文件路径、符号、路由或 schema 定位>
- **关联与消费者**：<上游调用者、下游对象及相关事实键；无则写“无”>
- **验证证据**：<证明该事实的源码检查、测试、构建或运行结果>
- **重验条件**：<哪些源码、契约、配置或依赖变化后必须重新核验>
