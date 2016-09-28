import paramiko

def cmd_block(client,cmd):
    print 'remote shell:',cmd
    stdin, out, err = client.exec_command(cmd)
    if type(out) is tuple: out = out[0]
    str = ''
    for line in out:
        str+=line
    return str



def sftp_get(ip,port,username,password,remote_file, local_path):
    # -----set up sftp to get decrypted ipa file-----
    t = paramiko.Transport(ip, port)
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.get(remote_file, local_path)
    t.close()