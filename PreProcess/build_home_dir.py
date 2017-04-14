import data
import time
import os


def build():
    start_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
    cur_workspace = os.path.abspath('.')+os.sep+'temp'+os.sep+start_time
    os.makedirs(cur_workspace+os.sep+'binary')
    os.makedirs(cur_workspace+os.sep+'report')
    os.makedirs(cur_workspace+os.sep+'files')

    data.start_time = start_time
    data.cur_workspace = cur_workspace