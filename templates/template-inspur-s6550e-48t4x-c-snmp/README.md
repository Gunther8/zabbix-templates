# 浪潮 S6550E-48T4X-C 交换机 SNMP 模板

针对浪潮（IEIT/INOP）S6550E-48T4X-C 交换机的 SNMP 监控模板。

- **采集方式**：SNMP Agent + Calculated Item
- **适用对象**：浪潮 S6550E-48T4X-C 交换机（固定 2 风扇/2 电源/2 温度传感器的定制机型，非模块化机箱，故未对这些做 LLD 自动发现）
- **企业私有 OID 分支**：`.1.3.6.1.4.1.48797`（INOP 软件体系，非 H3C/锐捷体系，注意区分）
- **需要配置的宏**：`{$SNMP_COMMUNITY}`（默认 `public`）
- **覆盖内容**：
  - 标准接口流量（走 IF-MIB，自动发现）
  - CPU 利用率、内存总量/已用/空闲/使用率
  - 系统描述、软件版本、运行时间
  - 风扇转速 ×2、电源状态/告警位 ×2、CPU 周围温度、交换芯片温度
  - 已通过 CLI（`show environment` / `show power`）交叉验证私有 OID 正确性

## 使用方式

1. Zabbix 后台导入本目录下的 yaml 文件
2. Host 层面配置 SNMP 团体字
3. 关联模板到对应交换机 Host

---
基于 Zabbix 6.0 实测通过，由 AI（Claude）协助编写，创建于 2026年7月。
