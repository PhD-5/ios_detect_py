import data
from Utils.utils import Utils
import time
class url_scheme_fuzzer():

    def __init__(self, urls):
        self.fuzz_inputs = urls
        self.results = dict()
        self.app = data.metadata['binary_name']


    def delete_old_reports(self):
        cmd = 'rm -f `find {} -type f | grep {}`'.format(data.crash_report_folder, self.app)
        Utils.cmd_block(data.client, cmd)

    def fuzz(self):
        for url in self.fuzz_inputs:
            self.delete_old_reports()
            Utils.openurl(url)
            time.sleep(2)
            Utils.kill_by_name(self.app)
            self.results[url] = self.crashed()
        print self.results

    def crashed(self):
        cmd = 'find {} -type f | grep {}'.format(data.crash_report_folder, self.app)
        if Utils.cmd_block(data.client, cmd).split("\n")[0]:
            return True
        else:
            return False