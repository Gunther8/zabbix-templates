# H3C Server Basic Monitoring

H3C 服务器基础监控模板，通过 SNMP 采集。

- **采集方式**：SNMP Agent
- **适用对象**：H3C 服务器（挂载在 `Linux servers` 组）
- **需要配置的宏**：`{$SNMP_COMMUNITY}`（默认 `public`，建议按实际环境修改）
- **覆盖内容**：
  - 进风/出风温度（Inlet/Outlet Temperature）
  - 整机耗电（Power Total Cost）
  - BIOS 版本、HDM（远程管理模块）版本
  - LLD 自动发现：CPU、风扇、FRU、硬盘、健康状态、内存、电源、温度传感器共 8 类

## 使用方式

1. Zabbix 后台导入本目录下的 yaml 文件
2. 在 Host 层面按需覆盖 `{$SNMP_COMMUNITY}`
3. 关联模板到对应 Host

---
基于 Zabbix 6.0 实测通过，由 AI（Claude）协助编写。
