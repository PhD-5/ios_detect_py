from PreProcess import build_home_dir
from PreProcess import should_install
from PreProcess import pre_clutch
from modules import *
from Utils import *
import data
from AppDynamicInfo import AppDynamicInfo
import os
import config
import time


class ios():
    def __init__(self):
        # get current time as root dir
        build_home_dir.build()

        # setup ssh client
        data.client = set_ssl_conn(config.mobile_ip, config.ssh_port, config.mobile_user, config.mobile_password)
        # data.omp_client = set_ssl_conn(config.server_ip, config.port, config.server_user, config.server_password)
        self.db = DBServer()
        self.db.on()

        # should install ipa from local
        should_install.ask_get_user_choose()

        Utils.getInstalledAppList()
        #--2016.12.09--yjb--preprocess
        Metadata().get_metadata()
        pre_clutch.clutch()




    def detect(self):
        # start java static analyse
        file_separator = os.path.sep
        os.chdir(os.path.abspath('.') + file_separator + 'lib')
        t_static = static_analyzer()
        t_static.start()
        # need to change dir to root, because in static thread the dir is changed to lib dir.
        time.sleep(3) #make sure java -jar in thread can get into directory lib
        os.chdir(os.path.abspath('..'))

        # store the dynamic json results
        app_dynamic_info = AppDynamicInfo(data.app_bundleID)

        # ask for should need detect MITM
        while True:
            user_input = raw_input('Do you want to detect MITE? [Y/N]')
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
        print 'Ready to start other detect, please CLOSE the MITM...'
        t_socket = SocketServerThread(app_dynamic_info)
        t_socket.start()


        # Metadata().get_metadata()
        # scan_task = Scan("127.0.0.1", "test_")
        # scan_task.openvas_start()
        # scan_task.creat_target()

        # openvas().launch('127.0.0.1')
        # SharedLibrary().get()
        # protect_check().check()
        # static_analyzer().do_analyse()

        # String().get_url()
        # openvas().launch()
        # openvas().parse()

        # end of dynamic detect
        t_socket.join()
        # copy the input data to class data
        data.input_list = app_dynamic_info.user_input

        # detect sensitive content according to user input
        # input_json_parser = input_parser()
        # input_json_parser.parse_dynamic_info_for_input(app_dynamic_info)

        # detect sensitive data in files in sandbox
        Plist().get()
        Sql().get()

        # detect Hard Code
        String().get_strings()
        hardcode_detect = HarCodeDetect(app_dynamic_info.cccrtpy_json_list)
        hardcode_detect.start_detect()
        print 'hardcode:',hardcode_detect.result

        # start url fuzz (after dynamic, because need the urlsheme info got from dynamic detect)
        # fuzzer = url_scheme_fuzzer(app_dynamic_info)
        # fuzzer.fuzz()


        # because static analyse cost long time, so join in the last
        t_static.join()

    def clean(self):
        data.client.close()
        self.db.down()
        data.omp_client.close()


ios().detect()