#-*- coding:utf-8 -*-
import plistlib
import paramiko
import os
import subprocess
import signal
from Utils import Utils
import config
import data


class Checker:

    def __init__(self, files):
        self.files = files
        self.black_list = list(data.input_list)
        self.read_txt()
        self.results = dict()
        self.cur_file = ''

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
        count = 0
        for file in self.files:
            self.cur_file = file
            # print 'getting plist file ', file, ' from iPhone.'
            sep = os.path.sep
            file_name = '{}_{}'.format(os.path.basename(file), count)
            local_file_path = './temp/{}/files/{}'.format(data.start_time, file_name)
            sftp.get(file, local_file_path)
            # print 'got the plist file: ', local_file_path
            # print 'start plist check'

            try:
                signal.signal(signal.SIGALRM, self.my_handler)
                signal.alarm(60*2)

                self.parse_plist(local_file_path)

                signal.alarm(0)
            except AssertionError:
                print 'time_out:',file

            count += 1
        Utils.printy_result('Plist Check.', 1)
        t.close()

    def parse_plist(self, file):
        pl_cmd = 'plutil -convert xml1 '+file
        subprocess.call(pl_cmd, shell=True)# 防止使用plistlib解析plist文件报错
        try:
            pl = plistlib.readPlist(file)
            key_path = []
            self.parse_element(pl, key_path)
        except:
            print 'plist error'

    def parse_element(self, item, key_path):
        if isinstance(item, list):
            for each in item:
                self.parse_element(each, key_path)
        elif isinstance(item, dict):
            for key in item.keys():
                key_path.append(key)
                self.parse_element(item[key], key_path)
                key_path.remove(key)
        else:
            # print key_path, ":", item
            for black_item in self.black_list:
                if (black_item in str(key_path)) or (black_item in str(item)):
                    if self.cur_file not in self.results:
                        self.results[self.cur_file] = []
                    info = (str(key_path), str(item), black_item)
                    self.results[self.cur_file].append(info)

    def my_handler(self, signum, frame):
        raise AssertionError