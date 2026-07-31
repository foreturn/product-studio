---
schema: 3
memory: verification
scope: current-project-code
project_root: ""
updated_at: ""
---

# verification 代码事实

<!-- 仅在项目首次产生值得跨会话保留的验证事实时复制本模板。实例化后填写项目根和带时区时间，删除本说明、事实键目录、示例与所有占位。同一语义键原位更新，新增代码事实时新增键，源码及消费者删除后删除键；Git 承担历史，既有事实文件不再次套用模板。 -->

## 事实键

- `verification:check:<surface>:<behavior>`：可重复执行的验证目标、入口与终态断言。
- `verification:coverage:<risk>:<scope>`：风险范围当前由哪些测试或证据覆盖，并明确仍未覆盖的边界。
- `verification:constraint:<surface>:<invariant>`：必须持续成立的数据、安全、兼容或体验不变量。

## 当前代码事实

### verification:check:api:order-idempotency

- **当前实现**：<当前代码库中可重复验证的检查、覆盖或不变量>
- **源码锚点**：<测试、脚本、配置、被测入口或相关代码的精确定位>
- **关联与消费者**：<所验证的 design、backend、frontend 事实键及使用者；无则写“无”>
- **验证证据**：<可复用测试、脚本或夹具，适用环境、关键断言与复现命令；不逐轮刷新单次结果>
- **重验条件**：<哪些被测代码、测试、环境或依赖变化后证据失效>
