import data
from Utils import Utils
import config
import os



def via_sftp(src):

    file_sep = os.sep

    cmd = 'cp {} /tmp/temp.binary'.format(src)
    Utils.cmd_block(data.client, cmd)
    src = '/tmp/temp.binary'
    # des = '{}/temp/{}/binary/'.format(os.path.abspath('.'), data.start_time) + data.metadata['bundle_id']
    des = data.cur_workspace+os.sep+'binary'+os.sep+data.metadata['bundle_id']
    Utils.sftp_get(config.mobile_ip, config.ssh_port, config.mobile_user, config.mobile_password, src, des)
    return des
