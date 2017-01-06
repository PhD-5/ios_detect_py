import paramiko
import os
import sqlite3
import signal

import config
import data


class Checker:

    def __init__(self,files):
        print files
        self.files = files
        self.black_list = data.input_list
        self.read_txt()
        self.results=dict()
        self.cur_db=''
        self.cur_table=''

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
            self.cur_db = file
            print 'getting db file ',file,' from iPhone.'
            file_name = '{}_{}'.format(os.path.basename(file),count)
            local_file_path = './temp/{}/files/{}'.format(data.start_time,file_name)
            sftp.get(file, local_file_path)
            print 'got the db file: ',local_file_path
            print 'start db file check'
            # set time_out
            try:
                signal.signal(signal.SIGALRM, self.my_handler)
                signal.alarm(60*2)

                self.read_db(local_file_path)

                signal.alarm(0)
            except AssertionError:
                print 'time_out:',file

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
            self.cur_table=table[0]
            query = 'select * from '+table[0]
            c.execute(query)
            print query
            for row in c:
                self.check_row(row)
        conn.close()

    def check_row(self,row):
        for i in range(len(row)):
            for black_item in self.black_list:
                try:
                    if black_item in str(row[i]):
                        self.results[self.cur_db] = (self.cur_table,row,black_item)
                        return
                except:
                    print 'read row errer,',row

    def my_handler(self, signum, frame):
        raise AssertionError