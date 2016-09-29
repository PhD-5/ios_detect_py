import data
from Utils.utils import Utils

class Shared_library():

    def get(self):
        self.client = data.client
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
