# -*- coding:utf-8 -*-
import re
import os
import config
from Utils.utils import Utils
import data
import DumpDecrypted
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


# ------get clutch -i result-----
def clutch():
    client = data.client
    clutch_i = Utils.cmd_block(client, 'clutch -i')
    pat = re.compile(r'.+<(.+)>')

    clutch_app_id = -1
    for line in clutch_i.split('\n'):
        print line
        m = pat.match(line)
        if m:
            if m.group(1) == data.app_bundleID:
                clutch_app_id = int(line[0])

    if clutch_app_id != -1:
        clutch_success = False
        print 'the application is encrypted, and use clutch to decrypt'
        # clean the decrypted ipas already done by clutch
        cmd = 'rm /private/var/mobile/Documents/Dumped/*.ipa'
        Utils.cmd_block(client, cmd)

        # Only dump binary files from the specified bundleID
        cmd = 'clutch -b ' + str(clutch_app_id)
        out = Utils.cmd_block(client, cmd)
        pat = re.compile(r'.+Finished.+to (.+)\[0m')
        for line in out.split('\n'):
            m = pat.match(line)
            if m:
                clutch_success = True
                print m.group(1)
                source = '{path}/{bundle_id}/{binary}'.format(path=m.group(1),
                                                              bundle_id=data.metadata['bundle_id'],
                                                              binary=data.metadata['binary_name'])
                des = '{}/temp/{}/binary/'.format(os.path.abspath('.'), data.start_time) + data.metadata["binary_name"]
                print '{} to {}'.format(str(source), des)
                Utils.sftp_get(config.mobile_ip, config.ssh_port, config.mobile_user, config.mobile_password,
                               str(source), des)

                data.static_file_path = des

        if not clutch_success:
            print 'Failed to clutch! Try to dump the decrypted app into a file. '
            DumpDecrypted.dump_binary()

    else:
        print 'the application is not encrypted'
        print data.metadata['binary_path']
        print data.metadata['binary_name']
        cmd = 'cp {} /tmp/temp.binary'.format(data.metadata['binary_path'])
        Utils.cmd_block(data.client, cmd)
        Utils.sftp_get(config.mobile_ip, config.ssh_port, config.mobile_user, config.mobile_password,
                       '/tmp/temp.binary',
                       './temp/{}/binary/'.format(data.start_time) + data.metadata['bundle_id'])
        data.static_file_path = os.path.abspath('.') + ('/temp/{}/binary/'.format(data.start_time)) + data.metadata[
            'bundle_id']




