# backend 当前代码事实

## 五技能技术职责边界

- **当前事实**：插件只注册 `router`、`design`、`backend`、`frontend`、`verification` 五个可调用 Skill；`design` 负责产品设计，`backend` 负责系统架构与服务端实现，`frontend` 负责界面实现，`verification` 独立裁决，生产写操作位于插件边界之外。
- **代码定位**：`skills/router/SKILL.md#裁决边界`；`skills/backend/SKILL.md#后端与系统架构`；`README.md#五个 Skill`
- **影响范围**：双端插件清单、最小调用链、四份技能自有记忆卷、专业能力加载和完成判定均依赖该职责边界。
- **验证入口**：`python3 -X utf8 scripts/validate_project.py --self-test` 检查技能目录精确集合、Skill frontmatter、职责关键词、旧 callable 清除及第六技能退化；不证明真实自动触发行为。

## 系统架构归属

- **当前事实**：系统边界、数据所有权、跨模块契约、质量属性、故障安全、可观测性和演进由 `backend` 裁定；跨边界时加载架构能力卷，进入服务端实现时再组合后端工程卷，具体 API 由后端或实际契约 Owner 形成里程碑。
- **代码定位**：`skills/backend/SKILL.md#条件加载专业能力`；`skills/backend/SKILL.md#架构流程`；`skills/router/SKILL.md#编排规则`
- **影响范围**：`router` 对技术边界任务的选链，`design`、`frontend`、`verification` 的回退路径，以及架构卷的唯一加载位置。
- **验证入口**：`python3 -X utf8 scripts/validate_project.py --self-test` 检查 backend 精确 reference 集合、两份能力卷加载、系统架构职责词和设计技能技术越界反例。

## 最终代码事实记忆

- **当前事实**：`design`、`backend`、`frontend`、`verification` 各自在同技能 `references/memory.md` 维护唯一记忆规则，只以人类可读主题保存当前项目的最终代码事实；每条事实仅含当前事实、代码定位、影响范围和验证入口，重构、迁移及变更过程不入册，`router` 不判断主题也不拥有事实册。
- **代码定位**：`skills/design/references/memory.md#实例格式`；`skills/backend/references/memory.md#终态同步`；`skills/router/SKILL.md#终态收口`
- **影响范围**：四个专业 Skill、目标项目的 `docs/product-studio/*.md` 和插件静态契约检查；跨 Owner 只描述当前消费者与依赖关系，不复制正文或建立形式化事实键。
- **验证入口**：`python3 -X utf8 scripts/validate_project.py --self-test` 检查四份技能自有记忆卷、人类可读主题、四字段、代码定位、最终状态表述和过程记忆退化。

## 专业能力与记忆分层

- **当前事实**：五份策展专业能力卷只承载专业判断；`design` 的产品规则直接位于主 Skill，`backend` 拥有架构与后端工程两卷；四个专业 Skill 的独立 `memory.md` 只承载本 Owner 的最终代码事实收录与同步规则。
- **代码定位**：`skills/backend/SKILL.md#条件加载专业能力`；`skills/router/references/delivery-capabilities.md#核心能力`；`scripts/validate_project.py#validate_reference`
- **影响范围**：五份 `SKILL.md` 的条件加载、专业判断深度及项目校验；专业能力卷与技能记忆卷保持职责分离。
- **验证入口**：`python3 -X utf8 scripts/validate_project.py --self-test` 检查每个 Skill 的精确 reference 集合、策展哈希、四章结构、能力卡名称与最低正文深度；不能证明模型必然正确应用能力卡。
