from datetime import datetime, timezone
from difflib import unified_diff
from pathlib import Path
import json
import re
import yaml
from jinja2 import Environment, FileSystemLoader

from .drivers import get_driver
from .parsers import parse_version, parse_bgp, parse_ospf, parse_interfaces

BASE = Path(__file__).resolve().parent.parent

class NetworkService:
    def __init__(self):
        inventory = yaml.safe_load((BASE / "inventory/devices.yaml").read_text())
        self.mock_mode = inventory["settings"]["mock_mode"]
        self.devices = inventory["devices"]
        self.rules = yaml.safe_load((BASE / "compliance/rules.yaml").read_text())["rules"]
        self.backups = BASE / "backups"
        self.reports = BASE / "reports"
        self.backups.mkdir(exist_ok=True)
        self.reports.mkdir(exist_ok=True)
        self.jinja = Environment(loader=FileSystemLoader(BASE / "templates"))

    def driver(self, device):
        return get_driver(device, self.mock_mode)

    def save(self, name, data):
        (self.reports / name).write_text(json.dumps(data, indent=2), encoding="utf-8")

    def inventory(self):
        result = []
        for device in self.devices:
            facts = parse_version(self.driver(device).command("show version"))
            result.append({**device, **facts})
        self.save("inventory.json", result)
        return result

    def backup(self):
        result = []
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        for device in self.devices:
            config = self.driver(device).command("show running-config")
            path = self.backups / f"{device['name']}_{stamp}.cfg"
            latest = self.backups / f"{device['name']}_latest.cfg"
            path.write_text(config + "\n", encoding="utf-8")
            latest.write_text(config + "\n", encoding="utf-8")
            result.append({"device": device["name"], "status": "success", "file": path.name})
        self.save("backup_report.json", result)
        return result

    def compliance(self):
        result = []
        for device in self.devices:
            config = self.driver(device).command("show running-config")
            checks = []
            for rule in self.rules:
                passed = bool(re.search(rule["pattern"], config, re.MULTILINE))
                checks.append({**rule, "status": "PASS" if passed else "FAIL"})
            passed = sum(c["status"] == "PASS" for c in checks)
            result.append({
                "device": device["name"],
                "passed": passed,
                "total": len(checks),
                "compliant": passed == len(checks),
                "checks": checks,
            })
        self.save("compliance_report.json", result)
        return result

    def interfaces(self):
        result = [{"device": d["name"], "interfaces": parse_interfaces(
            self.driver(d).command("show ip interface brief"))} for d in self.devices]
        self.save("interface_report.json", result)
        return result

    def bgp(self):
        result = [{"device": d["name"], "neighbors": parse_bgp(
            self.driver(d).command("show ip bgp summary"))} for d in self.devices]
        self.save("bgp_report.json", result)
        return result

    def ospf(self):
        result = [{"device": d["name"], "neighbors": parse_ospf(
            self.driver(d).command("show ip ospf neighbor"))} for d in self.devices]
        self.save("ospf_report.json", result)
        return result

    def vlan(self, vlan_id, vlan_name, device_names):
        if not 1 <= vlan_id <= 4094:
            raise ValueError("VLAN ID must be between 1 and 4094")
        text = self.jinja.get_template("vlan.j2").render(
            vlan_id=vlan_id, vlan_name=vlan_name)
        commands = [line.strip() for line in text.splitlines() if line.strip()]
        result = []
        for device in self.devices:
            if device["name"] not in device_names:
                continue
            if "switch" not in device["role"]:
                result.append({"device": device["name"], "status": "skipped"})
                continue
            output = self.driver(device).configure(commands)
            result.append({"device": device["name"], "status": "success", "output": output})
        self.save("vlan_report.json", result)
        return result

    def drift(self):
        result = []
        for device in self.devices:
            latest = self.backups / f"{device['name']}_latest.cfg"
            current = self.driver(device).command("show running-config")
            if not latest.exists():
                result.append({"device": device["name"], "status": "no_baseline", "diff": []})
                continue
            previous = latest.read_text(encoding="utf-8")
            diff = list(unified_diff(previous.splitlines(), current.splitlines(), lineterm=""))
            result.append({
                "device": device["name"],
                "status": "drift_detected" if diff else "no_change",
                "diff": diff,
            })
        self.save("drift_report.json", result)
        return result

    def all(self):
        return {
            "inventory": self.inventory(),
            "backup": self.backup(),
            "compliance": self.compliance(),
            "interfaces": self.interfaces(),
            "bgp": self.bgp(),
            "ospf": self.ospf(),
            "drift": self.drift(),
        }
