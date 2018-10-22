import socket
import sys
import json

from base import sysout

TAG = "socketUtils"



def connectServer(host, port):
    try:
        addr = (host, port)
        sysout.log(TAG, "connect socket server: "+str(addr))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(8)
        s.connect(addr)
        return s
    except Exception as e:
        sysout.err(TAG, e)
        return {
            'status':0,
            'result':'connect time out!'
        }


def sendSocket(host, port, params):
    try:
        s = connectServer(host, port)
        if s == None:
            return None
        s.send(params)
        print(s)
        sysout.log(TAG, "send params: " + str(params))
        resp = s.recv(1024).decode('utf-8')
        if resp != None:
    #         if type(resp) == type({}):
    #             status = resp['status']
    #             result = resp['result']
    #             s.close()
    #             if (status == '200'):
    #                 listener.onResponse(result)
    #             else:
    #                 listener.onFail(result)
            sysout.log(TAG, "response: " + str(resp))
            s.close()
            return json.loads(resp)
    except Exception as e:
        # listener.onException(s)
        sysout.err(TAG, e)
        return e

# def close(socket: socket):
#     if socket != None:
#         socket.close()
