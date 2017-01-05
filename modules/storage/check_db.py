import paramiko
import os
import sqlite3

import config
import data


class Checker:

    def __init__(self,files):
        print files
        self.files = files
        self.black_list = data.input_list
        self.read_txt()
        self.results=dict()

    def read_txt(self):
        file = open('./config/sensitive.txt')
        lines = file.readlines()
        for line in lines:
            line = line.strip('\n')
            self.black_list.append(line)

    def start_check(self):
        # sftp to local
        # connect to phone for sftp
        t = paramiko.Transport(config.mobile_ip, config.ssh_port)
        t.connect(username=config.mobile_user, password=config.mobile_password)
        sftp = paramiko.SFTPClient.from_transport(t)
        count =0
        for file in self.files:
            print 'getting db file ',file,' from iPhone.'
            sep = os.path.sep
            file_name = '{}_{}'.format(os.path.basename(file),count)
            local_file_path = './temp/{}/files/{}'.format(data.start_time,file_name)
            sftp.get(file, local_file_path)
            print 'got the db file: ',local_file_path
            print 'start check'
            self.read_db(local_file_path)
            count+=1
        print 'db file check DONE!'
        t.close()

    def read_db(self,file):
        conn = sqlite3.connect(file)
        c = conn.cursor()
        # get all tables
        c.execute("select name from sqlite_master where type='table' order by name")
        tables=c.fetchall()
        print tables
        for table in tables:
            query = 'select * from '+table[0]
            c.execute(query)
            print query
            for row in c:
                self.check_row(row,file,table)
        conn.close()

    def check_row(self,row,file,table):
        for i in range(len(row)):
            for black_item in self.black_list:
                if black_item in str(row[i]):
                    self.results[file] = (table,row)
                    return

# c = Checker()
# c.read_db('/Users/konghaohao/Desktop/CoreData.sqlite')