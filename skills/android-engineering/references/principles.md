# Android 工程专业约束

## 能力索引

正文位于本索引同级的 `principles/` 目录，下表链接相对于本索引文件。按任务的实际变化、风险与依赖选择能力簇，完整读取命中分卷；命中存疑时加读相关相邻簇，发现新边界时补读，无关簇不加载。设计或执行验证、评审检查结果与证据范围时，加读“测试与可观测性”卷。

| 能力簇 | 命中条件 | 正文 |
|---|---|---|
| 应用结构与交付单元 | 新建或整理功能模块、目录与命名，划分应用入口、模块职责、公共能力、依赖方向与交付单元，评审抽象复用和界面框架桥接 | [structure-delivery.md](principles/structure-delivery.md) |
| 生命周期与状态恢复 | 设计状态作用域与初始化，处理配置变化、窗口切换、后台回收与进程重建，核对恢复校验、资源注册释放和跨窗口共享 | [lifecycle-recovery.md](principles/lifecycle-recovery.md) |
| 导航与任务连续性 | 实现页面导航、系统返回、深链通知与跨页面参数传递，恢复列表上下文与未完成任务并区分失败去向 | [navigation-continuity.md](principles/navigation-continuity.md) |
| 状态、数据与离线同步 | 接入异步网络、分页实时推送、缓存与自动重试，实现本地数据库、文件存储、数据迁移与离线同步 | [state-data-sync.md](principles/state-data-sync.md) |
| 组件、布局与视觉体系 | 新建或重构 Compose 与 View 组件、调整页面容器与滚动结构、适配分屏折叠与大屏窗口、使用设计令牌与深浅色主题、调整字号间距图标与视觉层级、机型与屏幕密度适配 | [components-visual.md](principles/components-visual.md) |
| 表单、交互反馈与可达性 | 实现表单输入与提交、列表与批量操作、加载空错状态与操作反馈、动效与触觉反馈；多语言与双向布局、字体放大、高对比度与屏幕阅读器适配 | [interaction-a11y.md](principles/interaction-a11y.md) |
| 平台能力与安全 | 实现后台任务与调度、通知推送、权限请求与授权恢复、跨应用分享与外部文件访问、凭据密钥存储与网络安全 | [platform-security.md](principles/platform-security.md) |
| 性能与资源 | 排查启动耗时、掉帧卡顿、内存泄漏与功耗发热，治理主线程、媒体列表和系统资源生命周期 | [performance-resources.md](principles/performance-resources.md) |
| 系统兼容与构建治理 | 引入或升级工具链与依赖、调整构建变体和产物配置、升级 targetSdk、声明系统与设备支持范围，验证生产优化、安装和渠道兼容 | [build-compatibility.md](principles/build-compatibility.md) |
| 测试与可观测性 | 制定测试策略、编写或评审测试、真机与模拟器验证、崩溃与性能监控、遥测脱敏 | [verification.md](principles/verification.md) |
