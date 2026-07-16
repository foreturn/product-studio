# 平台兼容说明

## 共享内核

以下内容应在 Codex 与 Claude Code 之间保持通用：

- `skills/<skill-name>/SKILL.md`
- 相对路径引用与产物模板
- 与平台无关的 Node.js 或 Python 脚本
- 产品产物与验收标准
- 角色输入输出、阶段门禁、发布授权与反馈回流规则

共享 Skill 的 frontmatter 只使用两端均支持的 `name` 与 `description`，除非其他字段已经在两端验证。

## 平台适配层

以下内容分别维护：

- `.codex-plugin/plugin.json`
- `.claude-plugin/plugin.json`
- Skill 内的 `agents/openai.yaml` UI 元数据
- Marketplace 清单与安装命令
- Hooks 与生命周期事件配置
- MCP 封装配置
- 子代理定义与权限策略

共享 Skill 不写死工具名称，只描述需要完成的操作，由当前代理选择可用的读取、编辑、Shell、浏览器或测试能力。
