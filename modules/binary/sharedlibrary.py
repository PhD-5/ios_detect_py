import data
from Utils.utils import Utils


class SharedLibrary():
    def __init__(self):
        self.client = data.client

    def get(self):
        cmd = '{bin} -L {app}'.format(bin=data.DEVICE_TOOLS['OTOOL'], app=data.metadata['binary_path'])
        out = Utils.cmd_block(self.client, cmd).split("\n")
        if out:
            try:
                data.shared_lib = out
                print "--------------------shared_library-------------------"
                for l in out:
                    print l
                return True
            except AttributeError:
                return False
        else:
            return False
