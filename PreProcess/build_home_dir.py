import data
import time
import os
def build():
    data.start_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
    os.makedirs('./temp/{}/binary'.format(data.start_time))
    os.makedirs('./temp/{}/report'.format(data.start_time))
    os.makedirs('./temp/{}/files'.format(data.start_time))