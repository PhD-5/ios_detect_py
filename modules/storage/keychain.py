import data
from Utils.utils import Utils
import config
import os

class Keychain():

    def __init__(self):
        self.client = data.client
        self.send_tool()
        self.all_keychain_values = []
        self.results = []

    def send_tool(self):
        Utils.sftp_put(ip=config.mobile_ip, port=config.ssh_port,
                       username=config.mobile_user, password=config.mobile_password,
                       local_file=os.path.abspath('.')+os.sep+'tools'+os.sep+'keychain_dumper', remote_path='./keychain_dumper')

    def dump(self):
        cmd = './keychain_dumper'
        out = Utils.cmd_block(self.client, cmd)
        lines = out.split('\n')
        for line in lines:
            if line.startswith('Keychain Data:') and not '(null)' in line:
                content = line[15:]
                if content:
                    self.all_keychain_values.append(content)
        self.filter()
        Utils.printy_result('Keychain Dump', 1)
        return self.results

    def filter(self):
        for value in self.all_keychain_values:
            if value in data.input_list:
                self.results.append(value)



