import asyncio
import websockets
import json

params = {
    'action': 'copyData',
    'userId': 1,
    'classId': 1,
    'projectId': 10,
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
                if res['done'] == True:
                    websocket.close()
                    print('Procress to 100% Success!')
                    break
        except Exception as e:
            websocket.close()


# main
asyncio.get_event_loop().run_until_complete(hello('ws://localhost:8101'))

# while True:
#     asyncio.get_event_loop().run_until_complete(hello('ws://localhost:8765'))
