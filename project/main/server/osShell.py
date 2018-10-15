
import subprocess, os, time
# from project.main.base import sysout

TAG = "SHELL"


def execute(cmd):
    print(TAG, "executed: '"+ cmd +"'")
    return os.system(cmd)


# run cmd on localhost by subprocess
class SubProcessCmd(object):

    def __init__(self, cmd):
        self.popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        pid = self.popen.pid
        print(TAG, 'Popen.pid:' + str(pid))

    def getOutBuff(self):
        while True:
            line = self.popen.stdout.readline().strip()
            # 判断内容是否为空
            if line:
                print(TAG," "+ str(line))
                return line.encode('utf-8')

    def close(self):
        self.popen.kill()

