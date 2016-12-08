from openvas_lib import VulnscanManager, VulnscanException
from threading import Semaphore
from functools import partial
from openvas_lib import report_parser
from Utils.utils import Utils
import config
import data


class openvas():

    def __init__(self):
        self.client = data.omp_client
        self.result_name = None

    def launch(self):

        sem = Semaphore(0)

        try:
            scanner = VulnscanManager(config.omp_ip, config.omp_user, config.omp_password)
            task_id, target_id = scanner.launch_scan(target='https://log.cmbchina.com',
                                                     profile="Full and fast",
                                                     callback_end=partial(lambda x: x.release(), sem)
                                                     )
            print task_id, target_id
            sem.acquire()
            print("finished")

            report_id = scanner.get_report_id(task_id)
            self.result_name = task_id + '.csv'

            cmd = 'omp --get-report ' + report_id + ' --format ' + data.format_csv + ' > ' + self.result_name
            Utils.cmd_block(self.client, cmd)

            Utils.sftp_get(config.server_ip,
                           config.port,
                           config.server_user,
                           config.server_password,
                           self.result_name,
                           './temp/server/'+self.result_name)

        except VulnscanException as e:
            print("Error:")
            print(e)

    def parse(self):
        results = report_parser('temp/server/'+self.result_name)
        print(results)