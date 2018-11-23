# coding:utf-8

import logging
import os, sys
# from config import config
# path = os.getcwd().split("/project")[0]+'/logs'
path = sys.argv[0].split("/project")[0]+'/logs'

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    filename= path + '/NotebookServer.log',
                    # filename= config.logpath,
                    filemode='w')
logger = logging.getLogger("NBLogger")

isDebug = True


def log(tag, msg):
    if isDebug:
        try:
            log = "nbLOG: " + tag + " | " + str(msg)
            print(log)
            logging.log(log)
        except Exception as e:
            print('Exception:'+str(e))
            logging.error(str(e))


def err(tag, err):
    if isDebug:
        try:
            log = "nbERROR: " + tag + " | " + str(err)
            print(log)
            logging.debug(log)
        except Exception as e:
            print('Exception:'+str(e))
            logging.error(str(e))


def info(tag, msg):
    if isDebug:
        try:
            log = "nbINFO: " + tag + " | " + str(msg)
            print(log)
            logging.info(log)
        except Exception as e:
            print('Exception:'+str(e))
            logging.error(str(e))
