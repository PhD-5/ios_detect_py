from Util.database import DBServer
import iOSAVD
import data
import time
from Util.utils import Utils
import signal
import os
import logging
import logging.config


def when_killed(signum, frame):
    print frame
    Utils.printy("Server Down", 2)
    dbServer.execute("update ios_app set status=? where status=?", (2, 3))
    os.system("kill -9 " + str(os.getpid()))

signal.signal(signal.SIGQUIT, when_killed)

dbServer = DBServer()
dbServer.on()
while True:
    # status == 2  untested
    try:
        dbServer.refresh_status()
        result = dbServer.execute("select appid, name, path from ios_app where status=?", "2")[0]
        id = result[0]
        data.database_appid = id
        name = Utils.ret_name_from_db(result[1])
        path = result[2]
        # status == 3 in progress
        dbServer.execute("update ios_app set status=? where appid=?", (3, id))
        # result = dbServer.execute("select * from ios_app where appid=?", (id,))
        reload(data)
        logging.config.fileConfig('config/logging.conf')
        data.logger = logging.getLogger('root')
        task = iOSAVD.IOS(path, name).run()
        # data.report_path = "report"
        dbServer.execute("update ios_app set reportpath=?, status=? where appid=?", (data.report_path, '1', id))
    except IndexError:
        Utils.printy("Waiting for Task", 0)
        time.sleep(10)










