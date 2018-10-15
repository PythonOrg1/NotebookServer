import os, sys, select
import paramiko, re
from project.main.base import sysout
from paramiko.py3compat import u

TAG = "SSH"

class SSHUser(object):

    isConnecting = False


    def __init__(self, host, port:int, usr, pwd, keyFile=None, keyPwd=None):
        global isClosed
        sysout.info(TAG, "ssh to server... ["+host+":"+str(port)+"]")
        self.client = paramiko.SSHClient()
        # key = paramiko.RSAKey.from_private_key_file(keyFile, password=keyPwd)
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 自动接受密钥, 通过公共方式进行认证 (不需要在known_hosts 文件中存在)
        self.client.connect(host, port, username=usr, password=pwd)
        isClosed = True
        sysout.info(TAG, "ssh success")


    # @return  stdin, stdout, stderr
    #   get exec result: stdout.read().decode("UTF-8")
    def executeCmd(self, cmd):
        sysout.info(TAG, "execute cmd: '"+cmd+"'")
        return self.client.exec_command(cmd)


    def invoke_shell(self, cmd):
        sysout.info(TAG, "execute cmd: '"+cmd+"'")
        channel = self.client.invoke_shell()

        readable, writeable, error = select.select([channel, sys.stdin, ], [], [], 1)


        # while not channel.recv_ready():
        #     sysout.info(TAG, "invoke is running...")
        buff = channel.recv(1024)
        x = u(buff)
        sys.stdout.write(x)
        sys.stdout.flush()
        # base_prompt = r'(>|#|\]|\$|\)) *$'
        # while(not re.search(base_prompt, buff.split('\n')[-1])):
        #     _buff = channel.recv(2048)
        #     buff += _buff
        #     print(buff)

        channel.send(cmd)

        if sys.stdin in readable :
            inp = sys.stdin.readline()
            print("inp: "+inp)
            channel.sendall(inp)


    def close(self):
        global isConnecting
        sysout.info(TAG, "ssh closed.")
        self.client.close()
        isConnecting = False



#example
def example():
    ssh = SSHUser(host='cloudyotech.com',
                      port=22,
                      usr='root',
                      pwd='Dtx700pp',
                      # pkeyFile=r'D:\key\id_rsa',  # 密钥文件
                      keyFile="/Users/jerryyin/.ssh/id_rsa")
    stdin, stdout, stderr = ssh.executeCmd('hostndsdame')

    # sysout.info(TAG, str(type(stdout)))
    # sysout.info(TAG, str(type(stdin)))
    # sysout.info(TAG, str(type(stderr)))

    # sysout.info(TAG, "out:" +stdout.read().decode('utf-8'))
    # sysout.info(TAG, "in:" +stdin.read() is None)
    # sysout.info(TAG, "err:" +stderr.read() is None)
    # stdin, stdout, stderr = ssh.executeCmd('ls')
    # sysout.info(TAG, "out:" +stdout.read().decode('utf-8'))
    # ssh.close()

# example()