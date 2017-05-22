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
        exec "from staticAnalyzer import StaticAnalyze"
        exec "from staticAnalyzer.ttypes import *"
        Utils.printy('Start static analysis', 0)
        time.sleep(1)
        try:
            transport = TSocket.TSocket('192.168.133.128', 9090)
            transport = TTransport.TBufferedTransport(transport)
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            client = StaticAnalyze.Client(protocol)
            transport.open()
            client.connect()
            # print "check connection"
            # print "server - " + client.connect()
            # print "start static analysis"
            # print data.root
            # print os.path.abspath('.')
            report_dir = "{}/temp/{}/report".format(data.root, data.start_time)
            msg = client.analyze(data.static_file_path, report_dir)
            # print "server - " + msg
            transport.close()
        except Thrift.TException, ex:
            print "%s" % ex.message