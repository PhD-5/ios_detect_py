from PreProcess import build_home_dir
import config
import data
from modules import *
from Utils import *
from PreProcess import pre_clutch
from AppDynamicInfo import AppDynamicInfo

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
        # start local socket server to receive socket msg from iphone
        app_dynamic_info = AppDynamicInfo(data.app_bundleID)
        t = SocketServerThread(app_dynamic_info)
        t.start()

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

        t.join()

        # start url fuzz (after dynamic, because need the urlsheme info got from dynamic detect)
        fuzzer = url_scheme_fuzzer(app_dynamic_info)
        fuzzer.fuzz()

    def clean(self):
        data.client.close()
        self.db.down()
        # data.omp_client.close()


ios().detect()