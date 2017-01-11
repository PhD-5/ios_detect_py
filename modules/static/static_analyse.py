import subprocess
import threading
import data


class static_analyzer(threading.Thread):

    def run(self):
        self.do_analyse()

    def do_analyse(self):
        # call the static.jar
        print 'start thread to do static analyse...'
        cmd = 'java -jar ' + 'ios-vulnerability-detection_fat.jar {} ../temp/{}/report'.format(data.static_file_path, data.start_time)
        print cmd
        # os.system(cmd)
        subprocess.call(cmd, shell=True)