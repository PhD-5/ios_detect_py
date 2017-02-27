import data
import time
import os


def build():
    data.start_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
    os.makedirs('./temp/{}/binary'.format(data.start_time))
    os.makedirs('./temp/{}/report'.format(data.start_time))
    os.makedirs('./temp/{}/files'.format(data.start_time))
