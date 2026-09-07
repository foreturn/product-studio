# Android 工程专业约束

## 能力索引

专业约束正文按簇分卷存放于 `references/principles/`，每簇汇聚数个专业类别的跨框架与跨设备形态的不变量。先依命中条件判定本次任务命中的簇（通常一至三簇），再完整读取命中簇文件；命中存疑时宁可加读相邻簇，不因漏判而缺约束；与本次工作无关的簇不读取。实施类任务完成实现进入验证时，加读“测试与可观测性”卷。

| 能力簇 | 命中条件 | 正文 |
|---|---|---|
| 应用结构、生命周期与构建治理 | 新建功能模块或重构工程结构、调整状态分层与数据流边界、处理配置变化与进程重建后的恢复、引入或升级依赖、调整构建变体与产物配置、升级 targetSdk 或适配新系统行为与设备形态 | [structure-delivery.md](references/principles/structure-delivery.md) |
| 导航、数据与离线同步 | 实现页面导航、系统返回、深链跳转与跨页面参数传递；接入网络请求、分页、实时推送、缓存与自动重试；实现本地数据库、文件存储、数据迁移与离线同步 | [navigation-data.md](references/principles/navigation-data.md) |
| 组件、布局与视觉体系 | 新建或重构 Compose 与 View 组件、调整页面容器与滚动结构、适配分屏折叠与大屏窗口、使用设计令牌与深浅色主题、调整字号间距图标与视觉层级、机型与屏幕密度适配 | [components-visual.md](references/principles/components-visual.md) |
| 表单、交互反馈与可达性 | 实现表单输入与提交、列表与批量操作、加载空错状态与操作反馈、动效与触觉反馈；多语言与双向布局、字体放大、高对比度与屏幕阅读器适配 | [interaction-a11y.md](references/principles/interaction-a11y.md) |
| 平台能力、安全与性能 | 实现后台任务与调度、通知推送、权限请求与授权恢复、跨应用分享与外部文件访问、凭据密钥存储与网络安全；排查启动耗时、掉帧卡顿、内存泄漏与功耗发热 | [runtime-security.md](references/principles/runtime-security.md) |
| 测试与可观测性 | 制定测试策略、编写或评审测试、真机与模拟器验证、崩溃与性能监控、遥测脱敏 | [verification.md](references/principles/verification.md) |
