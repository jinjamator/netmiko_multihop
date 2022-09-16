import netmiko
from copy import deepcopy
import logging  # noqa

log = logging.getLogger(__name__)

platforms = {
    "linux": {
        "ssh_base_cmd": "/usr/bin/ssh",
        "ssh_cmd_str": "{ssh_base_cmd} {ssh_verbose_option} -p {port} {optional_parameters} {username}@{ip}",
        "ssh_password_pattern": "[pP]assword:",
        "ssh_accept_host_pattern": "yes/no",
        "ssh_accept_host_command": "yes",
        "ssh_verbose_option": "",
        "ssh_disconnect_sequence": "~.\n",
        "optional_parameters": "",
    },
    "cisco_nxos": {
        "ssh_base_cmd": "ssh",
        "ssh_cmd_str": "{ssh_base_cmd} {username}@{ip} {vrf_str} {optional_parameters}",
        "ssh_password_pattern": "[pP]assword:",
        "ssh_accept_host_pattern": "yes/no",
        "ssh_accept_host_command": "yes",
        "ssh_verbose_option": None,
        "ssh_disconnect_sequence": "~.\n",
        "vrf_prefix": "vrf ",
        "optional_parameters": "",
        "vrf_str": "",
    },
    "cisco_ios": {
        "ssh_base_cmd": "ssh",
        "ssh_cmd_str": "{ssh_base_cmd} -l {username} -p {port} {vrf_str} {ip} {optional_parameters}",
        "ssh_password_pattern": "[pP]assword:",
        "ssh_accept_host_pattern": "yes/no",
        "ssh_accept_host_command": "yes",
        "ssh_verbose_option": None,
        "ssh_disconnect_sequence": "~.\n",
        "vrf_prefix": "-vrf ",
        "optional_parameters": "",
        "vrf_str": "",
    },
}


def jump_back(self):
    if not hasattr(self, "__jump_device_list"):
        raise Exception("No previous host to jump back to")
    try:
        prev_platform = self.__jump_device_list.pop()
    except IndexError:
        raise Exception("No previous host to jump back to")

    self.write_channel(
        platforms.get(self.device_type, platforms["linux"])["ssh_disconnect_sequence"]
    )
    netmiko.redispatch(self, prev_platform["device_type"])
    self.find_prompt()
    log.debug(
        f"successfully jumped back to {prev_platform['device_type']} {prev_platform['username']}@{prev_platform['ip']}"
    )

    return self


def jump_to(self, **kwargs):
    try:
        target_ip = kwargs["ip"]
    except KeyError:
        raise netmiko.ConfigInvalidException("Jump target IP must be set")
    try:
        target_username = kwargs["username"]
    except KeyError:
        raise netmiko.ConfigInvalidException("Jump target username must be set")
    try:
        target_password = kwargs["password"]
    except KeyError:
        raise netmiko.ConfigInvalidException("Jump target password must be set")
    try:
        target_port = kwargs["port"]
    except KeyError:
        target_port = 22
    try:
        target_device_type = kwargs["device_type"]
    except KeyError:
        target_device_type = "linux"

    if not hasattr(self, "__jump_device_list"):
        self.__jump_device_list = []

    no_log = {"password": target_password}
    log.addFilter(netmiko.base_connection.SecretsFilter(no_log=no_log))

    ssh_accept_host_pattern = platforms[self.device_type]["ssh_accept_host_pattern"]
    ssh_password_pattern = platforms[self.device_type]["ssh_password_pattern"]
    ssh_accept_host_command = platforms[self.device_type]["ssh_accept_host_command"]
    cfg = deepcopy(platforms[self.device_type])
    for k, v in kwargs.items():
        cfg[k] = v

    if "vrf" in kwargs:
        cfg[
            "vrf_str"
        ] = f"{platforms[self.device_type].get('vrf_prefix', '')}{kwargs['vrf']}"

    ssh_cmd_str = platforms[self.device_type]["ssh_cmd_str"].format(**cfg)
    log.debug(ssh_cmd_str)

    try:
        result = self.send_command(
            ssh_cmd_str, f"({ssh_password_pattern})|({ssh_accept_host_pattern})"
        )
    except Exception:
        raise netmiko.ConfigInvalidException(f"Cannot jump to {target_ip}.")

    if ssh_accept_host_pattern in result:
        self.send_command(ssh_accept_host_command, ssh_password_pattern)
    self.write_channel(target_password + "\n")

    self.__jump_device_list.append(
        {"ip": self.host, "device_type": self.device_type, "username": self.username}
    )
    netmiko.redispatch(self, target_device_type)
    self.find_prompt()
    log.debug(
        f"successfully jumped to {target_device_type} {target_username}@{target_ip}"
    )
    return self


setattr(netmiko.BaseConnection, "jump_to", jump_to)
setattr(netmiko.BaseConnection, "jump_back", jump_back)
