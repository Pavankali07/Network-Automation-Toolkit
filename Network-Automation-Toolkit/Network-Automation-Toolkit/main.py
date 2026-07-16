import argparse
import json

from network_toolkit.automation import NetworkAutomation


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Network Automation Toolkit"
    )
    parser.add_argument(
        "command",
        choices=[
            "inventory",
            "backup",
            "compliance",
            "bgp",
            "ospf",
            "interfaces",
            "all",
        ],
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    toolkit = NetworkAutomation()

    actions = {
        "inventory": toolkit.inventory,
        "backup": toolkit.backup,
        "compliance": toolkit.compliance,
        "bgp": toolkit.bgp,
        "ospf": toolkit.ospf,
        "interfaces": toolkit.interfaces,
        "all": toolkit.run_all,
    }

    result = actions[args.command]()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
