import socket
import config
import json
import threading
import data
from Utils import Utils


class SocketServerThread(threading.Thread):
    def __init__(self, app_dy_info):
        threading.Thread.__init__(self)
        self.app_info = app_dy_info

    def run(self):
        self.start_server()

    def start_server(self):
        HOST = config.socket_ip
        PORT = config.socket_port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, int(PORT)))
        s.listen(1)
        Utils.printy('Start server to receive data from application.', 0)
        while 1:
            conn, addr = s.accept()
            input_data = conn.recv(2048)
            input_data = input_data[0:-1]
            if input_data == ('DONE:' + data.app_bundleID):
                if data.MITM_Done:
                    s.close()
                    break
                if not data.MITM_Done:
                    data.MITM_Done = True
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

        # print "input:        ", len(app_info.user_input)
        # print "traffic:      ", len(app_info.traffic_json_list)
        # print "mitm:         ", len(app_info.mitm_list)
        # print "cccrypt:      ", len(app_info.cccrtpy_json_list)
        # print "KeyChain:     ", len(app_info.keychain_json_list)
        # print "NSUserDefault:", len(app_info.userdefault_json_list)
        # print "Plist:        ", len(app_info.plist_json_list)
        # print "URLScheme:    ", len(app_info.urlscheme_list)

