# iOS 工程专业约束

## 能力索引

正文位于本索引同级的 `principles/` 目录，下表链接相对于本索引文件。按任务的实际变化、风险与依赖选择能力簇，完整读取命中分卷；命中存疑时加读相关相邻簇，发现新边界时补读，无关簇不加载。设计或执行验证、评审检查结果与证据范围时，加读“测试与可观测性”卷。

| 能力簇 | 命中条件 | 正文 |
|---|---|---|
| 应用结构与交付单元 | 新建或整理功能模块、目录与命名，划分 App、Target、Extension、Package 的职责、公共能力与依赖方向，评审抽象复用和界面框架桥接 | [structure-delivery.md](principles/structure-delivery.md) |
| 生命周期与状态恢复 | 设计状态作用域与初始化，处理前后台、Scene 重建、多窗口、内存压力与系统终止，核对恢复校验、资源释放和跨场景共享 | [lifecycle-recovery.md](principles/lifecycle-recovery.md) |
| 导航与任务连续性 | 实现页面导航、层级返回、通用链接与通知入口跳转、跨场景参数传递，恢复集合上下文与未完成任务 | [navigation-continuity.md](principles/navigation-continuity.md) |
| 状态、数据与离线同步 | 接入状态并发、网络请求、分页实时推送、缓存与自动重试，实现本地持久化、迁移与离线同步 | [state-data-sync.md](principles/state-data-sync.md) |
| 组件、布局与视觉体系 | 新建或重构 SwiftUI 与 UIKit 组件、调整页面容器与滚动结构、适配 iPad 多窗口与分屏、使用设计令牌与深浅色外观、调整字号间距图标与视觉层级、设备与屏幕形态适配 | [components-visual.md](principles/components-visual.md) |
| 表单、交互反馈与可达性 | 实现表单输入与提交、列表与批量操作、加载空错状态与操作反馈、动效与触觉反馈；多语言与双向文本、动态字体、高对比度与屏幕阅读器适配 | [interaction-a11y.md](principles/interaction-a11y.md) |
| 平台能力与安全 | 实现后台任务与刷新、通知推送、权限请求与恢复、系统扩展与跨应用共享、凭据密钥存储与网络安全 | [platform-security.md](principles/platform-security.md) |
| 性能与资源 | 排查启动耗时、掉帧卡顿、内存泄漏与能耗发热，治理主执行域、媒体列表和系统资源生命周期 | [performance-resources.md](principles/performance-resources.md) |
| 系统兼容与构建治理 | 引入或升级工具链与依赖、调整构建配置与签名分发、声明系统和设备支持范围，验证生产优化、能力声明及渠道兼容 | [build-compatibility.md](principles/build-compatibility.md) |
| 测试与可观测性 | 制定测试策略、编写或评审测试、真机与模拟器验证、崩溃与性能监控、遥测脱敏 | [verification.md](principles/verification.md) |
