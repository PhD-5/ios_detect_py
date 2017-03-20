import data
from Utils.utils import Utils
# from check_plist import Checker
from checker import Checker

class Plist():

    def __init__(self):
        self.client = data.client

    def check(self):
        files = self.get_files()
        if not files:
            Utils.printy("No Plist files found ", 2)
            return

        # Add data protection class
        retrieved_files = Utils.get_dataprotection(files)
        data.local_file_protection.extend(retrieved_files)

        # start check plist sensitive data
        check = Checker(files)
        check.start('PLIST')
        data.plist_file_results = check.results
        Utils.printy_result('Plist Check.', 1)

    def get_files(self):
        files = []
        dirs = [data.metadata['bundle_directory'], data.metadata['data_directory']]
        dirs_str = ' '.join(dirs)
        cmd = '{bin} {dirs_str} -type f -name "*.plist"'.format(bin=data.DEVICE_TOOLS['FIND'], dirs_str=dirs_str)
        temp = Utils.cmd_block(self.client, cmd).split("\n")
        for f in temp:
            if f != '':
                files.append(f)
        return files