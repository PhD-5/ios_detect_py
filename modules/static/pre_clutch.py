from Utils.utils import Utils
import data
import re
import ssh
import os


#------get clutch -i result-----
def use_clutch():
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
        cmd = 'clutch -d ' + str(clutch_app_id)
        out = Utils.cmd_block(client, cmd)
        pat = re.compile(r'DONE:\s(.+ipa)')
        for line in out.split('\n'):
            print line
            m = pat.match(line)
            if m:
                clutch_success = True
                print m.group(1)
                Utils.sftp_get(ssh.ip, ssh.port, ssh.username, ssh.password, m.group(1), './temp/'+ data.app_bundleID+'.ipa')
                data.static_file_path = os.path.abspath('.')+'/temp/' + data.app_bundleID+'.ipa'
        if not clutch_success:
            print 'clutch failed'
            exit(-1)

    else:
        print 'the application is not encrypted'
        print data.metadata['binary_path']
        Utils.sftp_get(ssh.ip,ssh.port,ssh.username,ssh.password,data.metadata['binary_path'],'./temp/'+data.metadata['binary_name'])
        data.static_file_path = os.path.abspath('.')+'/temp/'+ data.metadata['binary_name']
