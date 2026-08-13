# security-engineering 当前产品事实

## 安全工程裁决边界

- **当前事实**：`security-engineering` 唯一裁定资产与数据分类、威胁模型、身份认证与会话、授权和租户政策、输入与 API 滥用控制、秘密与密码学、隐私、供应链、安全基线与观测、漏洞风险和处置标准；架构拥有信任边界拓扑，工程技能落实代码，质量工程证明控制有效，发布工程执行生产动作。
- **权威依据**：`skills/security-engineering/SKILL.md#唯一决策权`；`skills/security-engineering/references/principles.md#能力索引`
- **影响边界**：安全可以阻止不满足政策或证据门槛的交付，但不独占所有实现代码或生产操作；前端隐藏、网络位置、扫描器标签和合规清单均不能替代资源级授权、当前威胁路径与影响证据。
- **复核入口**：以跨租户访问、会话撤销、SSRF、秘密轮换、隐私删除、依赖漏洞和高价值操作场景检查安全政策、实现 Owner、质量证据、发布授权与风险接受边界。

## 安全事实入口

- **当前事实**：当前已执行且会复用的资产分类、身份会话、授权租户、输入控制、秘密加密边界、隐私处置、供应链基线、安全观测和稳定漏洞修复事实进入 `docs/product-studio/<product-id>/security-engineering.md`；`security-engineering` 裁决语义，`fact-sync` 在质量通过后机械落盘。
- **权威依据**：`skills/security-engineering/SKILL.md#终态事实候选`；`skills/security-engineering/references/memory.md#共同定位与写入契约`
- **影响边界**：可利用攻击步骤、真实秘密、令牌、个人数据、生产样本、漏洞时间线、一次性扫描结果和未接受候选控制不得入册；同一事实正文不复制到架构、实现或质量册。
- **复核入口**：核对 Owner 裁决包使用脱敏直接证据并含唯一 locator、四栏或删除依据，以质量失败、策略变化、控制删除、证据入口搬移和零变化场景检查门禁与最小写入。
