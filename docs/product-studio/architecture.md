# architecture 当前代码事实

## 七技能职责拓扑

- **当前事实**：插件注册 `router`、`design`、`architecture`、`backend`、`frontend`、`verification`、`release` 七个可调用 Skill；`router` 只负责选链、依赖、并行、失败隔离与停止编排，实现结果由 `verification` 独立裁决，发布就绪、授权、执行与健康由 `release` 独立裁决；其余专业职责各有唯一 Owner。
- **代码定位**：`skills/router/SKILL.md#裁决边界`；`skills/release/SKILL.md#边界`；`README.md#七个 Skill`
- **影响范围**：双端插件清单、最小调用链、六份技能自有记忆卷、专业能力加载、编排停止条件、独立验收与发布运行结论均依赖该职责边界。
- **验证入口**：核对插件清单与 `skills/` 只暴露七项约定 Skill，并在新线程用明确单项、跨端、高风险与发布请求检查直达、编排、独立验收及授权边界；平台清单校验不证明真实自动触发行为。

## 架构与后端交接

- **当前事实**：`architecture` 只在跨模块、进程、数据所有权、信任边界、部署单元、共享不变量或系统级质量风险存在时裁定边界、所有权、跨边界语义、故障与演进；`backend` 依据这些决定落实具体 API、Schema、事务和服务端代码，局部实现不强制经过架构设计。
- **代码定位**：`skills/architecture/SKILL.md#输入门禁`；`skills/architecture/SKILL.md#输出与交接`；`skills/backend/SKILL.md#输入门禁`
- **影响范围**：`router` 对技术任务的选链，`design`、`frontend`、`backend`、`verification` 的回退路径，以及架构卷与后端工程卷的唯一加载位置。
- **验证入口**：用同时涉及数据所有权与具体 API 的全新任务检查 `architecture` 先裁定跨边界语义、`backend` 再落实字段与实现，并以局部后端任务确认不会强制经过架构设计。

## 专业能力与事实记忆分层

- **当前事实**：七份策展能力卷统一命名为各 Skill 自有的 `references/principles.md`，只承载专业判断；六个专业 Skill 的独立 `memory.md` 只承载本 Owner 的当前事实收录与同步规则，`router` 不拥有事实册，`release` 的易变运行事实必须绑定环境、制品、核验时点与失效条件。
- **代码定位**：`skills/design/SKILL.md#专业能力`；`skills/architecture/SKILL.md#当前代码事实记忆`；`README.md#当前代码事实`
- **影响范围**：七份 `SKILL.md` 的条件加载、专业判断深度及后续事实检索；专业能力卷与技能记忆卷保持职责分离。
- **验证入口**：核对每个 Skill 只引用本目录的 `principles.md`，六个专业 Skill 另各自拥有唯一 `memory.md`，且 `router` 不拥有事实册；是否正确应用能力仍须绑定具体任务输出判断。
