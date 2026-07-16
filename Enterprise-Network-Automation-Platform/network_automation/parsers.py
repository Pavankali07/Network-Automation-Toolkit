import re

def find(pattern, text):
    match = re.search(pattern, text)
    return match.group(1).strip() if match else "unknown"

def parse_version(text):
    return {
        "hostname": find(r"(?m)^(\S+) uptime is", text),
        "os_version": find(r"Version\s+([^\s,]+)", text),
        "model": find(r"(?m)^cisco\s+(\S+)", text),
        "serial_number": find(r"Processor board ID\s+(\S+)", text),
        "uptime": find(r"(?m)^\S+ uptime is (.+)$", text),
    }

def parse_bgp(text):
    rows = []
    for line in text.splitlines():
        if not re.match(r"^\d+\.\d+\.\d+\.\d+\s+", line):
            continue
        parts = line.split()
        state = parts[-1]
        established = state.isdigit()
        rows.append({
            "neighbor": parts[0],
            "remote_as": parts[2],
            "state": "Established" if established else state,
            "prefixes_received": int(state) if established else 0,
            "healthy": established,
        })
    return rows

def parse_ospf(text):
    rows = []
    for line in text.splitlines():
        if not re.match(r"^\d+\.\d+\.\d+\.\d+\s+", line):
            continue
        parts = line.split()
        rows.append({
            "neighbor_id": parts[0],
            "state": parts[2],
            "address": parts[4],
            "interface": parts[5],
            "healthy": parts[2].startswith("FULL"),
        })
    return rows

def parse_interfaces(text):
    rows = []
    for line in text.splitlines()[1:]:
        parts = line.split()
        if len(parts) < 6:
            continue
        rows.append({
            "interface": parts[0],
            "ip_address": parts[1],
            "status": parts[-2],
            "protocol": parts[-1],
        })
    return rows
