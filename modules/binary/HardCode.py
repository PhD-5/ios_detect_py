import data
import re

class HarCodeDetect:

    def __init__(self,input_list):
        self.black_list = []
        self.init_black_list_from_dynamic(input_list)
        self.init_black_list_from_txt()
        self.result = []

        self.mail_parttern = re.compile(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$')
        self.ip_parttern = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
        self.phonenumber_parttern = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
        self.url_pattern = re.compile(
         r'^(?:http|ftp)s?://' # http:// or https://
         r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
         r'localhost|' #localhost...
         r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
         r'(?::\d+)?' # optional port
         r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def init_black_list_from_dynamic(self,json_list):
        for json in json_list:
            self.black_list.append(json['iv'])
            self.black_list.append(json['key'])


    def init_black_list_from_txt(self):
        txt_file = open('./config/hardcode.txt')
        lines = txt_file.readlines()
        for line in lines:
            line = line.strip('\n')
            self.black_list.append(line)

    def start_detect(self):
        strings = ['745198699@qq.com','admin','1','2','www.baidu.com/1/1.html']
        for str in strings:
            if str in self.black_list:
                self.result.append(str)
            self.regex_match(str)

    def regex_match(self,str):
        mail_match = self.mail_parttern.search(str)
        ip_match   = self.ip_parttern.search(str)
        phone_match= self.phonenumber_parttern.search(str)
        url_match  = self.url_pattern.search(str)
        if mail_match :
            self.result.append(mail_match.group())
        if ip_match:
            self.result.append(ip_match.group())
        if phone_match:
            self.result.append(phone_match.group())
        if url_match:
            self.result.append(url_match.group())

