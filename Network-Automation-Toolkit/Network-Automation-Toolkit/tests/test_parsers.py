from network_toolkit.parsers import (
    parse_bgp_summary,
    parse_interfaces,
    parse_ospf_neighbors,
    parse_version,
)


def test_parse_version():
    output = """Cisco IOS Software, Version 17.09.03
CORE-R1 uptime is 12 weeks
cisco ISR4451-X/K9
Processor board ID ABC123"""
    result = parse_version(output)
    assert result["hostname"] == "CORE-R1"
    assert result["os_version"] == "17.09.03"
    assert result["serial_number"] == "ABC123"


def test_parse_bgp_established():
    output = """203.0.113.2 4 65002 100 100 10 0 0 2d18h 45"""
    result = parse_bgp_summary(output)
    assert result[0]["healthy"] is True
    assert result[0]["prefixes_received"] == 45


def test_parse_ospf_full():
    output = """10.0.0.2 1 FULL/DR 00:00:34 10.0.0.2 GigabitEthernet0/0"""
    result = parse_ospf_neighbors(output)
    assert result[0]["healthy"] is True


def test_parse_interfaces():
    output = """Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     10.0.0.1        YES manual up                    up"""
    result = parse_interfaces(output)
    assert result[0]["interface"] == "GigabitEthernet0/0"
    assert result[0]["status"] == "up"
