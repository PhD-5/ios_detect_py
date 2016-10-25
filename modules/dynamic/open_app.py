from Utils import utils
import data


def open():
    #the bundle id of application
    bundleID = data.app_bundleID

    #the client of ssh
    client = data.client

    #the cmd of open application
    open_cmd = 'open '+bundleID

    utils.Utils.cmd_block(client, open_cmd)
