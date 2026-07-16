import argparse
import json
from network_automation.services import NetworkService

parser = argparse.ArgumentParser()
sub = parser.add_subparsers(dest="command", required=True)
for name in ["inventory", "backup", "compliance", "interfaces", "bgp", "ospf", "drift", "all"]:
    sub.add_parser(name)
vlan = sub.add_parser("vlan")
vlan.add_argument("--vlan-id", type=int, required=True)
vlan.add_argument("--vlan-name", required=True)
vlan.add_argument("--devices", nargs="+", required=True)

args = parser.parse_args()
service = NetworkService()

actions = {
    "inventory": service.inventory,
    "backup": service.backup,
    "compliance": service.compliance,
    "interfaces": service.interfaces,
    "bgp": service.bgp,
    "ospf": service.ospf,
    "drift": service.drift,
    "all": service.all,
}

result = service.vlan(args.vlan_id, args.vlan_name, args.devices) if args.command == "vlan" else actions[args.command]()
print(json.dumps(result, indent=2))
