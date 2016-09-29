import os
import re
import paramiko

# ======================================================================================================================
# GENERAL UTILS
# ======================================================================================================================
class Utils(object):
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
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(remote_file, local_path)
        t.close()