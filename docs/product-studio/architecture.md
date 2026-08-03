# architecture 当前代码事实

## 六技能职责拓扑

- **当前事实**：插件只注册 `router`、`design`、`architecture`、`backend`、`frontend`、`verification` 六个可调用 Skill；`router` 只负责选链、依赖、并行、失败隔离与停止编排，最终结果由 `verification` 独立裁决；产品设计、系统架构、服务端实现和界面实现各有唯一职责，生产写操作位于插件边界之外。
- **代码定位**：`skills/router/SKILL.md#裁决边界`；`skills/architecture/SKILL.md#系统架构设计`；`README.md#六个 Skill`
- **影响范围**：双端插件清单、最小调用链、五份技能自有记忆卷、专业能力加载、编排停止条件和独立验收结论均依赖该职责边界。
- **验证入口**：`python3 -X utf8 scripts/validate_project.py --self-test` 检查技能目录精确集合、Skill frontmatter、职责关键词、旧 callable 清除及第七技能退化；不证明真实自动触发行为。

## 架构与后端交接

- **当前事实**：`architecture` 只在跨模块、进程、数据所有权、信任边界、部署单元、共享不变量或系统级质量风险存在时裁定边界、所有权、跨边界语义、故障与演进；`backend` 依据这些决定落实具体 API、Schema、事务和服务端代码，局部实现不强制经过架构设计。
- **代码定位**：`skills/architecture/SKILL.md#输入门禁`；`skills/architecture/SKILL.md#输出与交接`；`skills/backend/SKILL.md#输入门禁`
- **影响范围**：`router` 对技术任务的选链，`design`、`frontend`、`backend`、`verification` 的回退路径，以及架构卷与后端工程卷的唯一加载位置。
- **验证入口**：`python3 -X utf8 scripts/validate_project.py --self-test` 检查两项契约里程碑、两个 Skill 的精确 reference 集合、后端越权承担系统架构及产品设计技术越界反例。

## 专业能力与事实记忆分层

- **当前事实**：六份策展能力卷统一命名为各 Skill 自有的 `references/principles.md`，只承载专业判断；五个专业 Skill 的独立 `memory.md` 只承载本 Owner 的最终代码事实收录与同步规则，`router` 不拥有事实册。
- **代码定位**：`skills/design/SKILL.md#专业能力`；`skills/architecture/SKILL.md#专业能力`；`scripts/validate_project.py#validate_reference`
- **影响范围**：六份 `SKILL.md` 的条件加载、专业判断深度及项目校验；专业能力卷与技能记忆卷保持职责分离。
- **验证入口**：`python3 -X utf8 scripts/validate_project.py --self-test` 检查每个 Skill 的精确 reference 集合、策展哈希、四章结构、能力卡名称与最低正文深度；不能证明模型必然正确应用能力卡。
