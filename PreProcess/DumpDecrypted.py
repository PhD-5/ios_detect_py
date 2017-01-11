from Utils.utils import Utils
import data
import config
import os

def dump_binary():
    target_doc_path = data.metadata['data_directory']+'/Documents'
    target_doc_file = target_doc_path+'/dumpdecrypted.dylib'
    Utils.sftp_put(ip=config.mobile_ip, port=config.ssh_port,
                   username=config.mobile_user, password=config.mobile_password,
                   remote_path=target_doc_file,
                   local_file='./tools/dumpdecrypted.dylib')

    target_bin_path = data.metadata['binary_path']
    dump_cmd_INSERT = 'DYLD_INSERT_LIBRARIES={} {}'.format(target_doc_file,target_bin_path)
    Utils.cmd_block(data.client, dump_cmd_INSERT)

    # get decryped file from iphone
    Utils.sftp_get(ip=config.mobile_ip, port=config.ssh_port,
                   username=config.mobile_user, password=config.mobile_password,
                   local_path='./temp/{}/binary/'.format(data.start_time)+data.metadata['binary_name'],
                   remote_file='./{}.decrypted'.format(data.metadata['binary_name']))
    data.static_file_path = os.path.abspath('.') + ('/temp/{}/binary/'.format(data.start_time)) + data.metadata[
        'binary_name']

