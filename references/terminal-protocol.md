# 终态事实协议

本协议只约束一次可写工作如何收束。专业技能的选择、组合与先后由 AI 根据请求、仓库证据和风险自行决定；Hook 不参与路由，也不从差异推导 Owner、事实正文或事实动作。它是终态 guardrail，不是不可绕过的执行沙箱。

## 适用时点

当一次实现、验收、配置或发布工作已形成可交付终态，并取得与风险相称的当前验证后，执行一次事实同步检查。只读工作且没有观测到本轮变更时，Hook 自动放行。专门维护事实册时可先运行 `begin`，明确要求本轮留下回执。

`UserPromptSubmit` 注入的上下文会给出当前会话完整的 `status` 命令。普通工具 Shell 不保证继承 Hook 的插件数据环境，必须使用该命令中的 `--data-dir` 与 `--session`，不得省略或猜测。

```bash
node "<plugin-root>/scripts/terminal-hook.mjs" begin --data-dir "<plugin-data>" --session "<session-id>" --json
```

## 专业检查

Skill 中的 `references/memory.md` 是专业记忆规则，不是任务运行时的事实存储；真正的当前事实只写入目标仓库 `docs/product-studio/<product-id>/<owner>.md`。仅检查本轮实际触及并核验的专业边界。对每个受影响 Owner，先读取该 Skill 的 `references/memory.md` 中所有权、事实类型索引、通用入册门禁、动作语义与全册安全规则，再完整读取本轮命中的事实类型规则和事实册既有主题；未命中的专业细目不得机械加载。既有事实只作语义导航，必须沿其权威入口复核当前实现，然后作出以下一种事实动作：

- `ADD`：候选通过该 Owner 的全部入册门禁，且稳定主题首次成立。
- `UPDATE`：候选通过全部入册门禁，且同一主题的当前语义、权威依据、影响边界或复核入口发生实质改变。
- `DELETE`：主题或最后消费者已由当前权威证据证明消失。
- `NO_CHANGE`：已检查，但事实没有新增、改变或消失；对应事实册必须保持字节不变。

源码、Schema、流水线、制品库与环境查询始终是权威来源。事实册只是语义索引，不得凭旧记忆跳过当前复核。未通过当前终态、稳定性、非显然性、决策价值、重查成本、唯一 Owner、可复核性或安全边界任一门禁的内容，只留在本轮报告，不得包装为事实动作。单轮回执只对列出的核验范围负责，不得宣称全项目新鲜。

## 终态结果

- `SYNCED`：至少一个 Owner 执行了 `ADD`、`UPDATE` 或 `DELETE`，对应事实册已经修改。
- `NO_CHANGE`：所有已检查 Owner 均为 `NO_CHANGE`，所有事实册字节不变。
- `DEFERRED`：实现可能完成，但事实归属、证据、写权限或当前性不足，写明原因。归属尚不可知时 `checkedOwners` 可以为空；若同一事实册被并发会话触及，也只能作 `DEFERRED` 或 `BLOCKED`。
- `BLOCKED`：交付物尚未形成可验证终态，事实册保持不变并写明阻塞原因。

`DEFERRED` 与 `BLOCKED` 是终态协议结果，不是事实动作。它们不得伪装成历史条目写进事实册，也不能为 Hook 未观测、账本断链或 Pre/Post 输入不一致的变更提供放行回执。

## 回执格式

先查询当前状态与最终仓库指纹：

```bash
node "<plugin-root>/scripts/terminal-hook.mjs" status --data-dir "<plugin-data>" --session "<session-id>" --json
```

在仓库之外或 Hook 返回的 `envelopePath` 写入 JSON：

```json
{
  "schemaVersion": 2,
  "repositoryRoot": "<status.repositoryRoot>",
  "sessionId": "<status.sessionId>",
  "turnKey": "<status.turnKey>",
  "finalFingerprint": "<status.currentFingerprint>",
  "validationEvidence": [
    {
      "kind": "test",
      "toolUseId": "<status.validationEvidenceCandidates[n].toolUseId>",
      "inputDigest": "<status.validationEvidenceCandidates[n].inputDigest>",
      "commandHash": "<status.validationEvidenceCandidates[n].commandHash>",
      "expectedExitCodes": [0],
      "scope": "<该证据真正覆盖的行为与边界>"
    }
  ],
  "checkedOwners": [
    {
      "productId": "<已确认的单级产品目录名>",
      "owner": "<十一位 Owner 之一>",
      "factBookPath": "docs/product-studio/<productId>/<owner>.md",
      "checkedScope": ["<本轮实际复核范围>"],
      "actions": [
        {
          "action": "NO_CHANGE",
          "topic": "<稳定主题键或明确候选主题>",
          "authoritativeEvidence": ["<仓库相对入口或安全的环境查询标识>"]
        }
      ]
    }
  ],
  "result": "NO_CHANGE"
}
```

`validationEvidence` 只能逐项引用 `status.validationEvidenceCandidates`，不得填写命令正文或自报退出码。候选只来自本会话、本 turn 内成对且输入摘要一致的 `Bash`、`exec_command` 或 `shell_command` Post 事件；Hook 必须解析出退出状态，并确认验证发生在最后一次实现变更之后、其前后实现指纹均与最终实现指纹一致，且没有并发或冲突工具。实现指纹只排除合法 `docs/product-studio/<product-id>/<owner>.md` 事实册，因而允许在实现验证后写入事实；未知 Owner、非法路径或其他文档变更仍会使旧验证失效。`status`、`begin` 与 `record` 协议控制命令从不成为验证候选；唯一活动工具是当前会话与 turn 的非并发 `record` 外层调用时，回执可在该调用内闭合。`apply_patch`、`Edit` 等编辑工具只用于解释仓库变化，绝不构成验证证据。Post 出现本身不代表成功，无法解析、超时、取消与自由文本工具响应都不构成验证证据。

`expectedExitCodes` 只声明可接受语义，实际退出码始终取自执行账本。`test`、`build`、`lint` 等普通验证只接受 `[0]`；预期不存在等非零语义必须使用 `kind: "probe"` 并显式列出退出码。`DEFERRED` 与 `BLOCKED` 都必须含非空 `reason`；`DEFERRED` 表示实现已可验证而事实尚不能安全收束，因此仍须引用至少一项观测验证；`BLOCKED` 表示交付物未形成可验证终态，可不提供验证。`SYNCED` 必须至少含一个 `ADD`、`UPDATE` 或 `DELETE`，且实际归属于本会话的每一本变化事实册都与 `productId + owner + factBookPath` 精确对应。`NO_CHANGE` 必须至少含一个显式 `NO_CHANGE`，且不得保留归属于本会话的事实册变化。

记录回执：

```bash
node "<plugin-root>/scripts/terminal-hook.mjs" record --data-dir "<plugin-data>" --session "<session-id>" --envelope "<status.envelopePath>" --json
```

每个会话与 turn 都有独立的 `envelopePath`。新 `turn_id` 总是建立新基线，不继承旧 turn 的续写状态。回执绑定 Git 根、会话、turn、最终完整仓库指纹、当前会话的变更边、验证工具 ID、输入摘要、命令哈希和已检查 Owner；记录之后又出现变更边或完整指纹改变，回执立即陈旧，必须重新检查事实并重新记录；若实现指纹未变，仍在候选中的实现验证可继续引用。

同一工作树的事件写入带序号的仓库级有界账本。当前会话只把本 `sessionId + turnKey` 的非并发边归给自己；其他会话的顺序边只能解释共享工作树为何漂移，不会自动成为当前会话的事实变化。重叠工具、同册多会话、事件断链或无 Pre 的 Post 都不会被静默重基线。

## 安全边界

事实册与回执均不得保存秘密、令牌、私钥、用户数据、生产授权、原始生产载荷、任务流水、计划、历史、原始 diff 或一次性日志。回执只保留验证引用和范围，不复制命令或输出。Hook 在读取 JSON 前先检查文件字节数，再递归检查字段和值，拒绝常见口令、API/访问密钥、Bearer/Basic、云厂商与代码托管令牌、私钥、JWT、带凭据 URL、原始 diff 以及超过 64 KiB 的回执。

无论记录成功还是拒绝，预期位置的回执文件都会删除；未记录的孤儿回执在 24 小时后清理。状态只保留最小结果并在七日后清理，仓库事件账本保留至多 1024 条边；裁剪越过活跃基线时会显式报告 `journalGap`，不会静默放行。

Stop 最多请求一次续写。若续写后仍无有效回执，Hook 报告协议失败并停止继续阻断，避免无限循环；这不是事实同步成功，也不得据此声称交付完成。

## Hook 能力边界

当前客户端文档保证 `PreToolUse`/`PostToolUse` 提供会话、turn、工具 ID、工具输入及 model-facing `tool_response`，但工具 Hook 只是 guardrail，部分专用执行路径、外部编辑器或未注册工具可能绕开。Hook 无法从 Bash 命令字符串可靠推导其全部副作用，也不能证明浏览器、设备、服务或生产环境的真实状态。

因此，账本只对实际收到的 Hook 事件负责。Hook 可验证回执声明、观测工具证据和事实册文件变化彼此一致，却不能从代码差异证明 AI 已选全所有受影响 Owner，也不能判定事实正文的专业语义正确，更不能仅凭 Shell 命令名称或退出零判定其验证范围是否充分；这些仍由 AI 依各专业契约负责。未观测的工作树变化会成为不可解释转换并拒绝回执；客户端完全绕过 Stop Hook 时，本协议本身不能形成强制边界。完整指纹会流式读取脏文件并覆盖 `assume-unchanged`、`skip-worktree` 与脏子模块，实现指纹只在此基础上排除合法 Owner 事实册；单次指纹设 120 秒安全上限，Hook 命令配置 180 秒超时，仍只是本地工作树证据，不等同于外部系统验收。
