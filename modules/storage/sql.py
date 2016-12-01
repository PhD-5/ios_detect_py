import data
from Utils.utils import Utils

class Sql():


    # ==================================================================================================================
    # UTILS
    # ==================================================================================================================
    def __init__(self):
        self.client = data.client

    # ==================================================================================================================
    # RUN
    # ==================================================================================================================
    def get(self):
        # Compose cmd string
        dirs = [data.metadata['bundle_directory'], data.metadata['data_directory']]
        dirs_str = ' '.join(dirs)
        cmd = '{bin} {dirs_str} -type f -name "*sql*"'.format(bin=data.DEVICE_TOOLS['FIND'], dirs_str=dirs_str)
        out = Utils.cmd_block(self.client, cmd).split("\n")

        # No files found
        if not out:
            print("No SQL files found")
            return

        # Add data protection class
        retrieved_files = Utils.get_dataprotection(out)

        for file_lable in retrieved_files:
            print file_lable[0], "protection:", file_lable[1]