# Web 工程专业约束

## 能力索引

专业约束正文按簇分卷存放于 `references/principles/`，每簇汇聚数个专业类别的跨框架不变量。先依命中条件判定本次任务命中的簇（通常一至三簇），再完整读取命中簇文件；命中存疑时宁可加读相邻簇，不因漏判而缺约束；与本次工作无关的簇不读取。实施类任务完成实现进入验证时，加读“测试与可观测性”卷。

| 能力簇 | 命中条件 | 正文 |
|---|---|---|
| 应用结构、构建与交付治理 | 新建页面或模块、调整应用壳与渲染方式（服务端渲染、预渲染、水合一致性）、引入或升级依赖、调整构建拆包与环境配置、制定浏览器兼容策略；SEO 收录、页面元数据、站点地图、重定向与状态码、分享预览 | [structure-delivery.md](references/principles/structure-delivery.md) |
| 路由、状态与数据 | 实现 URL 结构、路由导航、浏览器历史、深链与跨页面状态；接入数据请求、缓存、轮询、重试、乐观更新、实时推送、本地存储与离线队列 | [routing-data.md](references/principles/routing-data.md) |
| 组件与视觉体系 | 新建或重构组件、调整组件接口与复用边界、使用设计令牌、CSS 架构与主题切换（深浅色、暗色模式）、调整布局栅格与响应式表现、视觉层级、颜色与尺寸 | [components-visual.md](references/principles/components-visual.md) |
| 表单、交互反馈与可达性 | 实现表单、表格列表与批量操作，处理异步加载与错误呈现、操作反馈与动效、浮层与焦点管理；键盘触控、屏幕阅读器、页面缩放与字体放大、多语言与双向文本 | [interaction-a11y.md](references/principles/interaction-a11y.md) |
| 运行时、安全与性能 | 渲染不可信内容、iframe 与第三方脚本嵌入、跨窗口通信、认证态与敏感数据留存；错误分类与恢复、性能测量与优化、监听计时等资源释放 | [runtime-security.md](references/principles/runtime-security.md) |
| 测试与可观测性 | 制定测试策略、编写或评审测试、真实浏览器验证、前端错误监控与遥测脱敏 | [verification.md](references/principles/verification.md) |
