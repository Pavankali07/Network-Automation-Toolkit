# Enterprise Network Automation Platform

A GitHub-ready portfolio project that automates common Cisco network engineering tasks.

## Features

- Device inventory collection
- Configuration backups
- Security compliance audits
- BGP and OSPF neighbor validation
- Interface status monitoring
- VLAN deployment using Jinja2
- Configuration drift detection
- Flask web dashboard
- Mock mode and live Netmiko mode
- JSON reports, Docker, tests, and GitHub Actions

## Run

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

```bash
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## CLI

```bash
python main.py inventory
python main.py backup
python main.py compliance
python main.py interfaces
python main.py bgp
python main.py ospf
python main.py drift
python main.py vlan --vlan-id 120 --vlan-name DATA --devices SW1 SW2
python main.py all
```

Mock mode is enabled in `inventory/devices.yaml`, so the project runs without network equipment.

For live Cisco devices, set `mock_mode: false` and use environment variables:

```bash
NET_USERNAME
NET_PASSWORD
NET_SECRET
```

## Resume Entry

**Enterprise Network Automation Platform | Python, Flask, Netmiko, Jinja2, Cisco IOS**

- Developed a Python platform that automates Cisco inventory collection, configuration backups, compliance auditing, VLAN deployment, routing validation, and configuration drift detection.
- Automated BGP and OSPF health checks and generated structured JSON operational reports.
- Built a Flask dashboard, mock-device lab, unit tests, Docker packaging, and GitHub Actions CI.

## License

MIT
