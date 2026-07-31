---
schema: 3
memory: frontend
scope: current-project-code
project_root: ""
updated_at: ""
---

# frontend 代码事实

<!-- 仅在项目首次产生值得跨会话保留的前端代码事实时复制本模板。实例化后填写项目根和带时区时间，删除本说明、事实键目录、示例与所有占位。同一语义键原位更新，新增代码事实时新增键，源码及消费者删除后删除键；Git 承担历史，既有事实文件不再次套用模板。 -->

## 事实键

- `frontend:page:<platform>:<route>`：页面入口、区域结构与主任务。
- `frontend:token:<theme>:<semantic-name>`：颜色、间距、字号、圆角等语义令牌的实际定义。
- `frontend:component:<platform>:<name>`：公共组件的变体、尺寸、状态与可访问契约。
- `frontend:layout:<platform>:<surface>`：真实容器、网格、对齐、滚动与层级关系。
- `frontend:state:<surface>:<operation>`：加载、空、错误、成功、禁用及恢复转换。
- `frontend:responsive:<surface>:<region>`：源码中的实际断点、重排、折叠与触控规则。

## 当前代码事实

### frontend:token:default:color-primary

- **当前实现**：<代码与真实渲染中已经成立的视觉、布局、交互或状态事实>
- **源码锚点**：<相对项目根的文件路径、组件、选择器、令牌或路由定位>
- **关联与消费者**：<引用它的页面、组件、状态、接口或相关事实键；无则写“无”>
- **验证证据**：<源码检查、交互测试、视口、主题、身份与渲染证据>
- **重验条件**：<哪些组件、令牌、样式、数据或断点变化后必须重新核验>
