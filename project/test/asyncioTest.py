import asyncio
import time


async def run(a):
    print('this is task for num %s' % a)
    # await caculate(a)
    res = caculate(a)
    print('task for num %s is done...' % a)
    print(res)
    return res


def caculate(a):
    i = 0
    while i < a:
        i += 1
        print(i)
        time.sleep(0.05)
    print('i=' + str(i))
    return str(i)


def callback(future):
    print('callback res= ' + str(future.result()))
    return future.result()


if __name__ == '__main__':

    # print(asyncio.iscoroutinefunction(run))
    task = run(5) #sigle task
    # futures = [asyncio.ensure_future(run(5)), asyncio.ensure_future(run(2)), asyncio.ensure_future(run(10))]
    # tasks = [run(5), run(2), run(10)]

    loop = asyncio.get_event_loop()

    try:
        ##single task
        future = asyncio.ensure_future(task)
        loop.run_until_complete(future)
        print('res=')
        print(future.result())
        # future.add_done_callback(callback)

        ##multi tasks
        # loop.run_until_complete(asyncio.wait(futures))
        # # loop.run_until_complete(asyncio.gather(tasks))
        # for t in futures:
        #     print('res=')
        #     print(t.result())
        #     print('Done after {}s'.format(time.time()))
    finally:
        loop.close()
