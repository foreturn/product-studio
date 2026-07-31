---
schema: 2
memory: backend
scope: current-project
project_root: ""
updated_at: ""
---

# backend

<!-- 首建说明：本模板仅用于首次创建 schema 2 记忆。先读 `../skills/backend/references/backend-design-principles.md` 角色能力手册；一个独立语义一张卡，同家族编号从 `001` 递增，只生成有证据的事实。实例化时删除本说明、事实家族索引与占位内容，只保留实际事实卡；既有 schema 1 或 schema 2 记忆不得读取或套用本模板。示例标题：`BE-API-001 — 创建订单接口返回持久化后的订单标识`。 -->

## 事实家族

- `BE-DOMAIN-*`：领域模型与业务不变量。
- `BE-SCHEMA-*`：权威数据 Schema 与持久化。
- `BE-API-*`：API 与错误契约。
- `BE-AUTH-*`：权限、安全与审计。
- `BE-CONSIST-*`：事务、一致性与失败恢复。
- `BE-INT-*`：外部服务与消息集成。
- `BE-OBS-*`：可观测性与运行信号。
- `BE-COMPAT-*`：兼容、迁移与调用方影响。
- `BE-LIMIT-*`：已证实的后端限制。

## 现行事实

### BE-<FAMILY>-001 — <可独立理解的事实标题>

- **事实类型**：<证据所支持的事实来源或性质>
- **已成立事实**：<主体、前提、行为、结果与边界>
- **角色专属细节**：<本角色判断所需且不重复事实句的细节>
- **适用范围**：<对象、版本、环境或边界>
- **精确定位**：<仓库位置、符号、契约、制品或环境>
- **成立证据**：<可复核的确认、实现、验证或运行证据>
- **核验基线**：<revision、制品、环境与核验时间>
- **关联事实**：<none 或相关稳定 ID>
- **下游约束**：<后续工作必须维持的事实边界>
- **状态**：<current / conditional / stale / superseded>
- **置信度**：<high / medium / low>
- **取代关系**：<none / supersedes ID / superseded-by ID>
- **失效条件**：<哪些变化会要求重新核验>
