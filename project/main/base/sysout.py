#coding:utf-8

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    filename='NotebookServer.log',
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
            print('Exception:')
            print(e)
            logging.error(str(e))

def err(tag, err):
    if isDebug:
        try:
            log = "nbERROR: " + tag + " | "+ str(err)
            print(log)
            logging.debug(log)
        except Exception as e:
            print('Exception:')
            print(e)
            logging.error(str(e))


def info(tag, msg):
    if isDebug:
        try:
            log = "nbINFO: " + tag + " | "+ str(msg)
            print(log)
            logging.info(log)
        except Exception as e:
            print('Exception:')
            print(e)
            logging.error(str(e))

