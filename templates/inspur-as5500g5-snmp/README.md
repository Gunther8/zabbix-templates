# Inspur AS5500G5 by SNMP

浪潮 AS5500G5 存储的 SNMP 监控模板，基于浪潮 `INSPUR_EXT_MIB`（企业 OID `1.3.6.1.4.1.48512`）编写。

- **采集方式**：SNMP Agent + Calculated Item
- **适用对象**：浪潮 AS5500G5 存储控制柜
- **使用前提**：存储已开启 SNMP v1/v2c 或 v3（建议 v3 authPriv），Host 接口按需配置团体字/USM 用户
- **需要配置的宏**：
  - `{$STORAGE.PUSED.WARN}` / `{$STORAGE.PUSED.CRIT}` — 容量使用率告警/严重阈值（默认 80% / 90%）
  - `{$CANISTER.TEMP.WARN}` — 控制器插箱温度告警阈值（默认 55℃）
  - `{$CPU.UTIL.WARN}` — CPU 利用率告警阈值（默认 90%）
  - `{$BBU.CHARGE.WARN}` — 电池电量告警阈值（默认 50%）
  - `{$VDISK.LATENCY.WARN}` — 虚拟盘延迟告警阈值（默认 20ms）
- **覆盖内容**：
  - 集群名称/状态/软件版本
  - 物理存储与存储池容量（总量/已用/可用/使用率）
  - LLD 自动发现：机箱、控制器插箱（Canister）、电源、风扇、电池（BBU）、硬盘、FC口、iSCSI口、SAS口、系统性能，共 10 类

## 使用方式

1. Zabbix 后台导入本目录下的 yaml 文件
2. 在 Host 层面配置 SNMP 接口（v2c 团体字或 v3 USM）
3. 按需覆盖告警阈值宏

---
基于 Zabbix 6.0 实测通过，由 AI（Claude）协助编写，数据来源 MIB 为 `INSPUR_EXT_MIB_1.0.0.MIB`。
