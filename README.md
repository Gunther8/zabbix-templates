# Zabbix Templates

个人整理 / 编写的 Zabbix 监控模板集合。所有模板均基于 **Zabbix 6.0** 实测通过，由 AI（Claude）协助编写。

每个模板独立一个文件夹，内含模板文件（.yaml）和对应说明（README.md）：

| 模板 | 说明 |
| --- | --- |
| [h3c-server-basic-monitoring](templates/h3c-server-basic-monitoring) | H3C 服务器基础监控（SNMP） |
| [inspur-as5500g5-snmp](templates/inspur-as5500g5-snmp) | 浪潮 AS5500G5 存储监控（SNMP） |
| [template-inspur-s6550e-48t4x-c-snmp](templates/template-inspur-s6550e-48t4x-c-snmp) | 浪潮 S6550E-48T4X-C 交换机监控（SNMP） |
| [lenovo-ibm-v5030-rest-api](templates/lenovo-ibm-v5030-rest-api) | Lenovo/IBM V5030 存储监控（REST API） |
| [template-lenovo-sr660-v2-redfish-ami](templates/template-lenovo-sr660-v2-redfish-ami) | Lenovo SR660 V2 服务器监控（Redfish） |
| [template-oda-x11-ilom-rest-api-system-health](templates/template-oda-x11-ilom-rest-api-system-health) | Oracle ODA X11 iLOM 系统健康监控（REST API） |
| [template-server-lenovo-xcc-snmpv3](templates/template-server-lenovo-xcc-snmpv3) | Lenovo XCC 服务器监控（SNMPv3） |

导入前请检查对应 README 里列出的宏，把默认占位值（IP/账号/密码）改成你自己环境的真实值。

