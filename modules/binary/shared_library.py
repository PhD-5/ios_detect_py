import data
from Utils.utils import Utils

class Shared_library():
    def __init__(self, client):
        self.client = client

    def get(self):
        cmd = '{bin} -L {app}'.format(bin=data.DEVICE_TOOLS['OTOOL'], app=data.metadata['binary_path'])
        out = Utils.cmd_block(self.client, cmd)
        if out:
            try:
                data.shared_lib = out
                return True
            except AttributeError:
                return False
        else:
            return False
