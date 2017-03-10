import data
from Utils.utils import Utils
from check_plist import Checker


class Plist():

    def __init__(self):
        self.client = data.client

    def get(self):
        dirs = [data.metadata['bundle_directory'], data.metadata['data_directory']]
        dirs_str = ' '.join(dirs)
        cmd = '{bin} {dirs_str} -type f -name "*.plist"'.format(bin=data.DEVICE_TOOLS['FIND'], dirs_str=dirs_str)
        temp = Utils.cmd_block(self.client, cmd).split("\n")
        out = []
        for file in temp:
            if file != '':
                out.append(file)
        # No files found
        if not out:
            Utils.printy("No Plist files found ", 2)
            return

        # Add data protection class
        retrieved_files = Utils.get_dataprotection(out)
        data.local_file_protection.extend(retrieved_files)

        # start check plist sensitive data
        check = Checker(out)
        check.start_check()
        data.plist_file_results = check.results
