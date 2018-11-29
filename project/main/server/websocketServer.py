import asyncio
import websockets
import websocket
import json
import time
import threading

from base import sysout
from config import config
from manager import projectManager

TAG = 'webSocketServer'

# global response data
resp_err_params = {'status': '0', 'result': 'request params form error!'}

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

def onProcess(numCur, numTotal):
    sysout.info('ws.onProcess()', 'cur:'+str(numCur) + ' / total:'+str(numTotal))
    return (numCur, numTotal)

#
# main func
#
async def onServer(websocket, path):
    # sysout.info(TAG, "ws_server is start running... ")
    requests = await websocket.recv()
    requests = json.loads(requests)
    sysout.info(TAG, "ws_server get request >> " + str(requests))

    try:
        if requests == None:
            resp = {
                'status': 0,
                'result': 'Request body can not be empty!'
            }
            await websocket.send(json.dumps(resp))
            websocket.close()
        else:
            # praseRequest(websocket, requests)
            # copy class's datasets
            if requests['action'] == 'copyClassData':
                # copyClassData(websocket)
                await copyClassData(requests, websocket)

                # for i in range(101):
                #     done = i == 100
                #     resp = {
                #         'process': str((i / 100) * 100) + '%',
                #         'done': done
                #     }
                #     print(resp)
                #     await websocket.send(json.dumps(resp))
                #     if done:
                #         # websocket.close()
                #         break
                #     time.sleep(0.05)

            elif requests['action'] == 'xxx?':
                pass

            else:
                msg_err = 'Request [' + requests + '] is not not allowed!'
                resp = {
                    'status': 0,
                    'result': msg_err
                }
                await websocket.send(json.dumps(resp))
                # websocket.close()

    except Exception as e:
        sysout.err(TAG, "ws_server Exception: " + str(e))
    finally:
        sysout.info(TAG, "ws_connection for -- " + str(requests) + " -- is closed.")
        websocket.close()
        pass


def run(loop):
    # asyncio.get_event_loop_policy().set_event_loop(loop)
    asyncio.set_event_loop(loop)

    start_server = websockets.serve(onServer, host, port)
    sysout.info(TAG, "\033[22;32;40m【200 SUCCESS】\033[0m" + "The ws_server is now running on %s in [%s] mode!" % (
        str((host, port)), config.system['mode']))
    loop.run_until_complete(start_server)
    loop.run_forever()


# def praseRequest(websocket, requests):


async def copyClassData(request, websocket):
    await websocket.send(json.dumps({
        'tips':'starting copyClassDataset...'
    }))
    userId = None
    classId = None,
    # projectId = None
    binds = []
    try:
        userId = request['userId']
        classId = request['classId']
        # projectId = request['projectId']
        binds = request['binds']

    except Exception as e:
        sysout.err(TAG, str(e))
        return resp_err_params

    # for test
    # show the connection of project and there's datasets
    # binds = [
    #     {
    #         'classPjId': 1,  # project id of class
    #         'pjId': 100,  # user's project id
    #         'version': 1,  # version of pj; default 1
    #         'dsetIds': [100 - 1, 100 - 2, 100 - 3]  # dataset id (same both user's & class)
    #     },
    #     {
    #         'classPjId': 2,
    #         'pjId': 101,
    #         'version': 1,  # version of pj; default 1
    #         'dsetIds': [1]
    #     }
    # ]

    # projectManager.copyClassDatasets(userId, classId, binds, onProcess, websocket)
    res = await projectManager.copyClassDatasets(userId, classId, binds, onProcess, websocket)
    if not res == None:
        await websocket.send(json.dumps(res))
        if res['status'] == 0:
            websocket.close()