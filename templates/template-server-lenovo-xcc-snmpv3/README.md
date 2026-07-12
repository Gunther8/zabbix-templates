# Template Server Lenovo XCC SNMPv3

Lenovo 服务器 XCC（XClarity Controller）SNMPv3 监控模板。

- **采集方式**：SNMP Agent + SNMP Trap
- **适用对象**：搭载 Lenovo XCC 管理模块的服务器
- **需要在 Host 层面设置的宏**：
  - `{$SNMP_AUTH_PASS}` / `{$SNMP_PRIV_PASS}` — SNMPv3 认证/加密密码（默认占位符 `CHANGE_ME_AT_HOST_LEVEL`，务必修改）
  - `{$SNMP_SECNAME_CONTEXT}` — SNMPv3 安全用户名（默认 `USERID`，Lenovo/IBM 常见默认账号）
  - `{$TEMP_WARN}` / `{$TEMP_CRIT}` — 温度告警/严重阈值（默认 65℃ / 75℃）
  - `{$TEMP_WARN:"Ambient"}` / `{$TEMP_CRIT:"Ambient"}` — 环境温度专用阈值（默认 35℃ / 40℃）
  - `{$TEMP_CRIT_LOW}` — 低温严重阈值（默认 5℃）
  - `{$FAN_OK_STATUS}` / `{$PSU_OK_STATUS}` / `{$DISK_OK_STATUS}` — 正常状态字符串（默认 `Normal`）
  - `{$HEALTH_DISASTER_STATUS}` / `{$HEALTH_CRIT_STATUS}` / `{$HEALTH_WARN_STATUS}` — 健康状态码分级
- **覆盖内容**：
  - 系统电源状态、开机时长、重启次数、系统健康状态、系统状态
  - 当前总功耗
  - SNMP Trap 接收（General）
  - LLD 自动发现：风扇、物理硬盘、电源、温度（含 Ambient/CPU 专项）、电压 共 7 类

## 使用方式

1. 在 XCC 上开启 SNMPv3，创建认证用户
2. Zabbix 后台导入本目录下的 yaml 文件
3. Host 层面配置 SNMPv3 认证信息，务必修改默认占位密码

---
基于 Zabbix 6.0 实测通过，由 AI（Claude）协助编写。
