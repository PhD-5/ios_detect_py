from PreProcess import build_home_dir
import config
import data
from modules import *
from Utils import *
from PreProcess import pre_clutch
from AppDynamicInfo import AppDynamicInfo
import os

class ios():
    def __init__(self):
        # get current time as root dir
        build_home_dir.build()

        # setup ssh client
        data.client = set_ssl_conn(config.mobile_ip, config.ssh_port, config.mobile_user, config.mobile_password)
        # data.omp_client = set_ssl_conn(config.server_ip, config.port, config.server_user, config.server_password)
        self.db = DBServer()
        self.db.on()
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
        os.chdir(os.path.abspath('..'))

        # start local socket server to receive socket msg from iphone
        app_dynamic_info = AppDynamicInfo(data.app_bundleID)
        t_socket = SocketServerThread(app_dynamic_info)
        t_socket.start()


        # Metadata().get_metadata()
        # scan_task = Scan("127.0.0.1", "test_")
        # scan_task.openvas_start()
        # scan_task.creat_target()
        # SharedLibrary().get()
        # protect_check().check()
        # static_analyzer().do_analyse()
        # Plist().get()
        # Sql().get()
        # String().get_url()
        # openvas().launch()
        # openvas().parse()

        t_socket.join()

        # start url fuzz (after dynamic, because need the urlsheme info got from dynamic detect)
        fuzzer = url_scheme_fuzzer(app_dynamic_info)
        fuzzer.fuzz()


        # because static analyse cost long time, so join in the last
        t_static.join()

    def clean(self):
        data.client.close()
        self.db.down()
        # data.omp_client.close()


ios().detect()