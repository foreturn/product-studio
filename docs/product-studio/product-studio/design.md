# product-management 当前产品事实

## 产品管理裁决边界

- **当前事实**：`product-management` 唯一裁定当前增量的目标用户与问题、期望业务结果、产品层业务政策、范围与优先级、成功指标、非目标和验收语义；用户旅程、信息架构、内容、可见状态与无障碍体验由 `product-experience` 裁定，技术方案和质量结论分别由相应专业 Owner 承担。
- **权威依据**：`skills/product-management/SKILL.md#唯一决策权`；`skills/product-management/references/principles.md#静态所有权边界`；`skills/product-experience/SKILL.md#唯一决策权`
- **影响边界**：产品、体验、架构、前后端、数据库、安全与质量技能消费同一套目标、业务政策、范围和 `AC-ID`，不得因实现成本或现状代码静默改变产品意图。
- **复核入口**：以“增加审批按钮”“提升转化率”“纯接口重构”和“管理员删除记录”等未点名 Skill 的场景，检查只在产品语义会令下游猜测时触发，并核对输出含依据、消费者、失效条件与可观察验收而不指定 UI、API、Schema 或测试结论。

## 产品事实稳定入口

- **当前事实**：`product-management` 的累计当前事实继续使用 `docs/product-studio/<product-id>/design.md` 作为稳定 locator；文件名不随 Skill 名变化，也不另建 `product-management.md` 复制同一事实。纯产品方案、候选范围和未实现假设不入册。
- **权威依据**：`skills/product-management/SKILL.md#当前产品事实`；`skills/product-management/references/memory.md#事实册所有权与稳定位置`
- **影响边界**：外部项目既有 `design.md` 的读取与终态同步保持可达；产品体验事实进入 `product-experience.md`，其余专业事实进入各自唯一事实册。
- **复核入口**：核对产品管理事实规则将 `design.md` 定义为稳定 locator，并以既有 `design.md`、新产品首次产生事实、质量失败和 `NO_CHANGE` 四类场景验证不机械迁移、不提前落盘且零变化不触碰文件。
