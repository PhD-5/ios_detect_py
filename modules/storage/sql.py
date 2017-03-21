import data
from Utils.utils import Utils
# from check_db import Checker
from checker import Checker

class Sql():

    def __init__(self):
        self.client = data.client

    def check(self):
        files = self.get_files()
        if not files:
            Utils.printy("No SQL files found ", 2)
            return
        retrieved_files = Utils.get_dataprotection(files)
        data.local_file_protection.extend(retrieved_files)
        check = Checker(files, 'SQL')
        check.start()
        data.db_file_results = check.results
        Utils.printy_result('Database Check.', 1)

    def get_files(self):
        files = []

        dirs = [data.metadata['bundle_directory'], data.metadata['data_directory']]
        dirs_str = ' '.join(dirs)
        cmd = '{bin} {dirs_str} -type f -name "*.sqlite"'.format(bin=data.DEVICE_TOOLS['FIND'], dirs_str=dirs_str)
        temp = Utils.cmd_block(self.client, cmd).split("\n")
        cmd = '{bin} {dirs_str} -type f -name "*.db"'.format(bin=data.DEVICE_TOOLS['FIND'], dirs_str=dirs_str)
        temp.extend(Utils.cmd_block(self.client, cmd).split("\n"))

        for db in temp:
            if db != '':
                files.append(db)

        return files