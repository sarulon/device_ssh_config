import time
import sys
from paramiko import SSHClient, AutoAddPolicy
import ipaddress
import argparse
from getpass import getpass
import csv


parser = argparse.ArgumentParser()
parser.add_argument('--net', type=str, help="destination subnet: 1.1.1.0/24, for single ip use 1.1.1.1/32",
                    required='--file' not in sys.argv)
parser.add_argument('--user', type=str, help="Username", required='--file' not in sys.argv)
# parser.add_argument('--password', type=str, help="Password")
parser.add_argument('--cmd', type=str, help='enter command separated by commas: "conf t,int gi0/0,description test"',
                    required='--file' not in sys.argv)
parser.add_argument('--file', type=str, help='read from csv file: 1.1.1.1, show run')
args = parser.parse_args()

client = SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(AutoAddPolicy())


def config(user=None, subnet=None, cmd=None):
    password = getpass()
    if args.file:
        with open(args.file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                user = user if args.user else row[2]
                execute_command(row[0], user=user, password=password, cmd=f"{row[1]},")
    else:
        net = ipaddress.ip_network(subnet).hosts()
        if "/32" in subnet:
            net = [ipaddress.ip_network(subnet).broadcast_address]
        for ip in net:
            execute_command(ip=ip, user=user, password=password, cmd=f"{cmd},")


def execute_command(ip=None, user=None, password=None, cmd=None):
    try:
        client.connect(hostname=str(ip), username=user, password=password, look_for_keys=False,
                       allow_agent=False, timeout=1)

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
