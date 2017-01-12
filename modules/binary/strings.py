from urlparse import urlparse
import re
import data
import sys
from Utils.utils import Utils
import commands

reload(sys)
sys.setdefaultencoding("utf-8")

class String():

    def __init__(self):
        self.strings = []
        self.urls = []

    def get_strings(self):
        # --2016.12.09--yjb--check and get string in Mach-o file
        if (len(data.strings) == 0):
            cmd_strings = 'strings {bin_file}'.format(bin_file=data.static_file_path)
            result_str = commands.getstatusoutput(cmd_strings)
            if (result_str[0] == 0):
                data.strings = result_str[1].split('\n')
                # data.strings = Utils.cmd_block(data.client, cmd_strings).split('\n')
        self.strings = data.strings
        # print "----------------strings--------------------"
        # print "strings count:", len(self.strings)
        # for s in self.strings:
        #     print s

    def get_url(self):
        url = []
        for s in self.strings:
            o = urlparse(s)
            if o.scheme == 'http' or o.scheme == 'https':
                if re.search('%@', o.netloc):
                    continue
                if o.netloc:
                    url.append(s)
                    # values = (data.metadata["uuid"], s)
                    # data.db.execute('INSERT INTO strings VALUES (?, ?)', values)
        print("----------------get_url---------------------")
        print "url count:", len(url)
        self.url = url


