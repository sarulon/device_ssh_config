import time
import sys
from paramiko import SSHClient, AutoAddPolicy
import ipaddress
import argparse
from getpass import getpass


client = SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(AutoAddPolicy())


def execute_command(ip=None, user=None, password=None, cmd=None, log=None):
    try:
        client.connect(hostname=str(ip), username=user, password=password, look_for_keys=False,
                       allow_agent=False, timeout=1)

        remote_conn = client.invoke_shell()
        log.appendPlainText(f"connected to {ip}\n")
        # print(f"connected to {ip}")
        output = remote_conn.recv(65535)
        [log.appendPlainText(f"{line}\n") for line in output.decode('utf-8').split("\n")]
        time.sleep(1)
        for c in cmd.split(","):
            remote_conn.send(f'{c}\n')
            out = remote_conn.recv(65535)
            time.sleep(1)
            [log.appendPlainText(f"{line}\n") for line in out.decode('utf-8').split("\n")]
        print(f"configuration is finished for {ip}\n")
    except Exception as error:
        log.appendPlainText(f"connection to {ip} failed -> {error}\n")


def execute_with_subnet(subnet=None, user=None, password=None, cmd=None, log=None):
    net = []
    if "/32" in subnet:
        net = [ipaddress.ip_network(subnet).broadcast_address]
    elif "/" in subnet:
        net = ipaddress.ip_network(subnet).hosts()
    else:
        net = [ipaddress.ip_network(f"{subnet}/32").broadcast_address]
    for ip in net:
        execute_command(ip=ip, user=user, password=password, cmd=f"{cmd},", log=log)






