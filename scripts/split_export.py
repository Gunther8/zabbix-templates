#!/usr/bin/env python3
"""
Split a Zabbix template export file (which Zabbix always names
zbx_export_templates.xml/.yaml, even for a single template) into one
file per template, named after the template, and drop them into
../templates/.

Usage:
    python split_export.py <exported_file.xml|.yaml>
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


def sanitize(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[^\w\-]+", "-", name)
    return re.sub(r"-+", "-", name).strip("-")


def split_yaml(path: Path):
    import yaml

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    root = data.get("zabbix_export", data)
    templates = root.get("templates") or []
    if not templates:
        raise SystemExit("No <templates> found in export file")

    for tpl in templates:
        name = tpl.get("template") or tpl.get("name")
        out = dict(data)
        out["zabbix_export"] = dict(root)
        out["zabbix_export"]["templates"] = [tpl]
        dest = TEMPLATES_DIR / f"{sanitize(name)}.yaml"
        with dest.open("w", encoding="utf-8") as f:
            yaml.safe_dump(out, f, allow_unicode=True, sort_keys=False)
        print(f"wrote {dest}")


def split_xml(path: Path):
    tree = ET.parse(path)
    root = tree.getroot()
    templates_el = root.find("templates")
    if templates_el is None:
        raise SystemExit("No <templates> element found in export file")

    for tpl in list(templates_el):
        name_el = tpl.find("template")
        name = name_el.text if name_el is not None else "template"

        new_root = ET.Element(root.tag, root.attrib)
        for child in root:
            if child.tag == "templates":
                continue
            new_root.append(child)
        new_templates = ET.SubElement(new_root, "templates")
        new_templates.append(tpl)

        dest = TEMPLATES_DIR / f"{sanitize(name)}.xml"
        ET.ElementTree(new_root).write(dest, encoding="utf-8", xml_declaration=True)
        print(f"wrote {dest}")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    src = Path(sys.argv[1])
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

    if src.suffix.lower() in (".yaml", ".yml"):
        split_yaml(src)
    elif src.suffix.lower() == ".xml":
        split_xml(src)
    else:
        raise SystemExit(f"Unsupported file type: {src.suffix}")


if __name__ == "__main__":
    main()
