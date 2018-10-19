# charset=utf-8

from project.main.base import sysout
from project.main.config import config, string
from project.main.server import httpServer



TAG = "NotebookServer"

warning = '\n ---- \n System Warning:\n ---- \n Before u start the NotebookServer, u have to make sure that u have already installed the module "Jupyter Notebook"! \n' + " Even though, there'll be some error when u use it !! \n ---- ---- ---- ---- \n"




if __name__ == '__main__':
    print(warning)
    sysout.info("", TAG + " is starting...")
    httpServer.run()
