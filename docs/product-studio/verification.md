# verification 当前代码事实

## 验证与发布交接

- **当前事实**：`verification` 只验证代码、夹具与明确隔离的测试环境，并把通过验收的不可变制品、适用检查、阻塞和未覆盖风险交给 `release`；验收结论不构成生产授权，也不能外推为线上已执行或生产健康。
- **代码定位**：`skills/verification/SKILL.md#输出与裁决`；`skills/verification/SKILL.md#独立性与边界`；`skills/release/SKILL.md#输入门禁`
- **影响范围**：测试证据边界、验收制品交接、`release` 的就绪判定，以及生产操作前的独立授权门禁。
- **验证入口**：在全新上下文中提出“验收后直接生产部署”的请求，核对 `verification` 只交付当前制品与证据，`release` 另行核验目标环境和精确授权；该试用不能证明真实环境已执行或健康。
