# charset=utf-8

from base import sysout
from config import config, string
from server import httpServer
from manager import fileManager

TAG = "NotebookServer"

warning = '\n ---- \n System Warning:\n ---- \n Before u start the NotebookServer, u have to make sure that u have already installed the module "Jupyter Notebook"! \n' + " Even though, there'll be some error when u use it !! \n ---- ---- ---- ---- \n"

if __name__ == '__main__':
    config.initConfig()
    sysout.info('', warning)
    httpServer.run()
    # t = threading.Thread(target=httpServer.run(), name='NotebookHttpServer')
    # thread.start()
    # thread.join()
    # fileManager.getFileNumber('/Users/jerryyin/workspace/notebook', True)
    # print(fileManager.getDirNumber('/Users/jerryyin/workspace/notebook', True))

    # notebookServer = httpServer.NotebookHttpServer(threadId=1, name='NotebookHttpServer')
    # notebookServer.start()
    # notebookServer.join()