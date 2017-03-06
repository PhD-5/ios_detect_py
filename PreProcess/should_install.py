import os
from Utils import Utils
import data
from modules.dynamic.open_app import open_some_app
import time
import config
import clint


def ask_for_user_choose():
    Utils.printy('[1]: I have installed the app .', 1)
    Utils.printy('[2]: I have the ipa file local to install.', 1)
    while True:
        user_choose_input = raw_input(clint.textui.colored.yellow("> >> >>> Enter your choice please [1/2]: > "))
        if user_choose_input == '1':
            break
        elif user_choose_input == '2':
            install_ipa_from_local()
            break
        else:
            Utils.printy('Invalid input!', 2)


def install_ipa_from_local():
    while True:
        ipa_path = raw_input(clint.textui.colored.yellow("> >> >>> Input the Path: > ")).strip()
        if not os.path.exists(ipa_path):
            Utils.printy_result('No such file ', 0)
        elif not ipa_path.endswith("ipa"):
            Utils.printy_result('Not ipa file ', 0)
        else:
            Utils.printy('Installing.. ', 0)
            #sftp to iPhone
            Utils.sftp_put(config.mobile_ip, config.ssh_port, config.mobile_user, config.mobile_password, '/tmp/detect/temp.ipa', ipa_path)
            #install ipa use ipainstaller
            Utils.cmd_block(data.client, "ipainstaller /tmp/detect/temp.ipa")
            # respring ...
            open_some_app("com.bigboss.respring")
            Utils.printy('Respring.. ', 0)
            time.sleep(int(config.respring_time))
            break

