from Util.database import DBServer
import iOSAVD
import data
import time

dbServer = DBServer()
dbServer.on()
while True:
    result = dbServer.execute("select appid, name, path from ios_app where status=?", "2")[0]
    id = result[0]
    name = result[1]
    path = result[2]
    task = iOSAVD.IOS(path, name).run()
    dbServer.execute("update ios_app set reportpath=? where appid=?", (data.report_path, id))
    # result = dbServer.execute("select * from ios_app where appid=?", (id,))










