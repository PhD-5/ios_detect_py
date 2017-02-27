import os
from Utils import Utils
import data
from modules.dynamic.open_app import open_some_app
import time
import config


def ask_for_user_choose():
    print 'iOS Detect Start!'
    while True:
        print '\n[1]: I have installed the app .'
        print '[2]: I have the ipa file local to install.'
        user_choose_input = raw_input("plz choose : ")
        if user_choose_input == '1':
            break
        elif user_choose_input == '2':
            install_ipa_from_local()
            break
        else:
            print 'invalid input! input again...'


def install_ipa_from_local():
    while True:
        print '\nplease input the ipa path...'
        ipa_path = raw_input("plz choose which app to analyse: ")
        if not os.path.exists(ipa_path):
            print "ipa file dosn't exist...input again"
        elif not ipa_path.endswith("ipa"):
            print "input is not a ipa file...input again"
        else:
            print 'installing ipa ...'
            #sftp to iPhone
            Utils.sftp_put(config.mobile_ip, config.ssh_port, config.mobile_user, config.mobile_password, '/tmp/detect/temp.ipa', ipa_path)
            #install ipa use ipainstaller
            Utils.cmd_block(data.client, "ipainstaller /tmp/detect/temp.ipa")
            # respring ...
            open_some_app("com.bigboss.respring")
            print('respring...')
            time.sleep(int(config.respring_time))
            break

