from datetime import datetime, timezone
from pathlib import Path
import json
import re
import yaml

from .mock_devices import run_mock_command
from .parsers import (
    parse_bgp_summary,
    parse_interfaces,
    parse_ospf_neighbors,
    parse_version,
)


BASE_DIR = Path(__file__).resolve().parent.parent
INVENTORY_FILE = BASE_DIR / "inventory" / "devices.yaml"
BACKUP_DIR = BASE_DIR / "backups"
REPORT_DIR = BASE_DIR / "reports"

COMPLIANCE_RULES = [
    {"name": "SSH Version 2", "pattern": r"(?m)^ip ssh version 2$"},
    {"name": "AAA Enabled", "pattern": r"(?m)^aaa new-model$"},
    {"name": "Password Encryption", "pattern": r"(?m)^service password-encryption$"},
    {"name": "NTP Configured", "pattern": r"(?m)^ntp server "},
    {"name": "Syslog Configured", "pattern": r"(?m)^logging host "},
    {"name": "SNMP Configured", "pattern": r"(?m)^snmp-server "},
]


class NetworkAutomation:
    def __init__(self) -> None:
        self.devices = self._load_devices()
        BACKUP_DIR.mkdir(exist_ok=True)
        REPORT_DIR.mkdir(exist_ok=True)

    @staticmethod
    def _load_devices() -> list[dict]:
        with INVENTORY_FILE.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        return data["devices"]

    @staticmethod
    def _timestamp() -> str:
        return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    @staticmethod
    def _save_json(filename: str, data) -> None:
        path = REPORT_DIR / filename
        with path.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)

    def inventory(self) -> list[dict]:
        results = []
        for device in self.devices:
            parsed = parse_version(
                run_mock_command(device["name"], "show version")
            )
            results.append({**device, **parsed})

        self._save_json("inventory.json", results)
        return results

    def backup(self) -> list[dict]:
        results = []
        for device in self.devices:
            config = run_mock_command(
                device["name"], "show running-config"
            )
            filename = f"{device['name']}_{self._timestamp()}.cfg"
            path = BACKUP_DIR / filename
            path.write_text(config + "\n", encoding="utf-8")
            results.append({
                "device": device["name"],
                "status": "success",
                "file": str(path.relative_to(BASE_DIR)),
            })

        self._save_json("backup_report.json", results)
        return results

    def compliance(self) -> list[dict]:
        results = []
        for device in self.devices:
            config = run_mock_command(
                device["name"], "show running-config"
            )
            checks = []
            for rule in COMPLIANCE_RULES:
                passed = bool(re.search(rule["pattern"], config))
                checks.append({
                    "rule": rule["name"],
                    "status": "PASS" if passed else "FAIL",
                })

            passed_count = sum(
                check["status"] == "PASS" for check in checks
            )
            results.append({
                "device": device["name"],
                "passed": passed_count,
                "total": len(checks),
                "compliant": passed_count == len(checks),
                "checks": checks,
            })

        self._save_json("compliance_report.json", results)
        return results

    def bgp(self) -> list[dict]:
        results = []
        for device in self.devices:
            output = run_mock_command(
                device["name"], "show ip bgp summary"
            )
            results.append({
                "device": device["name"],
                "neighbors": parse_bgp_summary(output),
            })

        self._save_json("bgp_report.json", results)
        return results

    def ospf(self) -> list[dict]:
        results = []
        for device in self.devices:
            output = run_mock_command(
                device["name"], "show ip ospf neighbor"
            )
            results.append({
                "device": device["name"],
                "neighbors": parse_ospf_neighbors(output),
            })

        self._save_json("ospf_report.json", results)
        return results

    def interfaces(self) -> list[dict]:
        results = []
        for device in self.devices:
            output = run_mock_command(
                device["name"], "show ip interface brief"
            )
            results.append({
                "device": device["name"],
                "interfaces": parse_interfaces(output),
            })

        self._save_json("interface_report.json", results)
        return results

    def run_all(self) -> dict:
        return {
            "inventory": self.inventory(),
            "backup": self.backup(),
            "compliance": self.compliance(),
            "bgp": self.bgp(),
            "ospf": self.ospf(),
            "interfaces": self.interfaces(),
        }
