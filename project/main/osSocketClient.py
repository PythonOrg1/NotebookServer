import time
from websocket import create_connection
import _thread as threading

svr_addr = 'cloudolize.cn:8001'
# svr_addr = 'cloudyotech.com:8002'
ws_server = 'ws://'+svr_addr+"/osm_server/"
svr_port = '8001'

# svr_addr = '18.18.24.24:8002'
# ws_server = 'ws://'+svr_addr+"/osm_server/"
# ws_server = 'ws://'+svr_addr

# svr_addr = '120.26.57.100:8001'
# svr_addr = '127.0.0.1:8002'
# ws_server = 'wss://'+svr_addr+"/osm_server/"

# svr_addr = '127.0.0.1:8001'
# ws_server = 'ws://127.0.0.1:8002'
# ws_server = 'ws://0.0.0.0:8002'
# ws_server = 'ws://localhost:8002'
# ws_server = 'ws://192.168.188.176:8002'



msg_check = "check"
res_check_success = "check_success"
msg_cmd = "cmd_"
msg_close = "close"

class SocketClient(object):

    def __init__(self, addr):
        print("create... "+ addr)
        self.socket = create_connection(addr)
        print(self.socket)
        self.isConnect = True
        print(addr+" has connected.")

    def sendMessage(self, msg):
        self.socket.send(msg.encode("utf-8"))
        print("send msg: "+msg)
        return self.socket.recv()

    def isServerAvailable(self):
        res = self.sendMessage(msg_check)
        if res == res_check_success:
            return True
        else:
            return False

    #t --- 超时时长（s）
    def setConnectTimeOut(self, t):
        i = 0
        while i < t:
            time.sleep(1)
            i = i + 1




    def close(self):
        if self.isConnect:
            self.socket.send(msg_close)
            print("socket.close..")
            # self.socket.close()
            self.socket = None
            print("socket.close runed")
            self.isConnect = False
            print("socket.close is not connect")

#
# def searchServer():
#     return ['www.cloudolize.cn', 'www.cloudyotech.com', '2.1.3', '2.2', '2.3.1']


def connectSocketServer(server_addr):
    print("start connecting...")
    isConnected = False
    ws ='ws://'+server_addr+':'+svr_port+"/osm_server/"
    socket = SocketClient(ws)
    result = socket.sendMessage(msg_check)
    print("check result: " + result)
    if result == res_check_success:
        isConnected = True
    return (socket, isConnected)


def testConnect():
    print("start...")
    socket = SocketClient(ws_server)
    result = socket.sendMessage(msg_check)
    print("result: " + result)

    res = socket.sendMessage("cmd_tail -f /usr/local/tomcat8/logs/catalina.out")
    # tmp = ""
    # while socket.isConnect:
    #     if res != tmp:
    #         print(str(res))
    #         tmp = res
    while socket.isConnect:
        result = socket.socket.recv()
        print(result)
        return result

    # socket.close()
