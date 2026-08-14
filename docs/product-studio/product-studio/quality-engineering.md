# quality-engineering 当前产品事实

## 插件结构契约校验

- **当前事实**：仓库的 `validate-project.mjs` 机械核对恰好十一项 Skill、三类文件各自的精确章节、principles 的八至十六个专业大类及每类四至八条通用约束、memory 的五至九类终态事实、八字段与八项共同入册门禁、SKILL 的命中读取及权威复核契约、Owner locator、OpenAI 界面元数据、已移除路径、README 与双端清单拓扑；Hook 校验还逐事件要求命令处理器经兼容插件根调用 `terminal-hook.mjs`。任一不一致以非零退出。
- **权威依据**：`scripts/validate-project.mjs`；`README.md#三层文件契约`；`.codex-plugin/plugin.json`
- **影响边界**：该入口证明源树结构和声明一致，不证明专业内容在真实任务中被正确触发、判断或执行，也不证明任一客户端已安装当前快照。
- **复核入口**：运行 `node scripts/validate-project.mjs` 并检查退出码；技能集合、统一格式、入册门禁、manifest、Hook 或 locator 规则变化时先更新失败测试，再更新实现。

## 终态 Hook 行为回归

- **当前事实**：`terminal-hook.test.mjs` 在隔离临时 Git 仓库与真实多进程 Hook 子进程回放中覆盖四类事件、无首提交分支、Pre/Post 配对、观测验证与伪造拒绝、验证后实现漂移、验证后仅 Owner 事实册写入、非法事实路径、协议命令非证据、真实外层 `record`、`DEFERRED` 验证要求、只读放行、有限续写、显式 CLI 坐标、顺序与重叠会话、活动工具、隐藏索引位、逐册 Owner 绑定、`NO_CHANGE`、`SYNCED`、凭据与回执删除、UTF-8 大小、已脏子模块、同尺寸大文件流式指纹、有界清理和非 Git 降级。
- **权威依据**：`tests/terminal-hook.test.mjs`；`tests/fixtures/terminal-envelope.json`；`scripts/terminal-hook.mjs`
- **影响边界**：该套件证明 Node 脚本在本地 Git、模拟客户端信封与并发子进程下的状态机，不证明 Codex 或 Claude Code 已安装并信任 Hook、客户端实际事件字段永不变化，也不证明浏览器、设备、服务或生产环境成立。
- **复核入口**：运行 `node --test tests/terminal-hook.test.mjs`，读取全部子测试与退出码；Hook 事件、状态、指纹、回执 Schema、安全门禁或重试策略变化时重审。

## 单项 Skill 结构入口

- **当前事实**：每项 Skill 可使用当前 `skill-creator` 的 `quick_validate.py` 独立检查 frontmatter、命名与基本结构，项目契约校验再补充本插件的统一章节、principles 通用约束清单、memory 类型数量、共同门禁与八字段、SKILL 的事实读取契约和跨文件拓扑约束；两类静态检查互不替代。
- **权威依据**：`skills/product-management/SKILL.md`；`skills/release-engineering/SKILL.md`；`scripts/validate-project.mjs#validateSkill`
- **影响边界**：十一项 Skill 的源文件结构受此入口保护；详细专业正确性、自动发现、边界服从和实际行为仍需压力场景与真实任务证据。
- **复核入口**：枚举 `skills/` 后对每个实际目录运行 `quick_validate.py`，再运行项目校验并分别记录失败；skill-creator 规则或本插件结构契约变化时重审。
