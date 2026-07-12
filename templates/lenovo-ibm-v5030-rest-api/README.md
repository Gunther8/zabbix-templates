# Lenovo IBM V5030 REST API

通过 Script Item 调用 V5030（IBM Spectrum Virtualize）REST API 采集存储状态，无需 SNMP。

- **采集方式**：Script Item（调用 REST API） + Dependent Item 解析
- **适用对象**：Lenovo/IBM V5030 存储（Spectrum Virtualize 系列）
- **需要在 Host 层面设置的宏**：
  - `{$V5030.URL}` — 例如 `https://192.0.2.10:7443`
  - `{$V5030.USER}` — REST API 用户名（建议使用 Monitor 权限只读账号）
  - `{$V5030.PASSWORD}` — REST API 密码（`SECRET_TEXT` 类型，需在 Host 层面填写，模板本身不含默认值）
  - `{$V5030.CAPACITY.WARN}` / `{$V5030.CAPACITY.CRIT}` — 容量使用率告警/严重阈值（默认 80% / 90%）
- **覆盖内容**：
  - 系统名称、固件/code level、总容量/剩余容量/容量使用率
  - 节点（Node）、硬盘（Drive）、机箱（Enclosure）、MDisk 离线/异常计数
  - LLD 自动发现：Nodes、Drives、Pools、MDisks 共 4 类

## 使用方式

1. 在 V5030 上创建一个 Monitor 权限的只读账号用于 REST API 调用
2. Zabbix 后台导入本目录下的 yaml 文件
3. Host 层面配置 `{$V5030.URL}` / `{$V5030.USER}` / `{$V5030.PASSWORD}`

---
基于 Zabbix 6.0 实测通过，由 AI（Claude）协助编写。
