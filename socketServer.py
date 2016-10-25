import socket
import config

def start_server():
    HOST = config.iphone_ip
    PORT = config.socket_port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    while 1:
        conn, addr = s.accept()
        # print'Connected by',addr
        data = conn.recv(1024)
        data = data[0:-1]
        print data
        if data == 'DONE':
            print 'need close'
            break
    conn.close()
