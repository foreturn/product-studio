# 发布工程专业约束

## 能力索引

专业约束正文按簇分卷存放于 `references/principles/`，每簇汇聚一至数个专业类别的跨交付形态不变量。先依命中条件判定本次任务命中的簇（通常一至四簇），再完整读取命中簇文件；命中存疑时宁可加读相邻簇，不因漏判而缺约束；与本次工作无关的簇不读取。实施类任务完成部署进入发布验证与健康观察时，加读“发布验证与观察”卷。

| 能力簇 | 命中条件 | 正文 |
|---|---|---|
| 版本范围与对象身份 | 确定发布范围与对象身份、打版本 Tag、声明版本与兼容语义、保持修订版本说明及状态可追溯 | [version-scope.md](references/principles/version-scope.md) |
| 制品与来源证明 | 构建不可变制品、控制全部输入、跨环境晋级同一候选，并绑定组件清单、签名与来源证明 | [artifacts-provenance.md](references/principles/artifacts-provenance.md) |
| 流水线与环境 | 编排流水线阶段与技术门禁、治理缓存重试，核验目标环境身份配置依赖并管控秘密注入 | [pipeline-environments.md](references/principles/pipeline-environments.md) |
| 迁移与兼容窗口 | 规划服务客户端数据与消息的混合版本窗口，实施可暂停恢复的数据迁移、回填校验及前滚恢复 | [migration-compatibility.md](references/principles/migration-compatibility.md) |
| 切流与恢复 | 规划渐进发布与部署切流、保护容量与下游依赖，执行停止回滚、前滚与完整恢复 | [rollout-recovery.md](references/principles/rollout-recovery.md) |
| 授权、隔离与审计 | 为提交推送标记上传部署迁移切流恢复等写动作核对当前授权、对象环境、隔离防重与审计边界 | [authorization-audit.md](references/principles/authorization-audit.md) |
| 分发、热修复与发布沟通 | 分发制品到区域与渠道、编排热修复与主线回归、准备消费者与值守材料、撰写发布说明与公告；分发渠道、热修复、发布沟通、可用范围 | [distribution-communication.md](references/principles/distribution-communication.md) |
| 发布验证与观察 | 验证目标环境部署身份与用户结果、观察健康信号与业务成功、确定观察窗口与门禁阈值；健康观察、候选与基线区分、观察窗口 | [verification.md](references/principles/verification.md) |
