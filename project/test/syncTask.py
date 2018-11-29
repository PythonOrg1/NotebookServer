import threading
import time
def onProcess(id, p):
    print('onProcess id='+str(id) + ' p='+str(p))

def test(ids, onProcess):
    print('test')
    for id in ids:
        print("index: " + str(ids.index(id)))
        onProcess(id, id/len(ids))
        time.sleep(0.1)

if __name__ == '__main__':
    test([1,2,3,4], onProcess)