# -*- coding:utf-8 -*-
import re
import os
import config
from Utils.utils import Utils
import data
import DumpDecrypted
import sys
import bin_get

reload(sys)
sys.setdefaultencoding('utf-8')


# ------get clutch -i result-----
def clutch():
    client = data.client
    clutch_i = Utils.cmd_block(client, 'clutch -i')
    pat = re.compile(r'.+<(.+)>')

    clutch_app_id = -1
    for line in clutch_i.split('\n'):
        # print line
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
                # print m.group(1)
                source = '{path}/{bundle_id}/{binary}'.format(path=m.group(1),
                                                              bundle_id=data.metadata['bundle_id'],
                                                              binary=data.metadata['binary_name'])
                data.static_file_path = bin_get.via_sftp(source)

        if not clutch_success:
            Utils.printy('Failed to clutch! Try to dump the decrypted app into a file. ', 2)
            DumpDecrypted.dump_binary()

    else:
        # print 'the application is not encrypted'
        data.static_file_path = bin_get.via_sftp(data.metadata['binary_path'])





