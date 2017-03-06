from PreProcess import *
from modules import *
from Utils import *
from Report.DocGenerator import Generator
import data
from AppDynamicInfo import AppDynamicInfo
import os
import config
import time
import clint
import socket


class IOS():
    def __init__(self):
        IOS.prepare_for_basic_info()
        # self.db = DBServer()
        # self.db.on()
        self.t_static = static_analyzer()
        self.app_dynamic_info = AppDynamicInfo(data.app_bundleID)
        self.t_socket = SocketServerThread(self.app_dynamic_info)
        self.server = Nessus()

    @staticmethod
    def prepare_for_basic_info():
        while True:
            try:
                Utils.printy('Conneting..', 0)
                data.client = set_ssl_conn(config.mobile_ip, config.ssh_port, config.mobile_user, config.mobile_password)
                break
            except socket.error:
                time.sleep(5)
                Utils.printy_result('Operation timed out.', 0)

        build_home_dir.build()
        should_install.ask_for_user_choose()
        Utils.getInstalledAppList()
        Metadata().get_metadata()
        pre_clutch.clutch()

    def start_static_analyse(self):
        file_separator = os.path.sep
        os.chdir(os.path.abspath('.') + file_separator + 'lib')
        self.t_static.start()
        # need to change dir to root, because in static thread the dir is changed to lib dir.
        time.sleep(2)  # make sure java -jar in thread can get into directory lib
        os.chdir(os.path.abspath('..'))

    def finish_static_analyse(self):
        self.t_static.join()
        Utils.printy_result('Static Analyse.', 1)
        return True

    def start_dynamic_check(self):
        self.t_socket.start()
        time.sleep(1)
        while True:
            user_input = raw_input(clint.textui.colored.yellow('> >> >>> Do you want to detect MITM? [Y/N] > '))
            if user_input == 'Y' or user_input == 'y':
                # print '================================================================='
                # print '=   If you want to detect the MITM, please config on phone:     ='
                # print '=   OPEN the "MITM" and CLOSE the "Traffic"!                    ='
                # print '================================================================='
                Utils.printy('CONFIG YOUR PHONE : MITM ON and Traffic OFF', 3)
                # Utils.printy('Start MITM detect.', 0)
                while not data.MITM_Done:
                    time.sleep(2)
                Utils.printy_result('MITM Check.', 1)
                Utils.printy("CONFIG YOUR PHONE : MITM OFF and Traffic ON", 3)
                break
            elif user_input == 'N' or user_input == 'n':
                data.MITM_Done = True
                Utils.printy("CONFIG YOUR PHONE : MITM OFF and Traffic ON", 3)
                break
            else:
                Utils.printy('Invalid input! Please input Y or N', 1)

    def finish_dynamic_check(self):
        self.t_socket.join()
        Utils.printy_result("Dynamic Check .", 1)
        return True

    def finish_server_scan(self):
        self.server.join()
        Utils.printy_result('Server Scan.', 1)

    @staticmethod
    def storage_check():
        Sql().get()
        Plist().get()
        # detect keychain
        keychain_checker = Keychain()
        keychain_checker.dump()
        data.keychain_values = keychain_checker.results

    @staticmethod
    def binary_check():
        SharedLibrary().get()
        protect_check().check()
        String().get_strings()

    def server_scan(self):
        hosts = ','.join(String().get_url(data.strings))
        self.server.set_args(hosts, data.app_bundleID)
        self.server.start()

    def analyse(self):
        # copy the input data to class data
        input_md5_list = get_md5(self.app_dynamic_info.user_input)
        input_md5_list.extend(self.app_dynamic_info.user_input)
        data.input_list = set(input_md5_list)

        # detect sensitive content according to user input
        input_json_parser = input_parser()
        input_json_parser.parse_dynamic_info_for_input(self.app_dynamic_info)
        data.dynamic_sensitive_json = self.app_dynamic_info.sensitive_json

        # parse traffic json
        traffic_parser = TrafficParser(self.app_dynamic_info.traffic_json_list)
        traffic_parser.start_parser()
        data.traffic_unsafe_result = traffic_parser.result

        # parse MITM json
        mitm_parser = MitmParser(self.app_dynamic_info.mitm_list)
        mitm_parser.start_parse()
        data.mitm_results = mitm_parser.results

        # detect Hard Code
        hardcode_detect = HarCodeDetect(self.app_dynamic_info.cccrtpy_json_list)
        hardcode_detect.start_detect()
        # print 'hardcode:',hardcode_detect.result

        fuzzer = url_scheme_fuzzer(self.app_dynamic_info)
        fuzzer.fuzz()

    def run(self):
        self.start_static_analyse()
        self.start_dynamic_check()
        IOS.binary_check()
        self.server_scan()
        if self.finish_dynamic_check():
            self.analyse()
            IOS.storage_check()
        if self.finish_static_analyse():
            report_gen = Generator()
            report_gen.generate()
        if self.finish_server_scan():
            self.clean()

    def clean(self):
        data.client.close()
        # self.db.down()

IOS().run()


