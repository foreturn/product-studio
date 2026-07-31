---
schema: 3
memory: verification
scope: current-project-code
project_root: "."
updated_at: "2026-07-31T21:52:42+08:00"
---

# verification 代码事实

## 当前代码事实

### verification:check:plugin:static-contract

- **当前实现**：项目提供单一静态校验入口，检查五技能精确集合、五份裁剪后固定哈希与四章结构的能力 reference、四个 schema 3 代码事实模板、按 Owner 完整匹配的四段语义键、带 `#精确定位` 的本地源码锚点及 Markdown 真实标题、双端 manifest 与 marketplace 一致性、旧 callable 清除、局部任务直达、全栈 API 契约里程碑及生产外部操作的超范围边界；`--self-test` 会在临时副本中注入 13 类退化并要求全部被拒绝。
- **源码锚点**：`scripts/validate_project.py#main`；`scripts/README.md#校验脚本`；`README.md#校验`
- **关联与消费者**：五份 Skill、五份专业能力 reference、四份模板、当前 `design`／`verification` 事实文件及 Codex／Claude 插件清单。
- **验证证据**：稳定检查资产为 `scripts/validate_project.py#validate`、`scripts/validate_project.py#run_negative_self_tests` 及其 13 个隔离突变用例；适用环境为插件根目录、Python 3 与 UTF-8 模式，复现命令是 `python -X utf8 scripts/validate_project.py --self-test`；关键断言是基线无错误、每个突变均被拒绝且临时副本不改当前工作树，覆盖技能集合、reference 集合与裁剪后内容哈希、事实字段与语义键、源码锚点、模板骨架、旧调用及路由契约退化。
- **重验条件**：校验器、任一 Skill/reference/template/memory、README、Codex 或 Claude 清单发生变化。

### verification:constraint:external-operation:scope

- **当前实现**：五技能只设计、实现和验证产品代码；实际生产部署、生产迁移及其他生产写操作不属于本插件，不能由 router 或 verification 执行。代码检查、本地测试与静态校验也不能作为线上已执行或运行健康的证明。
- **源码锚点**：`skills/router/SKILL.md#裁决边界`；`skills/verification/SKILL.md#独立性与边界`；`README.md#路由`
- **关联与消费者**：五技能的代码完成判定；项目既有的环境专属工具、运行流程或责任人在插件之外接收已验收代码。
- **验证证据**：稳定检查资产为 `scripts/validate_project.py#validate_skill` 的 router 外部操作边界精确计数与 reference 集合检查；适用环境为插件源码树，复现命令是 `python -X utf8 scripts/validate_project.py`，关键断言是范围边界句恰出现一次、任何未声明能力卷均使校验失败，且 verification 边界仍禁止生产外部状态操作。
- **重验条件**：router 职责、verification 独立性、插件范围边界或外部操作交接方式变化。
