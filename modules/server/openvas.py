from openvas_lib import VulnscanManager, VulnscanException
from openvas_lib import report_parser

from Utils.utils import Utils
import data
from temp import config


class openvas():

    def __init__(self):
        self.client = data.omp_client
        self.result_name = '6b78d2ed-823a-4db3-bf4d-e5b2cc6f3dd4.xml'

    def launch(self):

        # sem = Semaphore(0)

        try:
            scanner = VulnscanManager(config.omp_ip, config.omp_user, config.omp_password)
            # task_id, target_id = scanner.launch_scan(target="127.0.0.1",
            #                                          profile="Full and fast",
            #                                          callback_end=partial(lambda x: x.release(), sem)
            #                                          )
            # print task_id, target_id
            # sem.acquire()
            print("finished")

            task_id = '6b78d2ed-823a-4db3-bf4d-e5b2cc6f3dd4'

            report_id = scanner.get_report_id(task_id)
            self.result_name = task_id + '.xml'

            cmd = 'omp --get-report ' + report_id + ' --format ' + data.format_xml + ' > ' + self.result_name
            Utils.cmd_block(self.client, cmd)
            print cmd


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