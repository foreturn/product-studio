# verification 当前代码事实

## 插件静态契约检查

- **当前事实**：项目以单一 Python 入口静态检查六技能、六份专业能力卷、五份技能自有记忆卷及其最终事实格式、实例主题、四字段、代码定位、路由边界和双端插件清单，并用隔离突变验证关键退化会被拒绝。
- **代码定位**：`scripts/validate_project.py#validate`；`scripts/validate_project.py#run_negative_self_tests`；`scripts/README.md#校验脚本`
- **影响范围**：六份 Skill、六份专业能力 reference、五份技能自有 `references/memory.md`、当前 design／architecture／backend／verification 事实册及插件清单；覆盖产品、架构、后端职责、最终代码事实记忆和专业能力分层。
- **验证入口**：在插件根运行 `python3 -X utf8 scripts/validate_project.py --self-test`；关键断言是当前快照无结构错误、无实例事实册仍合法、38 类退化各自命中对应诊断且临时副本不改工作树。该入口不证明事实语义已随最终代码更新，也不证明真实插件触发、目标项目运行或线上行为。

## 外部操作边界

- **当前事实**：六技能只设计、实现和验证产品代码；实际生产部署、生产迁移及其他生产写操作不属于本插件，本地检查和静态绿灯也不能外推为线上已执行或生产健康。
- **代码定位**：`skills/router/SKILL.md#裁决边界`；`skills/verification/SKILL.md#独立性与边界`；`README.md#路由`
- **影响范围**：六技能职责边界、六技能完成判定，以及插件之外承接已验证代码的环境专属工具与运行责任人。
- **验证入口**：`python3 -X utf8 scripts/validate_project.py` 静态检查 router 的生产操作边界与 verification 禁止外部环境写入；该检查不能证明真实环境未被其他工具修改。
