# Zabbix Templates

个人整理 / 编写的 Zabbix 监控模板集合。

## 目录结构

```
templates/   存放模板文件（.xml / .yaml），一个模板一个文件
scripts/     辅助脚本
```

## 关于导出命名问题

Zabbix 后台导出模板时，文件名默认都是 `zbx_export_templates.xml`（或 `.yaml`），
多个模板导出后文件名会互相覆盖。用 `scripts/split_export.py` 可以把一次导出的文件
（哪怕里面包含多个模板）按模板名拆分成独立文件，自动放进 `templates/` 目录。

```bash
python scripts/split_export.py /path/to/zbx_export_templates.yaml
```

支持 `.yaml`/`.yml`（需要 `pyyaml`）和 `.xml`（标准库自带，无需额外依赖）。
