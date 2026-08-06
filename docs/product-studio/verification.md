# verification 当前项目事实

## 验证与发布交接

- **当前事实**：`verification` 只验证代码、夹具与明确隔离的测试环境，并把通过验收的不可变制品、适用检查、阻塞和未覆盖风险交给 `release`；验收结论不构成生产授权，也不能外推为线上已执行或生产健康。
- **权威依据**：`skills/verification/SKILL.md#输出与裁决`；`skills/verification/SKILL.md#独立性与边界`；`skills/release/SKILL.md#输入门禁`
- **影响边界**：测试证据边界、验收制品交接、`release` 的就绪判定，以及生产操作前的独立授权门禁。
- **复核入口**：在全新上下文中提出“验收后直接生产部署”的请求，核对 `verification` 只交付当前制品与证据，`release` 另行核验目标环境和精确授权；该试用不能证明真实环境已执行或健康。

## 插件校验与行为证据

- **当前事实**：当前仓库以 `claude plugin validate --strict .` 检查 Claude Code 清单与目录格式；Codex 侧须通过 marketplace 实际安装和新线程中的技能发现验证分发。平台格式校验不证明真实路由选择、专业判断或目标项目行为，这些行为须在未提示技能名的全新上下文中作正反向试用。
- **权威依据**：`README.md#校验`；`.claude-plugin/marketplace.json#plugins[0].source`；`.agents/plugins/marketplace.json#plugins[0].source`
- **影响边界**：Claude Code 与 Codex 两套插件分发面、七个 Skill 的发现、路由触发、专业边界及后续验收结论；任一平台的静态通过不得外推为另一平台可安装或行为正确。
- **复核入口**：先运行 `claude plugin validate --strict .`；再分别执行 Codex marketplace 安装与新线程技能发现，并用未提示技能名的明确单项、跨专业、验收和发布请求作正反向试用，绑定当前版本、输入、输出和越权情况。
