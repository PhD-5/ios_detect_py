import sys
import time
sys.path.append('./gen-py')
from staticAnalyzer import StaticAnalyze
from staticAnalyzer.ttypes import *
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer


class analyzerHandler:

    def connect(self):
        return "Connected"
    def analyze(self, bin_path, report_dir):
        ret = "Received: " + msg
        print ret
        return ret

handler = analyzerHandler()
processor = StaticAnalyze.Processor(handler)
transport = TSocket.TServerSocket("localhost", 9090)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
print "Starting thrift server in python..."
server.serve()
print "done!"
