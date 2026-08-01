---
schema: 4
memory: verification
scope: current-project-code
project_root: "."
updated_at: "2026-08-01T08:39:25+08:00"
---

# verification 代码事实

## 当前代码事实

### verification:check:plugin-static-contract

- **事实摘要**：项目以单一 Python 入口静态检查五技能、五份专业能力卷、共享记忆契约、四份 schema 4 模板、实例摘要、代码定位、跨卡链接、路由边界和双端插件清单，并用隔离突变验证关键退化会被拒绝。
- **代码定位**：`scripts/validate_project.py#validate`；`scripts/validate_project.py#run_negative_self_tests`；`scripts/README.md#校验脚本`
- **依赖与影响**：五份 Skill、五份专业能力 reference、`references/project-memory.md`、四份模板、当前 design／verification 事实册及插件清单；对应 `design:invariant:summary-memory` 与 `design:invariant:capability-layering`。
- **验证入口**：在插件根运行 `python3 -X utf8 scripts/validate_project.py --self-test`；关键断言是当前快照无结构错误、无实例事实册仍合法、23 类退化各自命中对应诊断且临时副本不改工作树。该入口不证明事实语义已随最终差异更新，也不证明真实插件触发、目标项目运行或线上行为。
- **失效条件**：校验器、任一 Skill、专业或共享 reference、模板、实例事实册、README、Codex 或 Claude 清单变化。

### verification:constraint:external-operation-scope

- **事实摘要**：五技能只设计、实现和验证产品代码；实际生产部署、生产迁移及其他生产写操作不属于本插件，本地检查和静态绿灯也不能外推为线上已执行或生产健康。
- **代码定位**：`skills/router/SKILL.md#裁决边界`；`skills/verification/SKILL.md#独立性与边界`；`README.md#路由`
- **依赖与影响**：`design:boundary:skill-topology`、五技能完成判定，以及插件之外承接已验证代码的环境专属工具与运行责任人。
- **验证入口**：`python3 -X utf8 scripts/validate_project.py` 静态检查 router 的生产操作边界与 verification 禁止外部环境写入；该检查不能证明真实环境未被其他工具修改。
- **失效条件**：router 职责、verification 独立性、插件范围、生产操作授权或外部运行交接方式变化。
