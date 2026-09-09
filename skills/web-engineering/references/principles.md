# Web 工程专业约束

## 能力索引

专业约束正文按簇分卷存放于 `references/principles/`，每簇汇聚一至数个专业类别的跨框架不变量。先依命中条件判定本次任务命中的簇（通常一至四簇），再完整读取命中簇文件；命中存疑时宁可加读相邻簇，不因漏判而缺约束；与本次工作无关的簇不读取。实施类任务完成实现进入验证时，加读“测试与可观测性”卷。

| 能力簇 | 命中条件 | 正文 |
|---|---|---|
| 应用结构、构建与交付治理 | 新建页面或模块、调整应用壳与渲染方式（服务端渲染、预渲染、水合一致性）、引入或升级依赖、调整构建拆包与环境配置、制定浏览器兼容策略；SEO 收录、页面元数据、站点地图、重定向与状态码、分享预览 | [structure-delivery.md](references/principles/structure-delivery.md) |
| 路由、导航与任务连续性 | 设计或调整 URL 结构、路由层级、站内导航、浏览器历史、外部深链、页面标题与返回上下文，处理未知资源、无权访问、失效链接和未提交任务的离开重入 | [routing-navigation.md](references/principles/routing-navigation.md) |
| 状态、数据与离线同步 | 划分远端事实、查询副本、表单草稿、局部交互与跨页面状态；接入数据请求、缓存、轮询、重试、乐观更新、实时推送、本地存储、跨标签页协同与离线队列 | [state-data-sync.md](references/principles/state-data-sync.md) |
| 组件与视觉体系 | 新建或重构组件、调整组件接口与复用边界、使用设计令牌、CSS 架构与主题切换（深浅色、暗色模式）、调整布局栅格与响应式表现、视觉层级、颜色与尺寸 | [components-visual.md](references/principles/components-visual.md) |
| 表单、交互反馈与可达性 | 实现表单、表格列表与批量操作，处理异步加载与错误呈现、操作反馈与动效、浮层与焦点管理；键盘触控、屏幕阅读器、页面缩放与字体放大、多语言与双向文本 | [interaction-a11y.md](references/principles/interaction-a11y.md) |
| 运行时安全与错误恢复 | 渲染不可信内容、iframe 与第三方脚本嵌入、跨窗口通信，处理认证态、敏感数据留存、错误分类、故障隔离与结果未知后的恢复 | [runtime-security.md](references/principles/runtime-security.md) |
| 性能与资源生命周期 | 测量与优化加载、交互、布局、绘制和内存表现，治理代码拆分、预取、虚拟呈现、监听、计时、连接、媒体与临时资源的生命周期 | [performance-resources.md](references/principles/performance-resources.md) |
| 测试与可观测性 | 制定测试策略、编写或评审测试、真实浏览器验证、前端错误监控与遥测脱敏 | [verification.md](references/principles/verification.md) |
