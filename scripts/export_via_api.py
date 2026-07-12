#!/usr/bin/env python3
"""
Export Zabbix templates directly via the Zabbix API, one file per
template, named after the template — avoids the "every export is
named zbx_export_templates" problem entirely.

Config via environment variables:
    ZABBIX_URL    e.g. https://zabbix.example.com/api_jsonrpc.php
    ZABBIX_TOKEN  API token (Zabbix 5.4+, generate under
                  Users -> API tokens). Preferred.
  or, if no token support:
    ZABBIX_USER
    ZABBIX_PASS

Usage:
    python export_via_api.py                # export all templates
    python export_via_api.py "NTP*" "Synology*"   # filter by name glob(s)
    python export_via_api.py --custom-only   # skip Zabbix's own built-in templates
    python export_via_api.py --list          # just list templates + built-in/custom, no export

"--custom-only" relies on the "vendor_name" field (Zabbix 6.2+): official
templates shipped by Zabbix have it set (e.g. "Zabbix"), self-made ones
don't. On older Zabbix versions this field doesn't exist and every
template will look "custom" — in that case tell them apart by group name
instead (built-in ones live under groups like "Templates/Operating
systems", "Templates/Network devices", etc; put your own templates in a
different group, e.g. "Templates/NTP").
"""
import argparse
import fnmatch
import json
import os
import re
import urllib.request
from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
EXPORT_FORMAT = "yaml"  # or "xml"


def rpc(url, method, params, auth=None, request_id=1):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": request_id,
    }
    headers = {"Content-Type": "application/json-rpc"}
    if auth:
        payload["auth"] = auth
        headers["Authorization"] = f"Bearer {auth}"

    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"), headers=headers
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    if "error" in result:
        raise SystemExit(f"Zabbix API error: {result['error']}")
    return result["result"]


def sanitize(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[^\w\-]+", "-", name)
    return re.sub(r"-+", "-", name).strip("-")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("patterns", nargs="*", help="glob(s) to filter template/host name")
    parser.add_argument(
        "--custom-only", action="store_true",
        help="skip templates with a vendor_name set (i.e. Zabbix's own built-in templates)",
    )
    parser.add_argument(
        "--list", action="store_true",
        help="just print templates with built-in/custom status, don't export anything",
    )
    args = parser.parse_args()

    url = os.environ.get("ZABBIX_URL")
    if not url:
        raise SystemExit("Set ZABBIX_URL, e.g. https://zabbix.example.com/api_jsonrpc.php")

    token = os.environ.get("ZABBIX_TOKEN")
    auth = token
    if not auth:
        user = os.environ.get("ZABBIX_USER")
        password = os.environ.get("ZABBIX_PASS")
        if not (user and password):
            raise SystemExit(
                "Set ZABBIX_TOKEN, or ZABBIX_USER + ZABBIX_PASS"
            )
        auth = rpc(url, "user.login", {"username": user, "password": password})

    templates = rpc(
        url,
        "template.get",
        {
            "output": ["templateid", "name", "host", "vendor_name", "vendor_version"],
            "selectGroups": ["name"],
        },
        auth,
    )

    if args.patterns:
        templates = [
            t for t in templates
            if any(fnmatch.fnmatch(t["name"], p) or fnmatch.fnmatch(t["host"], p) for p in args.patterns)
        ]

    if args.custom_only:
        templates = [t for t in templates if not t.get("vendor_name")]

    if not templates:
        raise SystemExit("No matching templates found")

    if args.list:
        for t in templates:
            groups = ", ".join(g["name"] for g in t.get("groups", []))
            origin = f"built-in ({t['vendor_name']} {t.get('vendor_version', '')})".strip() if t.get("vendor_name") else "custom"
            print(f"{t['name']}  [{origin}]  groups: {groups}")
        return

    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

    for tpl in templates:
        exported = rpc(
            url,
            "configuration.export",
            {
                "options": {"templates": [tpl["templateid"]]},
                "format": EXPORT_FORMAT,
            },
            auth,
        )
        dest = TEMPLATES_DIR / f"{sanitize(tpl['name'])}.{EXPORT_FORMAT}"
        dest.write_text(exported, encoding="utf-8")
        print(f"wrote {dest}")

    if not token:
        rpc(url, "user.logout", {}, auth)


if __name__ == "__main__":
    main()
