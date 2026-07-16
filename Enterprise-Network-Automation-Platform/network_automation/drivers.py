import os
from netmiko import ConnectHandler
from .mock_data import MOCK

class MockDriver:
    def __init__(self, device):
        self.device = device

    def command(self, command):
        return MOCK[self.device["name"]][command]

    def configure(self, commands):
        return "Mock configuration applied:\n" + "\n".join(commands)

class NetmikoDriver:
    def __init__(self, device):
        self.device = device

    def params(self):
        return {
            "device_type": self.device["device_type"],
            "host": self.device["host"],
            "username": os.getenv("NET_USERNAME", ""),
            "password": os.getenv("NET_PASSWORD", ""),
            "secret": os.getenv("NET_SECRET", ""),
        }

    def command(self, command):
        with ConnectHandler(**self.params()) as connection:
            if self.params()["secret"]:
                connection.enable()
            return connection.send_command(command)

    def configure(self, commands):
        with ConnectHandler(**self.params()) as connection:
            if self.params()["secret"]:
                connection.enable()
            output = connection.send_config_set(commands)
            connection.save_config()
            return output

def get_driver(device, mock_mode):
    return MockDriver(device) if mock_mode else NetmikoDriver(device)
