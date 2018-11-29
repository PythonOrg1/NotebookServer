import asyncio
import websockets
import json

params = {
    'action': 'copyClassData',
    'userId': 396,
    'classId': 1,
    'binds': [
        {
            'classPjId': 10,             # project id of class
            'pjId': 3,                # user's project id
            'version': 1,               # version of pj; default 1
            'dsetIds': ['sys-dset-1', 'sys-dset-2']    # dataset id (same both user's & class)
        },
        {
            'classPjId': 11,
            'pjId': 4,               # user's project id
            'version': 1,
            'dsetIds': ['sys-dset-1']
        }
    ]
}


async def hello(uri):
    async with websockets.connect(uri) as websocket:
        # print(websocket.is_alive())
        # print(websocket.isAlive())
        # print(websocket.close())
        await websocket.send(json.dumps(params))
        # res = await websocket.recv()
        # print(res)
        try:
            while True:
                res = await websocket.recv()
                res = json.loads(res)
                print(res)
                # if res['done'] == True:
                #     websocket.close()
                #     print('Procress to 100% Success!')
                #     break
        except Exception as e:
            print(e)
            websocket.close()


# main
asyncio.get_event_loop().run_until_complete(hello('ws://localhost:8101'))

# while True:
#     asyncio.get_event_loop().run_until_complete(hello('ws://localhost:8765'))
