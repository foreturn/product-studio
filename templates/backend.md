---
schema: 4
memory: backend
scope: current-project-code
project_root: "."
updated_at: ""
---

# backend 代码事实

<!-- 每次成功编码终态都执行记忆同步检查。只收录已由当前代码与适用验证支持、预计后续仍会使用，且具有跨消费者、重查成本或误判风险的总结性事实；不逐接口、字段、文件或 Symbol 机械建卡。实例化后填写带时区时间，删除本说明、事实键目录、示例与所有占位；无事实变化时报告 memory: 0 keys changed，不改文件与 updated_at。语义不变时原位更新，事实消失时删除，最后一张事实删除后移除本文件；Git 承担历史。 -->

## 事实键

- `backend:domain:<slug>`：非显然的领域行为、状态转换与不变量。
- `backend:api:<slug>`：接口、错误、幂等与兼容语义；method 和 path 写入代码定位。
- `backend:data:<slug>`：数据生命周期、Schema、事务与并发约束。
- `backend:auth:<slug>`：可信服务端校验点上的授权规则。
- `backend:event:<slug>`：消息、任务、回调或领域事件的实际契约。
- `backend:integration:<slug>`：外部系统适配、超时、重试、幂等与失败恢复。
- `backend:runtime:<slug>`：不含秘密值的配置、可观测和运行行为。

## 当前代码事实

### backend:api:order-creation

- **事实摘要**：<已经成立的一项领域行为、接口／错误语义、数据、授权、事件或可靠性约束>
- **代码定位**：<一至三个 `仓库相对路径#精确位置`，精确位置使用权威 Route、Symbol、Schema、迁移或配置键>
- **依赖与影响**：<直接调用方、前端、服务、任务、消息、数据对象、外部系统或相关事实键；无则写“无”>
- **验证入口**：<可重复使用的测试、脚本、命令或检查入口，关键断言与稳定未覆盖边界>
- **失效条件**：<哪些领域规则、接口、Schema、权限、依赖、配置或消费者变化后必须同步本卡>
