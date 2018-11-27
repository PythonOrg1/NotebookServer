import asyncio
import websockets
import websocket
import json
import time
import threading

from base import sysout
from config import config

TAG = 'webSocketServer'

#
# init config
#
with open("config/ws_conf.json", 'r') as conf:
    global load_dict
    load_dict = json.load(conf)

sysout.info(TAG, 'init ws config...  ')
sysout.info(TAG, str(load_dict))
host = load_dict['ws_host']
port = load_dict['ws_port']
conf.close()
sysout.info(TAG, "init ws config done, ws_host = " + str((host, port)))


class webSocketServer(threading.Thread):

    def __init__(self, threadId, name, loop):
        threading.Thread.__init__(self)
        self.threadID = threadId
        self.name = name
        self.loop = loop

    def run(self):
        t = threading.current_thread()
        sysout.info(TAG, 'websocketServer is stating at thread %s - %s' % (t.threadID, t.name))
        run(self.loop)


#
# main func
#
async def onServer(websocket, path):
    sysout.info(TAG, "ws is start running... ")
    requests = await websocket.recv()
    print("< {}".format(requests))
    print(type(requests))
    requests = json.loads(requests)
    print(type(requests))

    if not requests == None and requests['action'] == 'copyData':
        print('copyData')
        for i in range(101):
            done = i == 100
            resp = {
                'process': str((i / 100) * 100) + '%',
                'done': done
            }
            print(resp)
            await websocket.send(json.dumps(resp))
            if done:
                websocket.close()
                break
            time.sleep(0.05)

    else:
        msg_err = 'Request [' + requests + '] is not not allowed!'
        resp = {
            'status': 0,
            'result': msg_err
        }
        await websocket.send(json.dumps(resp))
        websocket.close()


def run(loop):
    # asyncio.get_event_loop_policy().set_event_loop(loop)
    asyncio.set_event_loop(loop)

    start_server = websockets.serve(onServer, host, port)
    sysout.info(TAG, "\033[22;32;40m【200 SUCCESS】\033[0m" + "The ws_server is now running on %s in [%s] mode!" % (
    str((host, port)), config.system['mode']))
    loop.run_until_complete(start_server)
    loop.run_forever()
