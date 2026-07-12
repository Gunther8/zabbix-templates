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
"""
import fnmatch
import json
import os
import re
import sys
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

    patterns = sys.argv[1:] or None

    templates = rpc(url, "template.get", {"output": ["templateid", "name", "host"]}, auth)
    if patterns:
        templates = [
            t for t in templates
            if any(fnmatch.fnmatch(t["name"], p) or fnmatch.fnmatch(t["host"], p) for p in patterns)
        ]

    if not templates:
        raise SystemExit("No matching templates found")

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
