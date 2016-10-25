import paramiko
import data
import config


# ------ssh parameters------
# ip       = "192.168.3.248"
# port     = 22
# username = "root"
# password = "alpine"
session_timeout = 60

def set_ssl_conn():
    #get config
    ip = config.iphone_ip
    port= config.ssh_port
    username = config.ssh_username
    password = config.ssh_password

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port, username=username, password=password)
    data.client = client
