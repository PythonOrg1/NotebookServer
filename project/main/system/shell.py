import subprocess, os, time
import traceback
import tempfile

from base import sysout

TAG = "SHELL"


def execute(cmd):
    sysout.log(TAG, "executed: [" + cmd + "]")
    return os.system(cmd)


# run cmd on localhost by subprocess
class SubProcessCmd(object):

    def __init__(self, cmd):
        try:
            self.tmpOut = tempfile.SpooledTemporaryFile(10 * 1000)
            self.fileno = self.tmpOut.fileno()

            # self.popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            self.popen = subprocess.Popen(cmd, stdout=self.fileno, stderr=self.fileno, shell=True)

            self.popen.communicate(timeout=10)
            # self.popen.wait()
            self.tmpOut.seek(0)
            pid = self.popen.pid
            sysout.info(TAG, 'Popen.pid:' + str(pid))

        except Exception as e:
            sysout.err(TAG, str(e))

    def getOutBuff(self):
        try:
            # while True:
                #old 1
                # line = self.popen.stdout.readline().strip()

                #old2
                # line = self.tmpOut.readline().strip()
                # # 判断内容是否为空
                # if line:
                #     return line.decode('utf-8')

                #new 1
            return self.popen.returncode
        except Exception as e:
            sysout.err(TAG, str(e))
            return None

    def close(self):
        self.tmpOut.close()
        self.popen.kill()



