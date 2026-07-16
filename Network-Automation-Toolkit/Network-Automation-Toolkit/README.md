# Network Automation Toolkit

A small portfolio project that demonstrates practical network automation using Python.

## Features

- Collect device inventory
- Back up running configurations
- Check configuration compliance
- Validate BGP neighbors
- Validate OSPF neighbors
- Monitor interface status
- Run without physical devices using mock data

## Technologies

Python, YAML, Cisco IOS concepts, BGP, OSPF, VLANs, SSH automation, GitHub Actions

## Project Structure

```text
Network-Automation-Toolkit/
├── main.py
├── requirements.txt
├── inventory/
│   └── devices.yaml
├── network_toolkit/
│   ├── __init__.py
│   ├── automation.py
│   ├── mock_devices.py
│   └── parsers.py
├── backups/
├── reports/
├── tests/
│   └── test_parsers.py
├── .github/
│   └── workflows/
│       └── python-ci.yml
├── .gitignore
└── LICENSE
```

## Installation

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Display device inventory:

```bash
python main.py inventory
```

Back up configurations:

```bash
python main.py backup
```

Run compliance checks:

```bash
python main.py compliance
```

Check BGP:

```bash
python main.py bgp
```

Check OSPF:

```bash
python main.py ospf
```

Check interfaces:

```bash
python main.py interfaces
```

Run all checks:

```bash
python main.py all
```

## Sample Compliance Checks

The project verifies whether devices have:

- SSH version 2
- AAA enabled
- Password encryption
- NTP server
- Syslog server
- SNMP configuration

## Resume Entry

**Network Automation Toolkit | Python, YAML, BGP, OSPF, Cisco IOS**

- Developed a Python-based network automation toolkit for device inventory, configuration backup, compliance auditing, and routing protocol health validation.
- Automated BGP, OSPF, and interface status checks across simulated Cisco routers and switches.
- Generated JSON reports and configuration backups to demonstrate repeatable operational network workflows.

## Live Device Extension

This project uses mock devices so recruiters can run it immediately. It can be extended with Netmiko by replacing the mock command function with SSH connections to Cisco IOS devices.

## License

MIT
