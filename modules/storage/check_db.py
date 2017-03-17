import paramiko
import os
import sqlite3
import signal
from Utils import Utils
import config
import data


class Checker:

    def __init__(self, files):
        # print files
        self.files = files
        self.input_list = list(data.input_list)

        self.txt_list = list()
        self.read_txt()

        self.keyiv_list = list()
        self.get_key_iv()

        self.results = dict()
        self.input_results = dict()
        self.keyiv_results = dict()
        self.txt_results = dict()

        self.cur_db = ''
        self.cur_table = ''

    def read_txt(self):
        file = open('./config/sensitive.txt')
        lines = file.readlines()
        for line in lines:
            line = line.strip('\n')
            self.txt_list.append(line)

    def get_key_iv(self):
        json_list = data.dynamic_json.cccrtpy_json_list
        if json_list:
            for json in json_list:
                if "key" in json and json["key"] != "":
                    self.keyiv_list.append(json["key"])
                if "iv" in json and json["iv"] != "":
                    self.keyiv_list.append(json["iv"])

    def start_check(self):
        # sftp to local
        # connect to phone for sftp
        t = paramiko.Transport(config.mobile_ip, config.ssh_port)
        t.connect(username=config.mobile_user, password=config.mobile_password)
        sftp = paramiko.SFTPClient.from_transport(t)
        count = 0
        for file in self.files:
            self.cur_db = file
            file_name = '{}_{}'.format(os.path.basename(file), count)
            local_file_path = './temp/{}/files/{}'.format(data.start_time, file_name)
            sftp.get(file, local_file_path)
            try:
                signal.signal(signal.SIGALRM, self.my_handler)
                signal.alarm(60*2)
                self.read_db(local_file_path)
                signal.alarm(0)
            except AssertionError:
                # print 'time_out:', file
                Utils.printy_result('Download db files from app', 0)
            count += 1
        self.results["input"] = self.input_results
        self.results["keyiv"] = self.keyiv_results
        self.results["txt"]   = self.txt_results

        Utils.printy_result('Database Check.', 1)
        t.close()

    def read_db(self, file):
        conn = sqlite3.connect(file)
        c = conn.cursor()
        # get all tables
        c.execute("select name from sqlite_master where type='table' order by name")
        tables = c.fetchall()
        for table in tables:
            self.cur_table = table[0]
            query = 'select * from ' + table[0]
            c.execute(query)
            for row in c:
                self.check_row(row)
        conn.close()

    def check_row(self, row):
        for i in range(len(row)):
            for black_item in self.input_list:
                try:
                    if black_item in str(row[i]):
                        if self.cur_db not in self.input_results:
                            self.input_results[self.cur_db] = []
                        info = (self.cur_table, str(row), black_item)
                        self.input_results[self.cur_db].append(info)
                except:
                    # print 'read row errer,', row
                    Utils.printy_result('READ ROW FROM DB ERROE', 0)
            for black_item in self.keyiv_list:
                try:
                    if black_item in str(row[i]):
                        if self.cur_db not in self.keyiv_results:
                            self.keyiv_results[self.cur_db] = []
                        info = (self.cur_table, str(row), black_item)
                        self.keyiv_results[self.cur_db].append(info)
                except:
                    # print 'read row errer,', row
                    Utils.printy_result('READ ROW FROM DB ERROE', 0)
            for black_item in self.txt_list:
                try:
                    if black_item in str(row[i]):
                        if self.cur_db not in self.txt_results:
                            self.txt_results[self.cur_db] = []
                        info = (self.cur_table, str(row), black_item)
                        self.txt_results[self.cur_db].append(info)
                except:
                    # print 'read row errer,', row
                    Utils.printy_result('READ ROW FROM DB ERROE', 0)

    def my_handler(self, signum, frame):
        raise AssertionError