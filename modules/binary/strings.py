from urlparse import urlparse
import re
import data


class String():
    def __init__(self):
        self.strings = data.strings
        print "----------------strings--------------------"
        for s in self.strings:
            print s

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
        for u in url:
            print u


