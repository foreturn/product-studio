---
schema: 2
memory: verification
scope: current-project
project_root: ""
updated_at: ""
---

# verification

<!-- 首建说明：本模板仅用于首次创建 schema 2 记忆。先读 `../skills/verification/references/verification-principles.md` 角色能力手册；一个独立语义一张卡，同家族编号从 `001` 递增，只生成有证据的事实。实例化时删除本说明、事实家族索引与占位内容，只保留实际事实卡；既有 schema 1 或 schema 2 记忆不得读取或套用本模板。示例标题：`VER-AC-001 — 注册失败提示满足已确认验收标准`。 -->

## 事实家族

- `VER-BASE-*`：核验对象、制品与环境基线
- `VER-AC-*`：验收标准及其证据结果
- `VER-JOURNEY-*`：端到端关键旅程结果
- `VER-REC-*`：失败注入与恢复结果
- `VER-NFR-*`：回归与非功能核验结果
- `VER-DEFECT-*`：已证实缺陷与证据限制
- `VER-CONCLUSION-*`：当前验收结论

## 现行事实

### VER-<FAMILY>-001 — <可独立理解的事实标题>

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
