import config
import data
from modules import *
from Utils import *
from PreProcess import pre_clutch
import threading

class ios():
    def __init__(self):

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
        t = SocketServerThread()
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
        String().get_url()
        # openvas().launch()
        # openvas().parse()

        t.join()

    def clean(self):
        data.client.close()
        self.db.down()
        # data.omp_client.close()


ios().detect()