import data
from Utils.utils import Utils
from check_db import Checker


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
        # print 'dirs:',dirs
        dirs_str = ' '.join(dirs)
        # print 'dirs_str:',dirs_str
        cmd = '{bin} {dirs_str} -type f -name "*.sqlite"'.format(bin=data.DEVICE_TOOLS['FIND'], dirs_str=dirs_str)

        temp = Utils.cmd_block(self.client, cmd).split("\n")
        cmd = '{bin} {dirs_str} -type f -name "*.db"'.format(bin=data.DEVICE_TOOLS['FIND'], dirs_str=dirs_str)
        temp.extend(Utils.cmd_block(self.client, cmd).split("\n"))

        out = []
        for db in temp:
            if db != '':
                out.append(db)

        # print 'sqlite:',out
        # No files found
        if not out:
            Utils.printy("No SQL files found ", 2)
            return
        # Add data protection class
        retrieved_files = Utils.get_dataprotection(out)
        data.local_file_protection.extend(retrieved_files)
        # print "-------------------sqlite----------------------"
        # for file_lable in retrieved_files:
        #     print file_lable[0], "protection:", file_lable[1]

        # check db file for sensitive data
        check = Checker(out)
        check.start_check()
        data.db_file_results = check.results
        # print 'db result: ', check.results
