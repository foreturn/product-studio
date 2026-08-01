---
schema: 4
memory: verification
scope: current-project-code
project_root: "."
updated_at: ""
---

# verification 代码事实

<!-- 每次成功编码终态都执行记忆同步检查。只收录当前代码库可重复使用的检查入口、稳定覆盖关系或必须持续守住的总结性事实；不为单次验收、某轮通过、临时失败或命令流水建卡。实例化后填写带时区时间，删除本说明、事实键目录、示例与所有占位；无事实变化时报告 memory: 0 keys changed，不改文件与 updated_at。语义不变时原位更新，事实消失时删除，最后一张事实删除后移除本文件；Git 承担历史。 -->

## 事实键

- `verification:check:<slug>`：可重复执行的检查入口、关键断言与适用环境。
- `verification:coverage:<slug>`：风险当前由哪些层级直接覆盖，以及稳定未覆盖边界。
- `verification:constraint:<slug>`：必须持续成立的数据、安全、兼容、体验或环境不变量。

## 当前代码事实

### verification:check:order-idempotency

- **事实摘要**：<一项可重复执行的检查、稳定风险覆盖或必须持续守住的验证约束>
- **代码定位**：<一至三个 `仓库相对路径#精确位置`，精确位置使用权威测试、脚本、配置、夹具、被测入口或实现 Symbol>
- **依赖与影响**：<所验证的 design、backend、frontend 事实键、要求、实现或测试套件；无则写“无”>
- **验证入口**：<稳定测试、脚本、命令和适用环境，关键断言与证据边界>
- **失效条件**：<哪些被测代码、契约、夹具、环境能力、依赖或浏览器变化后必须同步本卡>
