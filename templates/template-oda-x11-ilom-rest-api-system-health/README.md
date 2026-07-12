# Template ODA X11 iLOM REST API - System Health

Oracle ODA X11 iLOM 系统健康监控模板，通过 Oracle 私有的 ILOM Web Service REST API
（`/rest/v1/`，**不是** DMTF Redfish）采集 System/CPU/Memory/Power/Storage/Networking 健康状态。

- **采集方式**：HTTP Agent（ILOM REST API） + Dependent Item 解析
- **适用对象**：Oracle ODA X11 HA 节点（验证型号 ORACLE SERVER E6-2L，ILOM 5.1.4.23）
- **认证方式**：HTTP Basic，建议使用专门创建的只读 ILOM 用户
- **姊妹模板**：`Template ODA X11 iLOM REST API - Cooling`（风扇 + 进/排风温度），建议关联到同一 Host
- **对标**：覆盖范围与现有 `oda_check.py` ILOM-CLI 巡检脚本一致
  （System/CPU/Memory/Power/Storage/Networking/Open_Problems/SP），
  区别是本模板是持续轮询 + 触发告警，而不是每日一次的 HTML 报告
- **需要在 Host 层面设置的宏**：
  - `{$ILOM_IP}` — ILOM 地址（示例值，需按实际环境修改）
  - `{$ILOM_USER}` — 只读监控用户（默认 `monitor`）
  - `{$ILOM_PASSWORD}` — 密码（默认占位符 `change_me`，务必在 Host 层面修改）
- **最有价值的单项**：`ilom.openproblems.count` —— 与 ILOM Web UI 的 "Open Problems" 及
  `oda_check.py` 的 `cmd_open_problems` 同源，属于 ILOM 自身的聚合故障检测结果
- **覆盖内容**：CPU/DIMM/磁盘/网卡/电源健康状态（含逐个 index）、内存/存储/网络/电源子系统汇总、
  SP（Service Processor）描述与主机名、系统固件版本、Open Problems 计数，共 45 个监控项、22 个触发器

## 使用方式

1. 在 ODA X11 ILOM 上创建一个只读监控用户
2. Zabbix 后台导入本目录下的 yaml 文件
3. Host 层面配置 `{$ILOM_IP}` / `{$ILOM_USER}` / `{$ILOM_PASSWORD}`
4. 建议同时导入并关联 "Cooling" 姊妹模板

---
基于 Zabbix 6.0 实测通过，由 AI（Claude）协助编写，2026-07-08 验证数据源正确性。
