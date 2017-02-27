from PreProcess import *
from modules import *
from Utils import *
from Report.DocGenerator import Generator
import data
from AppDynamicInfo import AppDynamicInfo
import os
import config
import time


class ios():
    def __init__(self):

        build_home_dir.build()
        data.client = set_ssl_conn(config.mobile_ip, config.ssh_port, config.mobile_user, config.mobile_password)
        # self.db = DBServer()
        # self.db.on()
        should_install.ask_for_user_choose()
        Utils.getInstalledAppList()
        Metadata().get_metadata()
        pre_clutch.clutch()

    def detect(self):
        # start java static analyse
        file_separator = os.path.sep
        os.chdir(os.path.abspath('.') + file_separator + 'lib')
        t_static = static_analyzer()
        t_static.start()
        # need to change dir to root, because in static thread the dir is changed to lib dir.
        time.sleep(2)  # make sure java -jar in thread can get into directory lib
        os.chdir(os.path.abspath('..'))

        # store the dynamic json results
        app_dynamic_info = AppDynamicInfo(data.app_bundleID)

        # ask for should need detect MITM
        while True:
            user_input = raw_input('Do you want to detect MITM? [Y/N]')
            if user_input == 'Y' or user_input == 'y':
                print '================================================================='
                print '=   If you want to detect the MITM, please config on phone:     ='
                print '=   OPEN the "MITM" and CLOSE the "Traffic"!                    ='
                print '================================================================='
                t_mitm_socket = SocketServerThread(app_dynamic_info)
                t_mitm_socket.start()
                t_mitm_socket.join()
                time.sleep(3)
                break
            elif user_input == 'N' or user_input == 'n':
                break
            else:
                print 'Invalid input! Please input Y or N\n'

        # start local socket server to receive socket msg from iphone
        print 'Ready to start other detects, please CLOSE the MITM...'
        t_socket = SocketServerThread(app_dynamic_info)
        t_socket.start()

        SharedLibrary().get()
        protect_check().check()
        String().get_strings()

        hosts = ','.join(String().get_url(data.strings))
        # Nessus().scan(hosts, data.app_bundleID)1


        # #########################end of dynamic detect####################
        t_socket.join()


        # copy the input data to class data
        input_md5_list = get_md5(app_dynamic_info.user_input)
        input_md5_list.extend(app_dynamic_info.user_input)
        data.input_list = set(input_md5_list)


        # detect sensitive content according to user input
        input_json_parser = input_parser()
        input_json_parser.parse_dynamic_info_for_input(app_dynamic_info)
        data.dynamic_sensitive_json = app_dynamic_info.sensitive_json

        # parse traffic json
        traffic_parser = TrafficParser(app_dynamic_info.traffic_json_list)
        traffic_parser.start_parser()
        data.traffic_unsafe_result = traffic_parser.result

        # parse MITM json
        mitm_parser = MitmParser(app_dynamic_info.mitm_list)
        mitm_parser.start_parse()
        data.mitm_results = mitm_parser.results

        # detect Hard Code
        hardcode_detect = HarCodeDetect(app_dynamic_info.cccrtpy_json_list)
        hardcode_detect.start_detect()
        # print 'hardcode:',hardcode_detect.result

        # detect sensitive data in files in sandbox
        Sql().get()
        Plist().get()

        # detect keychain
        keychain_checker = Keychain()
        keychain_checker.dump()
        data.keychain_values = keychain_checker.results

        # start url fuzz (after dynamic, because need the urlsheme info got from dynamic detect)
        # fuzzer = url_scheme_fuzzer(app_dynamic_info)
        # fuzzer.fuzz()
        # data.fuzz_result = fuzzer.results


        # because static analyse cost long time, so join in the last
        t_static.join()

        # generate report
        report_gen = Generator()
        report_gen.generate()

    def clean(self):
        data.client.close()
        self.db.down()


ios().detect()