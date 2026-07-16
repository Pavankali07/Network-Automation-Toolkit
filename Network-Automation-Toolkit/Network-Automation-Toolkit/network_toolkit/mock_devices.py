MOCK_OUTPUTS = {
    "CORE-R1": {
        "show version": """Cisco IOS Software, Version 17.09.03
CORE-R1 uptime is 12 weeks, 4 days, 3 hours
cisco ISR4451-X/K9
Processor board ID FDO1234ABCD""",
        "show running-config": """hostname CORE-R1
service password-encryption
aaa new-model
ip ssh version 2
ntp server 10.10.10.10
logging host 10.10.10.20
snmp-server community NETWORK-RO RO
router ospf 10
 network 10.0.0.0 0.0.0.255 area 0
router bgp 65001
 neighbor 203.0.113.2 remote-as 65002""",
        "show ip bgp summary": """Neighbor        V    AS MsgRcvd MsgSent TblVer InQ OutQ Up/Down State/PfxRcd
203.0.113.2     4 65002    1200    1150     25   0    0 3d02h 45""",
        "show ip ospf neighbor": """Neighbor ID     Pri State           Dead Time Address         Interface
10.0.0.2          1 FULL/DR         00:00:34 10.0.0.2        GigabitEthernet0/0""",
        "show ip interface brief": """Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     10.0.0.1        YES manual up                    up
GigabitEthernet0/1     203.0.113.1     YES manual up                    up
GigabitEthernet0/2     unassigned      YES unset  administratively down down"""
    },
    "EDGE-R1": {
        "show version": """Cisco IOS Software, Version 17.06.05
EDGE-R1 uptime is 6 weeks, 2 days, 8 hours
cisco ISR4331/K9
Processor board ID FDO5678EFGH""",
        "show running-config": """hostname EDGE-R1
service password-encryption
ip ssh version 2
ntp server 10.10.10.10
logging host 10.10.10.20
router ospf 10
 network 10.0.1.0 0.0.0.255 area 0
router bgp 65002
 neighbor 203.0.113.1 remote-as 65001""",
        "show ip bgp summary": """Neighbor        V    AS MsgRcvd MsgSent TblVer InQ OutQ Up/Down State/PfxRcd
203.0.113.1     4 65001     980     965     21   0    0 2d18h 38""",
        "show ip ospf neighbor": """Neighbor ID     Pri State           Dead Time Address         Interface
10.0.0.1          1 FULL/BDR        00:00:31 10.0.0.1        GigabitEthernet0/0""",
        "show ip interface brief": """Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     10.0.0.2        YES manual up                    up
GigabitEthernet0/1     203.0.113.2     YES manual up                    up"""
    },
    "ACCESS-SW1": {
        "show version": """Cisco IOS Software, Version 16.12.08
ACCESS-SW1 uptime is 20 weeks, 1 day, 1 hour
cisco WS-C9300-48P
Processor board ID FCW9876WXYZ""",
        "show running-config": """hostname ACCESS-SW1
service password-encryption
aaa new-model
ip ssh version 2
ntp server 10.10.10.10
snmp-server community NETWORK-RO RO
vlan 10
 name USERS
vlan 20
 name VOICE""",
        "show ip bgp summary": "",
        "show ip ospf neighbor": "",
        "show ip interface brief": """Interface              IP-Address      OK? Method Status                Protocol
Vlan10                 10.0.10.2       YES manual up                    up
GigabitEthernet1/0/1   unassigned      YES unset  up                    up
GigabitEthernet1/0/2   unassigned      YES unset  down                  down"""
    }
}


def run_mock_command(device_name: str, command: str) -> str:
    try:
        return MOCK_OUTPUTS[device_name][command]
    except KeyError as exc:
        raise ValueError(
            f"No mock output for device={device_name!r}, command={command!r}"
        ) from exc
