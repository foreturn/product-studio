# software-architecture 当前产品事实

## 十技能自主发现拓扑

- **当前事实**：插件暴露 `product-management`、`product-experience`、`software-architecture`、`backend-engineering`、`frontend-engineering`、`database-engineering`、`security-engineering`、`quality-engineering`、`release-engineering` 与 `fact-sync` 十项 Skill，不设中央 Router 或固定技能链；各技能的触发描述共同构成发现面，Codex 依据任务、仓库事实、风险和缺失判断自主选择适用能力与工作顺序。
- **权威依据**：`README.md#十项 Skill`；`.codex-plugin/plugin.json#skills`；`skills/*/SKILL.md#frontmatter`
- **影响边界**：Codex 与 Claude Code 的技能发现、专业判断、实现验证、发布和事实同步均依赖该拓扑；静态描述可触发不等于已在真实新上下文中证明自主选择正确。
- **复核入口**：核对 `skills/` 恰有十个与 frontmatter 同名的目录且不存在 `router`，并扫描专业资料不含固定调用链；再于安装当前源快照后的全新上下文，以未点名 Skill 的单域、跨域、数据库、安全、验收和发布场景检查实际命中、顺序判断与越权。

## 专业所有权边界

- **当前事实**：产品管理唯一裁定为何、为谁、做什么与何谓成功，产品体验唯一裁定用户如何完成；软件架构拥有跨边界职责、数据主权、共享不变量和系统质量权衡，数据库工程拥有物理 Schema、约束、索引、隔离锁和数据库迁移，安全工程拥有威胁、身份授权、秘密隐私和风险政策；前后端落实代码，质量工程给出独立完成裁决，发布工程拥有生产执行与健康，事实同步只机械应用专业 Owner 的事实裁决。
- **权威依据**：`skills/software-architecture/SKILL.md#专业边界`；`skills/product-management/SKILL.md#唯一决策权`；`skills/fact-sync/SKILL.md#边界`
- **影响边界**：API、Schema、事务、授权、迁移、浏览器行为、质量结论、生产操作与事实正文均只有一个裁决来源；遇到缺失的专业语义时应暴露缺口，不得就地补写第二套规则，后续能力与顺序仍由 Codex 按任务决定。
- **复核入口**：以同时涉及业务资格、移动端体验、跨服务一致性、表约束、租户越权和发布迁移的场景逐项核对唯一 Owner 与越权停止条件；检查工程技能不得改写数据库或安全政策，`fact-sync` 不得产生事实语义，也不得由专业资料预设完整调用链。

## 终态事实同步架构

- **当前事实**：源码、权威 Schema、流水线、制品库和环境查询始终是事实权威；九个专业 Owner 的 `memory.md` 按本专业事实类型分别规定入册条件、主题合并键、四栏写法、证据、影响、复核、四态变更和专属禁项。每次可写实现、验收或发布形成经验证终态后必须执行事实同步检查，只有事实新增、改变或消失才最小落盘；`fact-sync` 没有 `memory.md` 或自身事实册，也不裁定事实语义。
- **权威依据**：`README.md#当前项目事实`；`skills/software-architecture/references/memory.md#共同定位与写入契约`；`skills/fact-sync/SKILL.md#不可绕过的规则`
- **影响边界**：各产品事实位于 `docs/product-studio/<product-id>/` 并按产品和 Owner 隔离；旧 `design.md`、`architecture.md`、`backend.md`、`frontend.md`、`verification.md` 与 `release.md` 是稳定 locator，技能改名不机械迁移这些文件。
- **复核入口**：检查九份专业 `memory.md` 均定义唯一语义 Owner、locator、四栏格式，并将每种专业事实写成含八项规则的独立类型，`fact-sync` 无 `memory.md`；以终态通过、验证失败、事实删除、路径搬移、零变化、多产品和 `product-id` 歧义场景检查写入、阻塞及不触碰文件行为。
