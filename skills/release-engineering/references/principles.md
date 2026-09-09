# 发布工程专业约束

## 能力索引

正文位于本索引同级的 `principles/` 目录，下表链接相对于本索引文件。按任务的实际变化、风险与依赖选择能力簇，完整读取命中分卷；命中存疑时加读相关相邻簇，发现新边界时补读，无关簇不加载。设计或执行发布验证、评审健康观察与发布结果时，加读“发布验证与观察”卷。

| 能力簇 | 命中条件 | 正文 |
|---|---|---|
| 版本范围与对象身份 | 确定发布范围与对象身份、组织源代码提交边界、打版本 Tag、声明版本与兼容语义、保持修订版本说明及状态可追溯 | [version-scope.md](principles/version-scope.md) |
| 制品与来源证明 | 构建不可变制品、控制全部输入、跨环境晋级同一候选，并绑定组件清单、签名与来源证明 | [artifacts-provenance.md](principles/artifacts-provenance.md) |
| 流水线与环境 | 编排流水线阶段与技术门禁、评审脚本职责与复用边界、治理缓存重试，核验目标环境身份配置依赖并管控秘密注入 | [pipeline-environments.md](principles/pipeline-environments.md) |
| 迁移与兼容窗口 | 规划服务客户端数据与消息的混合版本窗口，实施可暂停恢复的数据迁移、回填校验及前滚恢复 | [migration-compatibility.md](principles/migration-compatibility.md) |
| 切流与恢复 | 规划渐进发布与部署切流、保护容量与下游依赖，执行停止回滚、前滚与完整恢复 | [rollout-recovery.md](principles/rollout-recovery.md) |
| 授权、隔离与审计 | 为提交推送标记上传部署迁移切流恢复等写动作核对当前授权、对象环境、隔离防重与审计边界 | [authorization-audit.md](principles/authorization-audit.md) |
| 分发、热修复与发布沟通 | 分发制品到区域与渠道、编排热修复与主线回归、准备消费者与值守材料、撰写发布说明与公告；分发渠道、热修复、发布沟通、可用范围 | [distribution-communication.md](principles/distribution-communication.md) |
| 发布验证与观察 | 验证目标环境部署身份与用户结果、观察健康信号与业务成功、确定观察窗口与门禁阈值；健康观察、候选与基线区分、观察窗口 | [verification.md](principles/verification.md) |
