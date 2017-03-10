import data
from Utils.utils import Utils
from check_db import Checker


class Sql():

    def __init__(self):
        self.client = data.client

    def get(self):
        dirs = [data.metadata['bundle_directory'], data.metadata['data_directory']]
        dirs_str = ' '.join(dirs)
        cmd = '{bin} {dirs_str} -type f -name "*.sqlite"'.format(bin=data.DEVICE_TOOLS['FIND'], dirs_str=dirs_str)
        temp = Utils.cmd_block(self.client, cmd).split("\n")
        cmd = '{bin} {dirs_str} -type f -name "*.db"'.format(bin=data.DEVICE_TOOLS['FIND'], dirs_str=dirs_str)
        temp.extend(Utils.cmd_block(self.client, cmd).split("\n"))

        out = []
        for db in temp:
            if db != '':
                out.append(db)

        if not out:
            Utils.printy("No SQL files found ", 2)
            return
        retrieved_files = Utils.get_dataprotection(out)
        data.local_file_protection.extend(retrieved_files)

        check = Checker(out)
        check.start_check()
        data.db_file_results = check.results
