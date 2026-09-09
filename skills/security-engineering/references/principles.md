# 安全工程专业约束

## 能力索引

专业约束正文按簇分卷存放于 `references/principles/`，每簇汇聚一至数个专业类别的跨技术栈不变量。先依命中条件判定本次任务命中的簇（通常一至四簇），再完整读取命中簇文件；命中存疑时宁可加读相邻簇，不因漏判而缺约束；与本次工作无关的簇不读取。设计新系统或新入口时与完成实现进入安全验证时，加读“威胁建模与对抗验证”卷。

| 能力簇 | 命中条件 | 正文 |
|---|---|---|
| 威胁建模与对抗验证 | 为新系统或新入口建立威胁模型、梳理资产数据流与信任边界、评估剩余风险与控制生效性、在授权范围内确认漏洞并做对抗验证 | [threat-verification.md](references/principles/threat-verification.md) |
| 身份、会话与授权 | 设计或加固登录认证与联合身份、多因素与账户恢复、签发与校验会话令牌、实现对象级授权与租户隔离、清理权限变更后的缓存与会话 | [identity-access.md](references/principles/identity-access.md) |
| 解析、内容与滥用防护 | 处理外部输入与文件上传、防注入与跨站脚本、限制外联请求与解析资源、设计限流配额与幂等防重放、防护资源耗尽 | [input-abuse.md](references/principles/input-abuse.md) |
| 密码学与密钥管理 | 选择加密签名密码存储与随机令牌原语，设计密钥分层、秘密存储、轮换撤销销毁与泄露响应 | [crypto-key-management.md](references/principles/crypto-key-management.md) |
| 隐私与数据生命周期 | 划定隐私处理目的、接收者、地域与保留依据，实施数据最小化、访问导出更正与删除传播 | [privacy-data-lifecycle.md](references/principles/privacy-data-lifecycle.md) |
| 软件供应链 | 治理依赖与基础制品来源、隔离不受信构建、绑定组件清单签名来源证明，并按适用性处置漏洞 | [software-supply-chain.md](references/principles/software-supply-chain.md) |
| 运行环境加固 | 约束工作负载身份、系统权限、可写范围、宿主与网络访问，关闭生产调试入口并验证安全基线实态 | [runtime-hardening.md](references/principles/runtime-hardening.md) |
| 检测、审计与事件响应 | 建设安全日志与检测规则、设计审计记录与防篡改保留、校验检测链、指挥安全事件遏制取证与复盘 | [detection-response.md](references/principles/detection-response.md) |
