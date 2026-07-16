# 产品工作室

产品工作室是一套同时服务 Codex 与 Claude Code 的氛围编程插件。用户只需给出简短意图，插件便会先从仓库证据联想用户旅程、范围、约束与验收标准，再由职责清晰的产品研发角色推进实现，以减少过早编码、隐含假设和后期验收造成的返工。

扩写不是替用户虚构需求：仓库可查的信息自行查明，可逆细节记录假设后继续，只有会显著改变产品、安全、外部状态或不可逆数据的决策才请求确认。

## 工作流

端到端任务使用 `product-delivery`。它作为交付负责人，通过持久化产物协调各专项角色，不依赖对话历史独自传递决策：

```text
product-delivery
|-- product-discovery
|-- system-design（仅在存在重要架构决策时）
|-- frontend-experience
|-- backend-contract
|-- delivery-verification
`-- release-operations（发布适用且获授权时）
```

角色职责如下：

| Skill | 角色 | 主责 |
|---|---|---|
| `product-delivery` | 交付负责人 | 接入、路由、阶段门禁、变更控制与最终收口 |
| `product-discovery` | 产品经理 | 短提示词扩写、用户价值、范围、假设与验收标准 |
| `system-design` | 架构师 | 模块边界、跨域不变量、迁移回滚与关键权衡 |
| `frontend-experience` | 前端与体验负责人 | 用户可见流程、交互状态、实现与真实渲染证据 |
| `backend-contract` | 后端负责人 | API、数据、权限、一致性、兼容与恢复 |
| `delivery-verification` | 验收负责人 | 要求追溯、核心旅程、失败路径、回归与交付结论 |
| `release-operations` | 发布与运行负责人 | 发布授权、制品追溯、迁移回滚、上线验证与反馈回流 |

每个角色不只约定流程，还在 `SKILL.md` 中声明专业核心能力，并在自身 `references/` 中给出可直接指导设计、编码与验收的判断准则。前端能力覆盖易用性、交互简化、布局、色彩排版、可访问性和真实渲染；后端、架构、产品、验收与发布也各自拥有对应的领域能力模型。

产物按需写入目标仓库的 `docs/product/<product-slug>/`。没有下游消费者的文档不会为了形式完整而创建。

## 目录结构

```text
product-studio/
|-- .agents/plugins/marketplace.json
|-- .codex-plugin/plugin.json
|-- .claude-plugin/
|   |-- marketplace.json
|   `-- plugin.json
|-- skills/
|   |-- product-delivery/
|   |-- product-discovery/
|   |-- system-design/
|   |-- frontend-experience/
|   |-- backend-contract/
|   |-- delivery-verification/
|   `-- release-operations/
|-- templates/
|-- references/platform-compatibility.md
|-- scripts/validate_project.py
|-- docs/product/product-studio/
`-- assets/
```

## 安装

### Codex

从 GitHub 向 Codex 注册 marketplace，再安装其中的插件：

```powershell
codex plugin marketplace add foreturn/product-studio
codex plugin add product-studio@foreturn
```

第一条命令只注册 marketplace；第二条命令才会安装 `product-studio`。仓库更新后，可运行 `codex plugin marketplace upgrade foreturn` 刷新 marketplace，再按 Codex 提示升级插件。

### Claude Code

Claude Code 使用独立的 marketplace 清单与安装命令：

```powershell
claude plugin marketplace add foreturn/product-studio
claude plugin install product-studio@foreturn
```

## 校验

运行项目检查：

```powershell
python scripts/validate_project.py
```

Codex 插件使用内置 `plugin-creator` 校验器。Claude Code 同时严格校验插件与 marketplace 清单：

```powershell
claude plugin validate --strict C:\Users\root\plugins\product-studio
```
