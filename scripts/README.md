# 校验脚本

`validate_project.py` 检查本插件的五技能契约，而非旧式角色流程：

- 可调用 Skill 必须恰为 `router`、`design`、`backend`、`frontend`、`verification`；旧 Skill 名、目录、调用或记忆文件不得残留。
- `router` 必须声明代码任务的最小调用链、并行条件、唯一合并者和失败隔离，并且只保留一次精确边界：`代码权限不等于生产操作授权，生产执行不在本插件范围。`
- `router` 加载裁剪后的交付编排能力卷；`design` 的产品模式依其 `SKILL.md` 契约执行，系统模式加载系统架构能力卷；其余三项开发验证 Skill 直接加载自己的专业能力准则。
- 五份能力准则必须与基于 `9efef58ddb3f3a4bebcf856f6c2eef7ca7a53194` 裁剪后的固定哈希一致，并保持“目录—角色职责—核心能力—常见误判”四章顺序、38 项核心能力的精确名称与最低正文深度。
- 根 `references/` 只允许共享的 `project-memory.md`，定义 schema 4 总结事实、Owner、稳定键与终态同步；四个专业 Skill 必须引用它，`router` 只协调同步而不拥有记忆。
- 代码事实模板只允许 `design`、`backend`、`frontend`、`verification` 四份 schema 4 文件。实例键统一为 `owner:type:slug` 且全局唯一，每条事实恰含事实摘要、代码定位、依赖与影响、验证入口、失效条件。
- 每次成功编码终态必须执行同步检查，但只有五字段变化才落盘；任务摘要、过程历史、单次通过、命令流水、模板说明、键目录、占位符和空字段不得进入实例。
- Codex、Claude Code 与 marketplace 清单必须保持身份、版本、描述和来源一致。

在插件根目录运行：

```bash
python3 -X utf8 scripts/validate_project.py
```

改动技能拓扑、能力准则、路由边界或记忆 schema 后，再运行负向自检：

```bash
python3 -X utf8 scripts/validate_project.py --self-test
```

负向自检在无任何实例事实册的合法临时副本中注入拓扑、reference、路由、schema、跨项目根、秘密值、围栏伪结构、游离正文、额外字段、共享契约掏空、同步方向反转与外部写入越权等退化；23 类退化必须各自命中对应诊断，不改当前工作树。

该检查证明当前快照的源码结构、定位、链接和提示词契约自洽，不能判断锚点仍存在但语义已经陈旧；该边界只能由编码终态对照最终差异完成同步。真实路由效果仍须用全新上下文做正向与负向试用。
