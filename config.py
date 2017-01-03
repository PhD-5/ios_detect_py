import ConfigParser

print 'config begin...'
config = ConfigParser.SafeConfigParser()
config.read("./config/para_config.conf")

mobile_ip = config.get('mobile','mobile_ip')
mobile_user = config.get('mobile','mobile_user')
mobile_password = config.get('mobile','mobile_password')

omp_ip = config.get('omp','omp_ip')
omp_user = config.get('omp','omp_ip')
omp_password = config.get('omp','omp_ip')

server_ip = config.get('server','server_ip')
server_user = config.get('server','server_user')
server_password = config.get('server','server_password')

ssh_port = config.get('ssh','ssh_port')

socket_ip = config.get('socket','socket_ip')
socket_port = config.get('socket','socket_port')

respring_wait = config.get('other','respring_wait')

print 'config end...'

class c:
    def read_file(self):
        ssh_port