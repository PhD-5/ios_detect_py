import subprocess
import threading
import data
from Util.utils import Utils
import time
import os
import sys
sys.path.append('gen-py')
import importlib
from staticAnalyzer import StaticAnalyze
from staticAnalyzer.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

class static_analyzer(threading.Thread):
    def run(self):
        self.do_analyse()

    def do_analyse(self):
        # call the static.jar
        exec "from staticAnalyzer import StaticAnalyze"
        exec "from staticAnalyzer.ttypes import *"
        # importlib.import_module('staticAnalyzer.StaticAnalyze.*')
        # importlib.import_module('staticAnalyzer.ttypes.*')
        Utils.printy('Start static analysis', 0)
        time.sleep(1)
        try:
            transport = TSocket.TSocket('192.168.2.74', 9090)
            transport = TTransport.TBufferedTransport(transport)
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            client = StaticAnalyze.Client(protocol)
            transport.open()
            print "check connection"
            print "server - " + client.connect()
            print "start static analysis"
            report_dir = "{}/temp/{}/report".format(os.path.abspath('.'), data.start_time)
            msg = client.analyze(data.static_file_path, report_dir)
            print "server - " + msg
            transport.close()
        except Thrift.TException, ex:
            print "%s" % ex.message
        # cmd = 'java -jar ' + "ios-vulnerability-detection_fat.jar {} {}/temp/{}/report".format(data.static_file_path, os.path.abspath('..'), data.start_time)
        # subprocess.call(cmd, shell=True)