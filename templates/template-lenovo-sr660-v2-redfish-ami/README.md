# Template Lenovo SR660 V2 Redfish AMI

Lenovo ThinkSystem SR660 V2（AMI 架构 XCC）Redfish 监控模板，纯 HTTP Agent 实现，无需在被监控主机上装 Agent。

- **采集方式**：HTTP Agent（Redfish API） + Dependent Item 解析
- **适用对象**：Lenovo ThinkSystem SR660 V2（BMC 为 AMI-based XCC）
- **验证环境**：BMC 固件 `6.a2.00` / RedfishVersion `1.8.0`
- **需要在 Host 层面设置的宏**：
  - `{$REDFISH.USER}` — BMC 登录用户名（默认 `USERID`，Lenovo/IBM 类 BMC 常见默认账号，建议按实际环境修改）
  - `{$REDFISH.PASSWORD}` — BMC 登录密码（`SECRET_TEXT` 类型）
  - `{$REDFISH.SCHEME}` — 默认 `https`
  - `{$FAN.MIN.RPM}` — 风扇最低转速阈值（默认 500）
  - `{$SSD.LEFTTIME.WARN}` — SSD 寿命剩余告警阈值（默认 10%）
- **覆盖内容**：
  - System / Chassis / BMC 健康汇总，含机箱开盖（Intrusion）感应
  - CPU、内存健康与总内存容量
  - 电源实时功耗
  - RAID 存储控制器健康
  - LLD 自动发现：物理硬盘、风扇、电源、温度传感器 共 4 类

## 使用方式

1. Zabbix 后台导入本目录下的 yaml 文件
2. Host 接口设置好可达 BMC 的地址（`{HOST.CONN}`）
3. Host 层面配置 `{$REDFISH.USER}` / `{$REDFISH.PASSWORD}`

---
基于 Zabbix 6.0 实测通过，由 AI（Claude）协助编写。
