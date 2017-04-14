import subprocess
import threading
import data
from Utils import Utils
import time
import os


class static_analyzer(threading.Thread):
    def run(self):
        self.do_analyse()

    def do_analyse(self):
        # call the static.jar
        Utils.printy('Start static analysis', 0)
        time.sleep(1)
        report_path = os.path.abspath('..')+os.sep+data.start_time+os.sep+'report'
        cmd = 'java -jar ' + "ios-vulnerability-detection_fat.jar {} {}".format(data.static_file_path, report_path)
        # print cmd
        # print os.path.abspath('.')
        # print os.path.abspath('..')
        subprocess.call(cmd, shell=True)