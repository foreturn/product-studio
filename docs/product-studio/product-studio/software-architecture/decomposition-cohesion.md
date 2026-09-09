# software-architecture 当前产品事实 · 分解、内聚与代码组织

## 自主发现的专业技能拓扑

- **当前事实**：Product Studio 以同级、独立 Skill 暴露专业能力，编码代理依据请求、仓库证据和风险自主选择与排序；插件没有中央路由，各 Skill 不声明固定前置、后继或移交目标。
- **权威依据**：`README.md#技能组织`；`.codex-plugin/plugin.json`；`skills/`；`.claude-plugin/plugin.json`。
- **影响边界**：任务可命中多个专业，职责集合见 `docs/product-studio/product-studio/product-management/scope-priority.md#十一项通用专业底座`；技能数量不能代替交付完整性判断。
- **复核入口**：对照技能目录与双端清单评审所有权，再以具体任务检查选择依据与越权裁决；发现机制或专业拓扑变化时重审。

## 专业内容三层分离

- **当前事实**：README 介绍项目；`SKILL.md` 承载发现摘要、目标、执行协议与项目记忆协议；专业准则和记忆范围分别按同名能力簇放在 `references/principles/` 与 `references/memory/`。`references/principles.md` 仅以任务条件索引准则，链接相对索引解析；`agents/openai.yaml` 只承载界面元数据。簇按可独立触发的变化原因及必须共同加载的记忆划分：Android、iOS 的应用结构、生命周期恢复、构建兼容分别成簇，Web 的 SEO 与页面元数据独立成簇。
- **权威依据**：`README.md#技能组织`；各专业 `SKILL.md` 与 `references/principles.md`；`skills/android-engineering/references/principles.md`；`skills/ios-engineering/references/principles.md`；`skills/web-engineering/references/principles.md`。
- **影响边界**：任务按变化、风险和依赖完整读取命中分卷，出现新边界时补读；不按固定簇数组织内容。记忆卷只定义应保留的项目认知，具体项目事实另存于产品目录。
- **复核入口**：用结构整理、生命周期恢复、构建升级与公开页面收录任务核对索引、准则和记忆范围是否同义；文件职责或簇边界变化时重审。

## 完整业务流优先的能力复用与极简实现

- **当前事实**：软件架构、后端与三端工程共同要求从真实入口追踪至可确认结果，先确定业务能力所有者、共同不变量和真实消费者，再决定复用与抽象；接口、任务、页面和系统入口中的适配差异不另造业务权威。技术机制复用须在业务职责清楚后评估，完整满足行为与边界的方案再比较总维护成本。
- **权威依据**：`skills/software-architecture/references/principles/decomposition-cohesion.md`；`skills/backend-engineering/references/principles/domain-structure.md`；`skills/web-engineering/references/principles/structure-delivery.md`；`skills/android-engineering/references/principles/structure-delivery.md`；`skills/ios-engineering/references/principles/structure-delivery.md`。
- **影响边界**：约束服务端与客户端的公共业务能力和适配边界，不为假想消费者预建框架，也不以去重删除权限、事务、数据、副作用或恢复约束。
- **复核入口**：沿多入口核对共同能力与结果语义，再检查等价变体、相邻业务和失败恢复；能力所有权、真实消费者或复用边界变化时重审。

## 方法论与专业编码约束的归属

- **当前事实**：三思、拆解和阶段自检由各 Skill 的执行协议独立承载；职责归类、命名、常量与状态、副作用隔离和抽象取舍的具体标准归相应专业簇。对应记忆卷记录项目实际采用的组织边界，不另建方法论技能或固定技能链。
- **权威依据**：`skills/*/SKILL.md#执行协议`；`skills/*/references/principles.md` 及其关联准则与同名记忆卷。
- **影响边界**：专业代码整理可以直接命中所属工程技能；通用方法的演进约束见 `docs/product-studio/product-studio/software-architecture/drivers-evolution.md`。统一命名与去重不能抹除真实业务语义或必要隔离。
- **复核入口**：用模块整理、外部机制隔离、客户端状态归属和测试夹具复用核对专业归属与规则完整性；方法承载位置或专业职责变化时重审。

## 项目记忆边界

- **当前事实**：事实路径锚定 `<当前产品根目录>/docs/product-studio/<product-id>/<owner>/<簇卷文件名>.md`，簇名对应本专业准则。根目录按用户明确范围及产品证据确认，不要求 Git，也不能单凭进程或技能目录推定；插件仅提供技能时，其源码、安装与缓存目录不是目标产品。根目录或安全单级 `product-id` 不唯一时暂停事实册操作。先读命中簇的记忆范围和事实，涉及其他簇或专业约束时沿相关引用补读并核对权威，已读内容不重复加载；缺失或失效引用回到当前产品证据。同一认知只在主责专业与簇存一份，其他簇只记录相关影响和相对产品根的事实引用。
- **权威依据**：各专业 `SKILL.md#项目记忆`。
- **影响边界**：协议随每项 Skill 独立加载，使无 Git 产品、插件提供者目录与跨簇引用均有明确边界；首条事实建册，末条移除删文件，空目录清理止于 Owner 及其空的产品标识目录。记忆准入与写权限见 `docs/product-studio/product-studio/product-management/problem-users-policy.md#项目核心记忆政策`；敏感内容排除见 `docs/product-studio/product-studio/security-engineering/privacy-data-lifecycle.md`。
- **复核入口**：用无 Git 产品、产品与插件目录并存、根目录歧义、跨簇引用、循环或失效引用、首条建册与末条清理核对定位和读写行为；结构检查不能代替真实任务中的选择、维护与复用证据。目录模型、引用机制或专业所有权变化时重审。
