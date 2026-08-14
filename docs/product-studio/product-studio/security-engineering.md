# security-engineering 当前产品事实

## 终态回执敏感信息门禁

- **当前事实**：终态回执在解析前按 UTF-8 字节限制为 64 KiB，解析后递归检查字段名与字符串值，拒绝密码、令牌、API 或云访问密钥、客户端秘密、私钥、认证头、Cookie、JWT、带凭据连接串、常见供应商 token 前缀及原始 `diff --git`；无论记录成功或拒绝，预期回执文件均立即删除，孤儿回执在一日后清理。
- **权威依据**：`scripts/terminal-hook.mjs#readJsonLimited`；`scripts/terminal-hook.mjs#assertSafeEnvelope`；`scripts/terminal-hook.mjs#handleRecord`；`references/terminal-protocol.md#安全边界`
- **影响边界**：机械模式只提供常见泄露的最后防线，不能证明任意文本均已匿名化，也无法阻止秘密在调用 `record` 前被其他工具写入；它不替代最小化收集、秘密管理和人工审查。事实规则仍禁止秘密、用户数据、生产授权、原始生产载荷和任务历史进入回执或事实册。
- **复核入口**：运行凭据拒绝与文件删除测试，并覆盖未知敏感字段、AWS 或代码托管 key、JWT、带凭据 URL、私钥、Bearer、嵌套原始 diff、多字节超限 JSON、孤儿清理和正常脱敏回执；敏感模式、保留策略或回执 Schema 变化时重审。

## 事实册最小披露边界

- **当前事实**：十一位 Owner 的 memory 契约只允许同时满足当前终态、稳定、非显然、影响后续判断、重查成本高、唯一 Owner、可复核与安全留存的专业语义，并统一禁止秘密、令牌、用户数据、生产授权、原始载荷、任务历史和原始 diff；源码或配置摘要、迁移进度、单次版本、摘要、指标、时点、部署快照和可生成清单不得冒充当前事实。
- **权威依据**：`skills/security-engineering/references/memory.md`；`skills/release-engineering/references/memory.md`；`scripts/validate-project.mjs#validateSkill`
- **影响边界**：该边界约束所有目标仓库的 Product Studio 事实册和终态回执；它不自动净化权威源码、配置或环境系统中的敏感内容。
- **复核入口**：枚举十一份 memory 的通用入册门禁、全册安全规则与事实写法，执行项目校验、秘密模式扫描并检查回执负例；新增 Owner、事实字段、入册门禁或运行事实类型时重审。
