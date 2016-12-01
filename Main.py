import installedAppList
import data
from modules.binary.metadata import Metadata
from Utils.database import DBServer

# set up ssh connect for this analyse
from temp import ssh, config

data.client = ssh.set_ssl_conn(config.mobile_ip, config.port, config.mobile_user, config.mobile_password)
# data.omp_client = ssh.set_ssl_conn(config.server_ip, config.port, config.server_user, config.server_password)
# print(data.omp_client)

print data.db
db = DBServer()

db.setup()
db.on()

# scan_task = Scan("127.0.0.1", "test_")
# scan_task.openvas_start()
# scan_task.creat_target()


# get installed app list
installedAppList.getInstalledAppList()

# get metadata
Metadata().get_metadata()

# # get shared libraies
# Shared_library().get()
#
# # check protection
# protect_check().check()
#
# # static analyse
# static_analyzer().do_analyse()
#
# # Plist().get()
# # Sql().get()
#
# String().get_url()

# in the end, close the ssh client
data.client.close()


# openvas().launch()
# openvas().parse()
# data.omp_client.close()
db.down()

