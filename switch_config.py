import time
from paramiko import SSHClient, AutoAddPolicy
import ipaddress
import argparse
from getpass import getpass


parser = argparse.ArgumentParser()
parser.add_argument('--net', type=str, help="destination subnet: 1.1.1.0/24, for single ip use 1.1.1.1/32", required=True)
parser.add_argument('--user', type=str, help="Username", required=True)
# parser.add_argument('--password', type=str, help="Password")
parser.add_argument('--cmd', type=str, help='enter command separated by commas: "conf t,int gi0/0,description test"', required=True)
args = parser.parse_args()

client = SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(AutoAddPolicy())


def config(user=None, subnet=None, cmd=None):
    
    cmd += ","
    net = ipaddress.ip_network(subnet).hosts()
    password = getpass()
    if "/32" in subnet:
        net = [ipaddress.ip_network(subnet).broadcast_address]

    for ip in net:
        try:
            client.connect(hostname=str(ip), username=user, password=password, look_for_keys=False, allow_agent=False, timeout=1)

            remote_conn = client.invoke_shell()
            print(f"connected to {ip}")
            output = remote_conn.recv(65535)
            [print(line) for line in output.decode('utf-8').split("\n")]
            time.sleep(1)
            for c in cmd.split(","):
                remote_conn.send(f'{c}\n')
                out = remote_conn.recv(65535)
                time.sleep(1)
                [print(line) for line in out.decode('utf-8').split("\n")]
            print(f"configuration is finished for {ip}")
        except Exception as error:
            print(f"connection to {ip} failed -> {error}")
    
config(args.user, subnet=args.net, cmd=args.cmd)
