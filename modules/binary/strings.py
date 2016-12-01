from urlparse import urlparse
import re
import data


class String():
    def __init__(self):
        self.strings = data.strings
        data.url = []

    def get_url(self):
        for s in self.strings:
            o = urlparse(s)
            if o.scheme == 'http' or o.scheme == 'https':
                if re.search('%@', o.netloc):
                    continue
                if o.netloc:
                    data.url.append(s)
                    # values = (data.metadata["uuid"], s)
                    # data.db.execute('INSERT INTO strings VALUES (?, ?)', values)
        for index, url in enumerate(data.url):
            print index, url


