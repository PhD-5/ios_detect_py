import subprocess
import threading
import data
from Utils import Utils
import time


class static_analyzer(threading.Thread):
    def run(self):
        self.do_analyse()

    def do_analyse(self):
        # call the static.jar
        Utils.printy('Start static analysis', 0)
        time.sleep(1)
        cmd = 'java -jar ' + "ios-vulnerability-detection_fat.jar {} ../temp/{}/report".format(data.static_file_path,                                                                                      data.start_time)
        subprocess.call(cmd, shell=True)