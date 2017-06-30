import socket
import config
import json
import threading
import data
import os
from Util.utils import Utils


class SocketServerThread(threading.Thread):
    def __init__(self, app_dy_info):
        threading.Thread.__init__(self)
        self.dynamic_socket = None
        self._stop_event = threading.Event()
        print "stop_event0", self._stop_event.is_set()
        self.app_info = app_dy_info

    def stop(self):
        self._stop_event.set()
        self.dynamic_socket.shutdown(0)
        self.dynamic_socket.close()
        print "stop_event1", self._stop_event.is_set()

    def stopped(self):
        print "stop_event2", self._stop_event.is_set()
        return self._stop_event.is_set()

    def run(self):
        self.start_server()

    def start_server(self):
        HOST = config.socket_ip
        PORT = config.socket_port
        self.dynamic_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dynamic_socket.bind((HOST, int(PORT)))
        self.dynamic_socket.listen(1)
        Utils.printy('Start server to receive data from application.', 0)
        while not self.stopped():
            conn, addr = self.dynamic_socket.accept()
            input_data = conn.recv(2048)
            input_data = input_data[0:-1]
            if input_data == ('DONE:' + data.app_bundleID):
                self.dynamic_socket.close()
                break
            self.parse_json(self.app_info, input_data)

    # classify and store jsons according to type
    def parse_json(self, app_info, json_str):

        try:
            json_dict = json.loads(json_str)
            if json_dict['bundle'] == app_info.bundle_id:
                type = json_dict['type']
                if type =='input':
                    app_info.user_input.append(json_dict['msg'])
                elif type == 'MITM':
                    app_info.mitm_list.append(json_dict['msg'])
                elif type == 'Traffic':
                    app_info.traffic_json_list.append(json_dict['msg'])
                elif type == 'CCCrypt':
                    app_info.cccrtpy_json_list.append(json_dict['msg'])
                elif type == 'KeyChain':
                    app_info.keychain_json_list.append(json_dict['msg'])
                elif type == 'NSUserDefaults':
                    app_info.userdefault_json_list.append(json_dict['msg'])
                elif type == 'Plist':
                    app_info.plist_json_list.append(json_dict['msg'])
                elif type == 'URLScheme':
                    app_info.urlscheme_list.append(json_dict['msg'])
        except BaseException:
            # print "parse json error"
            # print json_str
            pass



