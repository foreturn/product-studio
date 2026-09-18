# 产品工作室

产品工作室是一套面向 Codex、Claude Code 与 Google Antigravity 的软件工程专业技能插件。编码代理仍直接理解请求、阅读仓库、编写代码并自主决定需要哪些专业判断；插件以十一项 Skill 提供清晰的专业所有权、实施准则与证据约束，并由每项命中 Skill 读取和维护相关项目核心记忆。

它不提供中央路由，不要求预先写成套计划，也不规定固定技能链。一个任务可以只使用一项 Skill，也可以按证据需要组合多项；未命中的专业内容不会被机械加载。

## 十一项通用底座

| Skill | 唯一专业边界 |
|---|---|
| `product-management` | 产品问题、用户与利益相关者、结果价值、业务资格与产品结果政策、状态语义、范围优先级、指标验收，以及旅程、信息架构、内容、动作反馈、恢复、响应式、无障碍、可用性、视觉层级与设计系统语义。 |
| `software-architecture` | 系统上下文、跨模块与跨服务职责、系统与部署边界、数据主权、跨边界交互、质量属性权衡、故障恢复、可运行性和演进约束。 |
| `backend-engineering` | 领域与应用服务、API 和错误、事务一致性、并发幂等、持久化适配、缓存、事件任务、外部集成、服务端性能和可观测实现。 |
| `web-engineering` | 浏览器运行时、路由、DOM 与 CSS、客户端状态、网络交互、表单、响应式、Web 无障碍、本地化与双向文本、兼容、安全和性能实现。 |
| `android-engineering` | Android 生命周期与进程恢复、Compose/View、导航与深链、离线数据、后台工作、权限、存储网络、本地化与双向文本、性能、兼容和平台测试。 |
| `ios-engineering` | iOS 生命周期与状态恢复、SwiftUI/UIKit、导航与 Universal Links、网络 API、并发、持久化、后台能力、隐私权限、Keychain、本地化与双向文本、性能和平台测试。 |
| `database-engineering` | 服务端、共享或独立运营数据库的物理 Schema、键与约束、索引和执行计划、事务隔离与锁、迁移回填、生命周期容量、备份恢复、复制和高可用；客户端私有本地库归对应端。 |
| `platform-engineering` | 环境与账户、IaC 和状态、网络 DNS、计算容器、编排、运行配置注入、CI 运行平台、观测平台、容量弹性、恢复、纯可用性事故治理、成本与漂移。 |
| `security-engineering` | 资产与威胁、身份会话、授权强制与租户隔离、API 滥用、秘密密码学、隐私、供应链、安全配置、安全事故响应与取证、漏洞处置。 |
| `quality-engineering` | 独立验收对象、风险覆盖、测试架构、环境夹具、功能与数据、用户界面与无障碍、非功能证据、缺陷归因和退出裁决。 |
| `release-engineering` | 发布对象、版本 Tag、不可变制品、环境就绪、兼容迁移、部署切流、健康观察、停止恢复、分发映射和操作授权。 |

产品管理覆盖产品意图与体验语义，各工程技能负责相应实现与专业判断。客户端私有本地存储归对应端，共享或独立运营的数据库归数据库工程；产品资格政策与安全授权强制也分别由产品管理和安全工程承担。

当前范围面向应用型产品软件。数据工程、机器学习系统、硬件与嵌入式等专门领域可按项目需要扩展。

## 技能组织

每项技能由入口、专业准则和记忆范围组成，具体执行规则保存在技能文件中：

| 文件 | 用途 |
|---|---|
| `SKILL.md` | 技能目标、执行方法与项目记忆使用协议。 |
| `references/principles.md` | 专业能力索引，按任务条件定位相关能力簇。 |
| `references/principles/` | 按能力簇组织的专业判断标准与工程约束。 |
| `references/memory/` | 按能力簇分卷定义本专业关注的项目核心认知。 |
| `agents/openai.yaml` | 技能的界面元数据与调用示例。 |

专业准则与记忆范围按同名能力簇对应，便于任务只加载相关内容。不同技能独立维护自己的专业范围，可以按需组合使用。

## 项目记忆

项目记忆帮助后续任务理解已有的业务边界、状态来源、兼容约束和恢复关系，减少重复梳理。事实册按产品、专业和能力簇保存在所处理产品的目录中：

```text
<current-product-root>/docs/product-studio/<product-id>/<owner>/<能力簇卷文件名>.md
```

这里的产品目录指本次任务所处理的产品，支持尚未初始化 Git 的项目。事实册记录持续影响专业判断的当前认知；代码、配置与运行证据仍是事实依据。各技能的 `SKILL.md` 包含具体的定位、读取、授权与维护规则。

## 目录

```text
product-studio/
|-- plugin.json                   # 插件清单（Antigravity 与通用）
|-- skills/                       # 十一项自主发现的专业 Skill
|   `-- <skill>/
|       |-- SKILL.md              # 统一执行契约
|       |-- agents/openai.yaml
|       `-- references/
|           |-- principles.md     # 能力簇瘦索引：读取协议 + 命中条件表
|           |-- principles/       # 专业约束簇分卷正文
|           `-- memory/           # 项目核心记忆簇分卷：文件名与 principles/ 簇卷一致
|-- docs/product-studio/<product-id>/
|-- .codex-plugin/plugin.json
|-- .claude-plugin/
`-- .agents/plugins/marketplace.json
```

## 安装

Antigravity (AGY)：

```powershell
# 工作区安装（仅当前项目生效）：
git clone https://github.com/foreturn/product-studio.git .agents/plugins/product-studio

# 全局安装（所有工作区生效）：
git clone https://github.com/foreturn/product-studio.git ~/.gemini/antigravity/plugins/product-studio
```

Codex：

```powershell
codex plugin marketplace add foreturn/product-studio
codex plugin add product-studio@foreturn
```

Claude Code：

```powershell
claude plugin marketplace add foreturn/product-studio
claude plugin install product-studio@foreturn
```

安装后，在新会话中描述任务即可由编码代理按需要选择专业技能；相关能力与项目记忆按任务加载。

## 校验

```bash
claude plugin validate --strict .
claude plugin validate --strict .claude-plugin/plugin.json
```

各技能还可使用 `skill-creator` 提供的 `quick_validate.py` 检查元数据。这些工具检查技能元数据和插件清单；提示说明的完整性、专业归属与实际效果需要通过任务评审和安装后的新会话验证。

## 许可

本项目依据 [MIT License](LICENSE) 授权。
