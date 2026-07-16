from network_automation.parsers import parse_version, parse_bgp, parse_ospf

def test_version():
    text = "Cisco IOS Software, Version 17.09.03\nR1 uptime is 12 weeks\ncisco ISR4451-X/K9\nProcessor board ID ABC123"
    result = parse_version(text)
    assert result["hostname"] == "R1"
    assert result["os_version"] == "17.09.03"

def test_bgp():
    result = parse_bgp("203.0.113.2 4 65002 100 100 10 0 0 2d18h 45")
    assert result[0]["healthy"] is True
    assert result[0]["prefixes_received"] == 45

def test_ospf():
    result = parse_ospf("10.0.0.2 1 FULL/DR 00:00:34 10.0.0.2 GigabitEthernet0/0")
    assert result[0]["healthy"] is True
