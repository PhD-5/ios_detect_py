import ssh
import installedAppList
import data
from modules.binary.metadata import Metadata

# set up ssh connect for this analyse
ssh.set_ssl_conn()

# get installed app list
installedAppList.getInstalledAppList()

# get metadata
#Metadata.get_metadata()

# get shared libraies


# check protection





# in the end, close the ssh client
data.client.close();