import os
import datetime
import time
# print(os.getcwd())

print(time.asctime( time.localtime(time.time()) ))
print(time.strftime("%Y.%m.%d-%H:%M:%S", time.localtime()))