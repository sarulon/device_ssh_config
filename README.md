# device_ssh_config
### configure devices with paramiko
required paramiko
-------------------------------------------------------------------------------------------------------------------
### arguments
<p> -h, --help           show this help message and exit</p>
<p>  --net NET            destination network 1.1.1.0/24</p>
<p>  --user USER          Username</p>
<p>  --password PASSWORD  Password</p>
<p>  --cmd CMD            enter command separated by commas: conf t,int gi0/0,ip address 2.2.2.2 255.255.255.255 </p>

usage: <code>python switch_config.py --net 1.1.1.0/24 --user alex --cmd "pwd,touch ssh_test.log"</code>
