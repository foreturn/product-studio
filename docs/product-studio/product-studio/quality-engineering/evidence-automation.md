# quality-engineering 当前产品事实 · 证据层级、隔离与自动化

## 单项 Skill 结构入口

- **当前事实**：每项 Skill 可使用当前 `skill-creator` 的 `quick_validate.py` 独立检查 frontmatter、命名与基本结构，项目契约校验再补充本插件的统一章节、principles 索引与簇卷对应契约、`references/memory/` 簇卷对应契约与“记住……”陈述、SKILL 的项目记忆定位读取准入维护指令、按簇 Owner 事实目录和跨文件拓扑约束；两类静态检查互不替代。
- **权威依据**：`skills/product-management/SKILL.md`；`skills/release-engineering/SKILL.md`；`scripts/validate-project.mjs#validateSkill`
- **影响边界**：十一项 Skill 的源文件结构受此入口保护；详细专业正确性、自动发现、边界服从和实际行为仍需压力场景与真实任务证据。
- **复核入口**：枚举 `skills/` 后对每个实际目录运行 `quick_validate.py`，再运行项目校验并分别记录失败；skill-creator 规则或本插件结构契约变化时重审。
