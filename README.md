# Zabbix Templates

个人整理 / 编写的 Zabbix 监控模板集合。

## 目录结构

```
templates/   存放模板文件（.xml / .yaml），一个模板一个文件
scripts/     辅助脚本
```

## 关于导出命名问题

Zabbix 后台导出模板时，文件名默认都是 `zbx_export_templates.xml`（或 `.yaml`），
多个模板导出后文件名会互相覆盖。有两种解决方式：

### 方式一：API 直接导出（推荐）

`scripts/export_via_api.py` 通过 Zabbix API 按模板逐个导出，直接用模板名命名文件，
不需要再手动拆分。

```bash
export ZABBIX_URL="https://your-zabbix/api_jsonrpc.php"
export ZABBIX_TOKEN="xxxx"        # Users -> API tokens 里生成（Zabbix 5.4+）
# 或者没有 token 支持的话：
# export ZABBIX_USER="Admin"
# export ZABBIX_PASS="xxxx"

python scripts/export_via_api.py              # 导出全部模板
python scripts/export_via_api.py "NTP*"       # 按名称过滤（支持通配符），可传多个
python scripts/export_via_api.py --custom-only         # 只导出自建模板，跳过Zabbix内置模板
python scripts/export_via_api.py --list                # 只列出模板+来源(内置/自建)，不导出
```

`--custom-only` 判断依据是 API 返回的 `vendor_name` 字段（Zabbix 6.2+）：
官方内置模板会带 vendor 信息（如 "Zabbix"），自己写的模板这个字段为空。
如果你的Zabbix版本较老没有这个字段，所有模板都会被当成"自建"，这种情况下
建议用模板组区分——内置模板默认在 `Templates/Operating systems`、
`Templates/Network devices` 等官方组下，自己新建模板时选一个不同的组名
（比如 `Templates/NTP`）就能靠组名区分开。

### 方式二：网页手动导出后拆分

用 `scripts/split_export.py` 把一次导出的文件（哪怕里面包含多个模板）按模板名拆分成
独立文件，自动放进 `templates/` 目录。

```bash
python scripts/split_export.py /path/to/zbx_export_templates.yaml
```

支持 `.yaml`/`.yml`（需要 `pyyaml`）和 `.xml`（标准库自带，无需额外依赖）。
