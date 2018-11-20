
import subprocess, os, time
from base import sysout



TAG = "SHELL"


def execute(cmd):
    sysout.log(TAG, "executed: ["+ cmd +"]")
    return os.system(cmd)


# run cmd on localhost by subprocess
class SubProcessCmd(object):

    def __init__(self, cmd):
        self.popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        pid = self.popen.pid
        sysout.info(TAG, 'Popen.pid:' + str(pid))

    def getOutBuff(self):
        while True:
            line = self.popen.stdout.readline().strip()
            # 判断内容是否为空
            if line:
                return line.decode('utf-8')

    def close(self):
        self.popen.kill()

