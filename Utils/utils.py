#coding=utf-8
import os
import re
import paramiko
import data
import simplejson

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# ======================================================================================================================
# GENERAL UTILS
# ======================================================================================================================
class Utils():
    # ==================================================================================================================
    # PATH UTILS
    # ==================================================================================================================
    @staticmethod
    def escape_path(path):
        """Escape the given path."""
        import pipes
        path = path.strip(''''"''')  # strip occasional single/double quotes from both sides
        return pipes.quote(path)

    @staticmethod
    def escape_path_scp(path):
        """To be correctly handled by scp, paths must be quoted 2 times."""
        temp = Utils.escape_path(path)
        return '''"%s"''' % temp

    @staticmethod
    def extract_filename_from_path(path):
        return os.path.basename(path)

    @staticmethod
    def extract_paths_from_string(str):
        # Check we have a correct number of quotes
        if str.count('"') == 4 or str.count("'") == 4:
            # Try to get from double quotes
            paths = re.findall(r'\"(.+?)\"', str)
            if len(paths) == 2: return paths[0], paths[1]
            # Try to get from single quotes
            paths = re.findall(r"\'(.+?)\'", str)
            if len(paths) == 2: return paths[0], paths[1]
        # Error
        return None, None

    # ==================================================================================================================
    # UNICODE STRINGS UTILS
    # ==================================================================================================================
    @staticmethod
    def to_unicode_str(obj, encoding='utf-8'):
        """Checks if obj is a string and converts if not."""
        if not isinstance(obj, basestring):
            obj = str(obj)
        obj = Utils.to_unicode(obj, encoding)
        return obj

    @staticmethod
    def to_unicode(obj, encoding='utf-8'):
        """Checks if obj is a unicode string and converts if not."""
        if isinstance(obj, basestring):
            if not isinstance(obj, unicode):
                obj = unicode(obj, encoding)
        return obj

    @staticmethod
    def regex_escape_str(str):
        """Make the string regex-ready by escaping it."""
        return re.escape(str)

    # ==================================================================================================================
    #  SSH UTILS
    # ==================================================================================================================
    @staticmethod
    def cmd_block(client, cmd):
        print 'remote shell:', cmd
        stdin, out, err = client.exec_command(cmd)
        if type(out) is tuple: out = out[0]
        str = ''
        for line in out:
            str += line
        return str

    @staticmethod
    def sftp_get(ip, port, username, password, remote_file, local_path):
        # -----set up sftp to get decrypted ipa file-----
        t = paramiko.Transport(ip, port)
        t.connect(username=username, password=password)
        print '{} -> {}'.format(remote_file, local_path)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(remote_file,local_path)

    # @staticmethod
    # def sftp_get_files(ip, port, username, password, remote_files, local_dir):
    #     t = paramiko.Transport(ip, port)
    #     t.connect(username=username, password=password)
    #     sftp = paramiko.SFTPClient.from_transport(t)
    #     for file in remote_files:
    #         sftp.get(remote_file, local_path)

    @staticmethod
    def get_dataprotection(filelist):
        """Get the Data Protection of the files contained in 'filelist'."""
        computed = []
        for el in filelist:
            if el:
                fname = Utils.escape_path(el.strip())
                dp = '{bin} -f {fname}'.format(bin=data.DEVICE_TOOLS['FILEDP'], fname=fname)
                dp += ' 2>&1'                                            # needed because by default FileDP prints to STDERR
                res = Utils.cmd_block(data.client, dp).split("\n")
                # Parse class
                cl = res[0].rsplit(None, 1)[-1]
                computed.append((fname, cl))
        return computed

    @staticmethod
    def openurl(url):
        cmd = '{uiopen} {u}'.format(uiopen=data.DEVICE_TOOLS['UIOPEN'], u=url)
        Utils.cmd_block(data.client, cmd)

    @staticmethod
    def kill_by_name(bin_name):
        cmd = 'killall -9 {}'.format(bin_name)
        Utils.cmd_block(data.client, cmd)

    @staticmethod
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
            i += 1

        # data.app_dict = app_options
        data.app_dict = app_dict

        app_id = int(raw_input("plz choose which app to analyse: "))
        print 'you have choose [', app_id, ']', app_options[app_id]
        data.app_bundleID = app_options[app_id]

