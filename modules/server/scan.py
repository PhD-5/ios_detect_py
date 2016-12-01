import data
from Utils.utils import Utils
import xml.etree.ElementTree as ET
class Scan():

    def __init__(self, target_ip, target_name):
        self.client = data.omp_client
        self.ip = target_ip
        self.target_name = target_name
        self.target_id = None

    def openvas_start(self):
        cmd = "sudo service openvas-scanner restart"
        out = Utils.cmd_block(self.client, cmd).split("\n")
        print "1", out
        cmd = "sudo service openvas-manager restart"
        out = Utils.cmd_block(self.client, cmd).split("\n")
        print "2", out
        cmd = "sudo openvasmd --rebuild --progress"
        out = Utils.cmd_block(self.client, cmd).split("\n")
        print "3", out

    def creat_target(self):
        cmd = 'omp -X "<create_target><name>'+self.target_name+'</name><hosts>'+self.ip+'</hosts></create_target>"'
        out = Utils.cmd_block(self.client, cmd).split("\n")
        print "4", out[0]
        status = ET.fromstring(out[0]).attrib['status']
        print status
        if status == "400":
            cmd = "omp -T | grep " + self.target_name
            out = Utils.cmd_block(self.client, cmd).split("\n")
            self.target_id = out[0].split(" ")[0]

        if status == "201":
            self.target_id = ET.fromstring(out[0]).attrib['id']

        print self.target_id


