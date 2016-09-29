from Utils.utils import Utils
import data
import simplejson


def getInstalledAppList():
    client = data.client
    # ------get install app plist and analyse------
    Utils.cmd_block(client,
                    'cp /var/mobile/Library/MobileInstallation/LastLaunchServicesMap.plist /var/mobile/Library/MobileInstallation/temp.plist')
    Utils.cmd_block(client, 'plutil -convert json /var/mobile/Library/MobileInstallation/temp.plist')
    json = Utils.cmd_block(client, 'cat /var/mobile/Library/MobileInstallation/temp.json')
    Utils.cmd_block(client, 'rm /var/mobile/Library/MobileInstallation/temp.plist')
    Utils.cmd_block(client, 'rm /var/mobile/Library/MobileInstallation/temp.json')
    json_dict = simplejson.loads(json)
    app_dict = json_dict['User']
    app_options = dict()

    i = 0
    for app in app_dict.keys():
        print i, ' : ', app
        app_options[i] = app
        i = i + 1

    # data.app_dict = app_options
    data.app_dict = app_dict

    app_id = int(raw_input("plz choose which app to analyse: "))
    print 'you have choose [', app_id, ']', app_options[app_id]
    data.app_bundleID = app_options[app_id]