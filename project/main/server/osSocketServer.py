from bottle import *
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer

from project.main.server import osShell
from threading import Thread as Thread




svr_host = "172.16.27.81"   #Test Server  www.cloudolize.cn
svr_port = 8001

msg_check = "check" # msg check server is running ?
res_check_success = "check_success" # server is running
msg_cmd = "cmd_"
msg_close = "close"

app = Bottle()
clients = set()
@app.get('/osm_server/')
def recv_websocket():
    cSocket = request.environ.get('wsgi.websocket')
    clients.add(cSocket)
    print("新增一个用户"+ str(cSocket))
    print("当前连接用户数 ：" + str(len(clients)))
    if not cSocket:
        abort(400, 'Wxcepted WebSocket request.')

    while True:
        try:
            msg = cSocket.receive()
            print("recv from user: '"+str(msg)+"'")
        except WebSocketError:
            print("WebSocketError...")
            break
        if msg:
            for c in clients:
                try:
                    #todo:  handler msg and send result to user
                    msg = str(msg)
                    if msg == msg_check:
                        # check
                        c.send(res_check_success)
                    elif msg == msg_close:
                        clients.remove(c)
                        print("removed 1 user "+str(c))
                        break
                    else:
                        # handler
                        if msg.startswith(msg_cmd):
                            #process cmd
                            cmd = msg.split(msg_cmd)[1]
                            print("cmd = ' "+cmd +"'")

                            ServerThread(c, cmd)

                        elif msg.startswith("???"):
                            # others
                            pass
                except WebSocketError:
                    print("send msg failed, the client user was losed..")
    #remove when cSocket is leave
    clients.remove(cSocket)
    print("removed 1")



# thread to handler socket clients
class ServerThread(Thread):
    def __init__(self, socket, cmd):
        Thread.__init__(self)
        self.socket = socket
        self.cmd = cmd
        self.start()

    def run(self):
        while self.socket:
            popen = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            # while c and clients.__contains__(c):
            while True:
                line = popen.stdout.readline().strip()
                print(line)
                self.socket.send(line)






if __name__ == '__main__':
    server = WSGIServer((svr_host, svr_port), app, handler_class=WebSocketHandler)
    print("os_SocketServer is running at ws://"+svr_host+":"+str(svr_port)+":/osm_server/   ...")
    server.serve_forever()