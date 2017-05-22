from Util.database import DBServer
import iOSAVD
import data
import time
from Util.utils import Utils

dbServer = DBServer()
dbServer.on()
while True:
    # status == 2  untested
    try:
        dbServer.refresh_status()
        result = dbServer.execute("select appid, name, path from ios_app where status=?", "2")[0]
        id = result[0]
        name = Utils.ret_name_from_db(result[1])
        path = result[2]
        # status == 3 in progress
        dbServer.execute("update ios_app set status=? where appid=?", (3, id))
        # result = dbServer.execute("select * from ios_app where appid=?", (id,))
        task = iOSAVD.IOS(path, name).run()
        # data.report_path = "report"
        dbServer.execute("update ios_app set reportpath=?, status=? where appid=?", (data.report_path, '1', id))
        # result = dbServer.execute("select * from ios_app where appid=?", (id,))
        # result = dbServer.execute("select * from ios_app where appid=?", (id,))
    except IndexError:
        time.sleep(5)










