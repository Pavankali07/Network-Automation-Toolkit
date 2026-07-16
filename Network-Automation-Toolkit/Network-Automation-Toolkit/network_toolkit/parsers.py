import re


def parse_version(output: str) -> dict:
    hostname_match = re.search(r"(?m)^(\S+) uptime is", output)
    version_match = re.search(r"Version\s+([^\s,]+)", output)
    model_match = re.search(r"(?m)^cisco\s+(\S+)", output)
    serial_match = re.search(r"Processor board ID\s+(\S+)", output)
    uptime_match = re.search(r"(?m)^\S+ uptime is (.+)$", output)

    return {
        "hostname": hostname_match.group(1) if hostname_match else "unknown",
        "os_version": version_match.group(1) if version_match else "unknown",
        "model": model_match.group(1) if model_match else "unknown",
        "serial_number": serial_match.group(1) if serial_match else "unknown",
        "uptime": uptime_match.group(1) if uptime_match else "unknown",
    }


def parse_bgp_summary(output: str) -> list[dict]:
    neighbors = []
    for line in output.splitlines():
        if not re.match(r"^\d+\.\d+\.\d+\.\d+\s+", line):
            continue

        parts = line.split()
        state_value = parts[-1]
        established = state_value.isdigit()

        neighbors.append({
            "neighbor": parts[0],
            "remote_as": parts[2],
            "state": "Established" if established else state_value,
            "prefixes_received": int(state_value) if established else 0,
            "healthy": established,
        })
    return neighbors


def parse_ospf_neighbors(output: str) -> list[dict]:
    neighbors = []
    for line in output.splitlines():
        if not re.match(r"^\d+\.\d+\.\d+\.\d+\s+", line):
            continue

        parts = line.split()
        neighbors.append({
            "neighbor_id": parts[0],
            "state": parts[2],
            "address": parts[4],
            "interface": parts[5],
            "healthy": parts[2].startswith("FULL"),
        })
    return neighbors


def parse_interfaces(output: str) -> list[dict]:
    interfaces = []
    for line in output.splitlines():
        if not line or line.startswith("Interface"):
            continue

        match = re.match(
            r"^(\S+)\s+(\S+)\s+\S+\s+\S+\s+(.+?)\s{2,}(\S+)$",
            line
        )
        if not match:
            continue

        interfaces.append({
            "interface": match.group(1),
            "ip_address": match.group(2),
            "status": match.group(3).strip(),
            "protocol": match.group(4),
        })
    return interfaces
