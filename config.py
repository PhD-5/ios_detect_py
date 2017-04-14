import ConfigParser
import os

from Utils import Utils

config = ConfigParser.SafeConfigParser()
config_path = os.path.abspath('.')+os.sep+'config'+os.sep+'para_config.conf'
print config_path
config.read(config_path)

mobile_ip = config.get('mobile', 'mobile_ip')
mobile_user = config.get('mobile', 'mobile_user')
mobile_password = config.get('mobile', 'mobile_password')

server_ip = config.get('server', 'server_ip')
server_user = config.get('server', 'server_user')
server_password = config.get('server', 'server_password')

ssh_port = config.get('ssh', 'ssh_port')

socket_ip = config.get('socket', 'socket_ip')
socket_port = config.get('socket', 'socket_port')

respring_time = config.get('other', 'respring_time')

Utils.printy('Finished configuration.', 0)

