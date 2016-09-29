import ssh
import installedAppList
import data
from modules.binary.metadata import Metadata
from modules.binary.protect_checks import protect_check
from modules.binary.shared_library import Shared_library
from modules.static.static_analyse import static_analyzer

# set up ssh connect for this analyse
ssh.set_ssl_conn()

# get installed app list
installedAppList.getInstalledAppList()

# get metadata
Metadata().get_metadata()

# get shared libraies
Shared_library().get()

# check protection
protect_check().check()

# static analyse
static_analyzer().do_analyse()


# in the end, close the ssh client
data.client.close()