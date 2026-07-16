MOCK = {
    "R1": {
        "show version": "Cisco IOS Software, Version 17.09.03\nR1 uptime is 12 weeks, 4 days\ncisco ISR4451-X/K9\nProcessor board ID FDO1234ABCD",
        "show running-config": "hostname R1\nservice password-encryption\naaa new-model\nip ssh version 2\nntp server 10.10.10.10\nlogging host 10.10.10.20\nsnmp-server community NETWORK-RO RO\nrouter ospf 10\nrouter bgp 65001",
        "show ip interface brief": "Interface IP-Address OK? Method Status Protocol\nGigabitEthernet0/0 10.0.0.1 YES manual up  up\nGigabitEthernet0/1 203.0.113.1 YES manual up  up",
        "show ip bgp summary": "203.0.113.2 4 65002 1200 1150 25 0 0 3d02h 45",
        "show ip ospf neighbor": "10.0.0.2 1 FULL/DR 00:00:34 10.0.0.2 GigabitEthernet0/0",
    },
    "R2": {
        "show version": "Cisco IOS Software, Version 17.06.05\nR2 uptime is 6 weeks, 2 days\ncisco ISR4331/K9\nProcessor board ID FDO5678EFGH",
        "show running-config": "hostname R2\nservice password-encryption\nip ssh version 2\nntp server 10.10.10.10\nlogging host 10.10.10.20\nrouter ospf 10\nrouter bgp 65002",
        "show ip interface brief": "Interface IP-Address OK? Method Status Protocol\nGigabitEthernet0/0 10.0.0.2 YES manual up  up\nGigabitEthernet0/1 203.0.113.2 YES manual up  up",
        "show ip bgp summary": "203.0.113.1 4 65001 980 965 21 0 0 2d18h 38",
        "show ip ospf neighbor": "10.0.0.1 1 FULL/BDR 00:00:31 10.0.0.1 GigabitEthernet0/0",
    },
    "SW1": {
        "show version": "Cisco IOS Software, Version 16.12.08\nSW1 uptime is 20 weeks, 1 day\ncisco WS-C9300-48P\nProcessor board ID FCW9876WXYZ",
        "show running-config": "hostname SW1\nservice password-encryption\naaa new-model\nip ssh version 2\nntp server 10.10.10.10\nlogging host 10.10.10.20\nsnmp-server community NETWORK-RO RO\nvlan 10\n name USERS",
        "show ip interface brief": "Interface IP-Address OK? Method Status Protocol\nVlan10 10.0.10.2 YES manual up  up\nGigabitEthernet1/0/1 unassigned YES unset up  up",
        "show ip bgp summary": "",
        "show ip ospf neighbor": "",
    },
    "SW2": {
        "show version": "Cisco IOS Software, Version 16.12.08\nSW2 uptime is 10 weeks, 3 days\ncisco WS-C9200-48P\nProcessor board ID FCW2468LMNO",
        "show running-config": "hostname SW2\nservice password-encryption\nip ssh version 2\nntp server 10.10.10.10\nsnmp-server community NETWORK-RO RO\nvlan 10\n name USERS",
        "show ip interface brief": "Interface IP-Address OK? Method Status Protocol\nVlan10 10.0.10.3 YES manual up  up\nGigabitEthernet1/0/1 unassigned YES unset down  down",
        "show ip bgp summary": "",
        "show ip ospf neighbor": "",
    },
}
