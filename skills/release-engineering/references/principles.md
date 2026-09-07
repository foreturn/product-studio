# 发布工程专业约束

## 能力索引

专业约束正文按簇分卷存放于 `references/principles/`，每簇汇聚数个专业类别的跨交付形态不变量。先依命中条件判定本次任务命中的簇（通常一至三簇），再完整读取命中簇文件；命中存疑时宁可加读相邻簇，不因漏判而缺约束；与本次工作无关的簇不读取。实施类任务完成部署进入发布验证与健康观察时，加读“发布验证与观察”卷。

| 能力簇 | 命中条件 | 正文 |
|---|---|---|
| 版本、制品与对象身份 | 确定发布范围与对象身份、打版本 Tag、声明版本与兼容语义、构建不可变制品、绑定来源与签名证明；发布范围、版本 Tag、对象身份、制品不可变、来源证明 | [version-artifacts.md](references/principles/version-artifacts.md) |
| 流水线、环境与迁移 | 编排流水线阶段与技术门禁、核验环境配置与依赖、管控秘密注入、规划数据迁移与混合版本窗口；流水线门禁、环境配置、缓存与重试、迁移与兼容窗口 | [pipeline-environments.md](references/principles/pipeline-environments.md) |
| 切流、恢复与授权审计 | 规划渐进发布与部署切流、保护容量与下游依赖、执行停止回滚与恢复、申请写动作授权、实施隔离与审计；部署切流、容量保护、停止恢复、授权隔离审计 | [rollout-recovery.md](references/principles/rollout-recovery.md) |
| 分发、热修复与发布沟通 | 分发制品到区域与渠道、编排热修复与主线回归、准备消费者与值守材料、撰写发布说明与公告；分发渠道、热修复、发布沟通、可用范围 | [distribution-communication.md](references/principles/distribution-communication.md) |
| 发布验证与观察 | 验证目标环境部署身份与用户结果、观察健康信号与业务成功、确定观察窗口与门禁阈值；健康观察、候选与基线区分、观察窗口 | [verification.md](references/principles/verification.md) |
