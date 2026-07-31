# 校验脚本

`validate_project.py` 检查本插件的五技能契约，而非旧式角色流程：

- 可调用 Skill 必须恰为 `router`、`design`、`backend`、`frontend`、`verification`；旧 Skill 名、目录、调用或记忆文件不得残留。
- `router` 必须声明代码任务的最小调用链、并行条件、唯一合并者和失败隔离，并且只保留一次精确边界：`代码权限不等于生产操作授权，生产执行不在本插件范围。`
- `router` 加载恢复后的交付编排能力卷；`design` 按产品模式与系统模式分别加载产品设计、系统架构能力卷；其余三项开发验证 Skill 直接加载自己的专业能力准则。
- 六份能力准则必须与 `9efef58ddb3f3a4bebcf856f6c2eef7ca7a53194` 的对应原文哈希一致，并保持“目录—角色职责—核心能力—专业决策顺序—交付证据—常见误判”六章顺序、45 项核心能力的精确名称与最低正文深度。
- 代码事实模板只允许 `design`、`backend`、`frontend`、`verification` 四份 schema 3 文件；`router` 不得拥有记忆。
- 实例记忆只保存当前代码事实。语义键须属于对应技能且全局唯一，每条事实恰含当前实现、源码锚点、关联与消费者、验证证据、重验条件；模板说明、键目录、占位符、任务历史和空字段不得进入实例。
- Codex、Claude Code 与 marketplace 清单必须保持身份、版本、描述和来源一致。

在插件根目录运行：

```powershell
python -X utf8 scripts/validate_project.py
```

改动技能拓扑、能力准则、路由边界或记忆 schema 后，再运行负向自检：

```powershell
python -X utf8 scripts/validate_project.py --self-test
```

负向自检在临时副本中分别注入第六技能、router 记忆、缺失的设计能力卷、未声明的额外 reference、能力原文篡改、错误事实字段、重复事实键、畸形事实键、失去精确定位的源码锚点、错误模板骨架、旧调用名、把常规终端验证误算为跨领域，以及省略全栈 API 契约里程碑；13 类退化必须全部被拒绝，不改当前工作树。

该检查证明源码结构和提示词契约自洽。真实路由效果仍须用全新上下文做正向与负向试用。
