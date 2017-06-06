#_*_ coding:utf8 _*_
import threading
import socket
import json
from time import sleep

import config

class ApplistThread(threading.Thread):


    def run(self):
        HOST = config.socket_ip
        PORT = '9002'
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, int(PORT)+1 ))
        s.listen(1)
        while 1:
            conn, addr = s.accept()
            input_data = conn.recv(2048)
            # input_data = input_data[0:-1] # 不确定要不要
            input_dict = json.loads(input_data)
            print input_dict
            self.writeAppListToFile(input_dict)

    def writeAppListToFile(self, app_info):
        f = open('apps.txt','w')

        lines = []

        for bundle_id in app_info:
            line = bundle_id + ' * ' + app_info[bundle_id] + ' *\r\n'
            lines.append(line)
        lines[-1] = lines[-1][0:-2]
        f.writelines(lines)
        print 'write done'
        f.close()


if __name__ == '__main__':

    mydict = {'1':'aa','2':'招商银行'}

    t = ApplistThread()
    t.start()

    sleep(3)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.2.117',9003))
    s.send(json.dumps(mydict))