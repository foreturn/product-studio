# quality-engineering 当前产品事实

## 插件结构契约校验

- **当前事实**：仓库的 `validate-project.mjs` 机械核对恰好十一项 Skill、三类文件各自的精确章节、principles 的八至十六个专业大类及每类四至八条通用约束、memory 仅含“核心记忆”且具有五至九个主题及每题一至三条“记住……”普通列表、SKILL 内 Git 根与安全单级 `product-id` 唯一解析、Owner locator、工作前读取、当前权威优先、事实准入、旧认知维护、安全与写权限边界、OpenAI 界面元数据、已移除运行资产与公共协议、README 和双端清单拓扑；任一不一致以非零退出。
- **权威依据**：`scripts/validate-project.mjs`；`README.md#三层文件契约`；`.codex-plugin/plugin.json`
- **影响边界**：该入口证明源树结构、提示契约和声明一致，不证明专业内容在真实任务中被正确触发、判断或执行，也不证明任一客户端已安装当前快照或代理一定完成事实写入与后续读取。
- **复核入口**：运行 `node scripts/validate-project.mjs` 并检查退出码；技能集合、统一格式、memory 主题、manifest、项目记忆提示或 locator 规则变化时先更新机械断言，再更新实现。

## 单项 Skill 结构入口

- **当前事实**：每项 Skill 可使用当前 `skill-creator` 的 `quick_validate.py` 独立检查 frontmatter、命名与基本结构，项目契约校验再补充本插件的统一章节、principles 通用约束清单、memory 的单一“核心记忆”章、主题数量与“记住……”普通列表、SKILL 的项目记忆定位读取准入维护指令、Owner locator 和跨文件拓扑约束；两类静态检查互不替代。
- **权威依据**：`skills/product-management/SKILL.md`；`skills/release-engineering/SKILL.md`；`scripts/validate-project.mjs#validateSkill`
- **影响边界**：十一项 Skill 的源文件结构受此入口保护；详细专业正确性、自动发现、边界服从和实际行为仍需压力场景与真实任务证据。
- **复核入口**：枚举 `skills/` 后对每个实际目录运行 `quick_validate.py`，再运行项目校验并分别记录失败；skill-creator 规则或本插件结构契约变化时重审。
