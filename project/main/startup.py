# charset=utf-8

from base import sysout
from config import config, string
from server import httpServer
from manager import fileManager
import threading
import asyncio

TAG = "NotebookServer"

warning = '\n ---- ' \
          '\n System Warning:\n ' \
          '---- \n ' \
          'Before u start the NotebookServer, u have to make sure that u have already installed the module "Jupyter Notebook"! \n' + \
          " Even though, there'll be some error when u use it !! \n" \
          " ---- ---- ---- ---- \n"
Warning = "\033[0;37;43m" + warning + "\033[0m"


def initConfig():
    config.initConfig()
    sysout.info('', "\033[0;37;43m" + warning + "\033[0m")


def startHttpServer():
    httpServer.run()

    # t = threading.Thread(target=httpServer.run(), name='NotebookHttpServer')
    # thread.start()
    # thread.join()
    # fileManager.getFileNumber('/Users/jerryyin/workspace/notebook', True)
    # print(fileManager.getDirNumber('/Users/jerryyin/workspace/notebook', True))

    # notebookServer = httpServer.NotebookHttpServer(threadId=1, name='NotebookHttpServer')
    # notebookServer.start()
    # notebookServer.join()


def startWebsocket():
    from server import websocketServer
    websocketServer.run()
    # ws_server = websocketServer.webSocketServer(threadId=2, name='nbWsServer', loop=asyncio.new_event_loop())
    # ws_server.start()
    # ws_server.join()


if __name__ == '__main__':
    initConfig()
    # startWebsocket()
    # startHttpServer()

    pool = []
    pool.append(httpServer.NotebookHttpServer(threadId=1, name='NotebookHttpServer', loop=asyncio.new_event_loop()))
    from server import websocketServer
    pool.append(websocketServer.webSocketServer(threadId=2, name='nbWsServer', loop=asyncio.new_event_loop()))
    for t in pool:
        t.start()
        # t.join()
