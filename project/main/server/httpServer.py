#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from http.server import BaseHTTPRequestHandler, HTTPServer
from wsgiref.simple_server import make_server
import json
import threading
import asyncio

from base import sysout
from manager import projectManager
from config import config
from manager import fileManager

TAG = 'httpServer'


# global response data
resp_err_params = {'status': '0', 'result': 'request params form error!'}

global mLoop


class NotebookHttpServer(threading.Thread):
    def __init__(self, threadId, name):
        threading.Thread.__init__(self)
        self.threadID = threadId
        self.name = name

    def run(self):
        t = threading.current_thread()
        sysout.info(TAG, 'NotebookHttpServer is stating at thread %s - %s' %(t.threadID, t.name))
        run()

##
# module -- project
#
#

# action = initProject
def initProject(request_body):
    userId = None
    pjId = None
    pjName = None
    pjType = None
    try:
        userId = request_body['userId']
        pjId = request_body['projectId']
        pjName = request_body['projectName']
        pjType = request_body['projectType']
    except:
        return resp_err_params
    return {
        'status': 1,
        'result': projectManager.createPreProject(userId, pjId, pjName, pjType)
    }


# action = newVersion
def newVersion(request_body):
    userId = None
    pjId = None
    pjName = None
    version = None
    try:
        userId = request_body['userId']
        pjId = request_body['projectId']
        pjName = request_body['projectName']
        version = request_body['version']
    except:
        return resp_err_params
    result = projectManager.createNewVersion(userId, pjId, pjName, version)
    if (type(result) == type({})) and result.get('status') == 0:
        return result
    else:
        return {
            'status': 1,
            'result': result
        }


# delete project
def deleteProject(request_body):
    userId = None
    pjId = None
    version = None
    pjName = ''
    try:
        userId = request_body['userId']
        pjId = request_body['projectId']
        pjName = request_body['projectName']
    except:
        return resp_err_params
    (code, msg) = projectManager.delectProject(userId, pjId, pjName)
    status = 0
    if code == 1:
        # success
        status = 1
    return {
        "status": status,
        "result": msg
    }


def runWithVm(request_body):
    userId = None
    pjId = None
    pjName = None
    version = None
    vmId = None
    passwd = None
    isoName = None
    isoRemarks = ''
    gpu = None
    cpu = None
    memory = None
    action1 = 'start'   #default : start
    pstartTime = None
    pendTime = None
    try:
        userId = request_body['userId']
        pjId = request_body['projectId']
        pjName = request_body['projectName']
        version = request_body['version']
        vmId = request_body['vmId']
        passwd = request_body['passwd']
        isoName = request_body['isoName']
        isoRemarks = request_body['isoRemarks']
        gpu = request_body['gpu']
        cpu = request_body['cpu']
        memory = request_body['memory']

        if 'action1' in request_body:
            action1 = request_body['action1']
        if 'pstartTime' in request_body:
            pstartTime = request_body['pstartTime']
        if 'pendTime' in request_body:
            pendTime = request_body['pendTime']

    except Exception as e:
        return str(resp_err_params) + str(e)
    return projectManager.runWithVm(str(userId), str(pjId), pjName, str(version), str(vmId), passwd, isoName,
                                    isoRemarks, gpu, cpu, str(memory), action1, pstartTime, pendTime)


##
# module -- file system
#

#
# get user's all files & directories of his storage
#
def getMyFiles(request_body):
    userId = None
    try:
        userId = request_body['userId']
    except Exception as e:
        return str(resp_err_params) + str(e)

    home = config.dir_home + '/' + str(userId)
    res =  fileManager.getUserHome(home)
    return {
        "status": 1,
        "result": res
    }


def bindDataWithProject(request_body):
    userId = None
    projectId = None
    version = request_body['version']
    dataIds = None
    isUbind = False

    if request_body['action'] == 'unbindDataset':
        isUbind = True
    try:
        userId = request_body['userId']
        projectId = request_body['projectId']
        # pjName = request_body['projectName']
        version = request_body['version']
        dataIds = request_body['dataIds']
    except Exception as e:
        return str(resp_err_params) + str(e)
    if dataIds == None or len(dataIds) == 0:
        return {'status': '0', 'result': 'empty dataset!'}
    else:
        return projectManager.bindDataWithProject(userId, projectId, version, dataIds, isUbind)

def deleteDataset(request_body):
    userId = None
    dataId = None
    try:
        userId = request_body['userId']
        dataId = request_body['dataId']
    except Exception as e:
        return str(resp_err_params) + str(e)
    if dataId == None:
        return {'status': '0', 'result': 'empty dataset!'}
    else:
        return projectManager.deleteDataset(userId, dataId)

#
# get all files & dirs info of the current path
#
# @asyncio.coroutine
# async def getFilesInfoOfPath(request_body):
def getFilesInfoOfPath(request_body):
    path = None
    try:
        path = request_body['path']
    except Exception as e:
        return str(resp_err_params) + str(e)
    res = fileManager.getFilesInfoOfPath(path)
    if res == None:
        return {
            'status':0,
            'result':"File or directory not found!"
        }
    else:
        return {
            'status':1,
            'result':res
        }

#
# rename file or dir
#
def rename(request_body):
    src = None
    dst = None
    try:
        src = request_body['src']
        dst = request_body['dst']
    except Exception as e:
        return str(resp_err_params) + str(e)
    return fileManager.rename(src, dst)

#
#delete file or dir
#
def deleteFile(request_body):
    path = None
    try:
        path = request_body['path']
    except Exception as e:
        return str(resp_err_params) + str(e)
    (code, res) = fileManager.deleteFile(path)
    return {
        'status': code,
        'result': res
    }

def deleteFiles(request_body):
    paths = None
    try:
        paths = request_body['paths']
    except Exception as e:
        return str(resp_err_params) + str(e)
    if not type(paths) == type([]):
        return resp_err_params
    result = fileManager.deleteFiles(paths)
    return {
        'status': 1,
        'result': result
    }

def makeDir(request_body):
    dir = None
    try:
        dir = request_body['dir']
    except Exception as e:
        return str(resp_err_params) + str(e)
    (code, res) = fileManager.makeDir(dir)
    return {
        'status': code,
        'result': res
    }

def createFile(request_body):
    file = None
    try:
        file = request_body['file']
    except Exception as e:
        return str(resp_err_params) + str(e)
    (code, res) = fileManager.createFile(file)
    return {
        'status': code,
        'result': res
    }

def moveFile(request_body):
    file = None
    dir = None
    try:
        file = request_body['file']
        dir = request_body['dir']
    except Exception as e:
        return str(resp_err_params) + str(e)
    (code, res) = fileManager.moveFile(file, dir)
    return {
        'status': code,
        'result': res
    }


#public classes dir:
#   /notebook/storage/base/class/classIds/projectIds/version/files...
# copy class's projects and files to user's pj home
#
def copyClassProject(request_body):
    classId = None
    userId = None
    projectIds = []
    # version = 1 #default project version = 1
    try:
        userId = request_body['userId']
        classId = request_body['classId']
        projectIds = request_body['projectIds']
    except Exception as e:
        return str(resp_err_params) + str(e)
    return projectManager.copyClassProject(classId, userId, projectIds)

#public datasets dir:
#   /notebook/storage/base/datasets/dataIds
#
def copyClassDataset(request_body):
    classId = None
    #todo copy

    #todo need return on time process

#
# reset some onr or some pj in class
# 1. delete all versions
# 2. hold all versions
#
def resetClassProject(request_body):
    classId =None
    versions = []
    pjIds = []
    # todo reset project
    if(len(versions) == 0):
        #reset all pj of this class
        pass


def resetDatasets(request_body):
    dataIds = None
    # todo reset datas

    # if (isDifferent):  isDifferent == (size1 != size2 && name1s==name2s ?)
    #   reset
    # else : no

#
#
#
#
def praseData(request_body):
    if type(request_body) != type({}):
        return resp_err_params
    else:
        action = request_body['action']
        sysout.info(TAG, 'action=' + str(action))
        # functions = {
        #     'initproject': initProject(request_body),
        #     'newVersion': newVersion(request_body)
        # }
        if action == 'initProject':
            return initProject(request_body)
        elif action == 'newVersion':
            return newVersion(request_body)
        elif action == 'runWithVm':
            return runWithVm(request_body)
        elif action == 'deleteProject':
            return deleteProject(request_body)
        elif action == 'bindDataset':
            return bindDataWithProject(request_body)
        elif action == 'unbindDataset':
            return bindDataWithProject(request_body)
        elif action == 'deleteDataset':
            return deleteDataset(request_body)
        elif action == 'getMyFiles':
            return getMyFiles(request_body)
        elif action == 'getFilesInfoOfPath':
            return getFilesInfoOfPath(request_body)
            # loop = asyncio.get_event_loop()
            # task = getFilesInfoOfPath(request_body)
            # futrue = asyncio.ensure_future(task)
            # loop.run_until_complete(futrue)
            # return futrue.result()
        elif action == 'rename':
            return rename(request_body)
        elif action == 'deleteFile':
            return deleteFile(request_body)
        elif action == 'deleteFiles':
            return deleteFiles(request_body)
        elif action == 'mkdir':
            return makeDir(request_body)
        elif action == 'mkfile':
            return createFile(request_body)
        elif action == 'moveFile':
            return moveFile(request_body)

        elif action == 'initClass':
            return copyClassProject(request_body)
        else:
            return {'status': 0, 'result': 'request & params not support!!!'}

# server
def application(environ, start_response):
    # 定义请求的类型和当前请求成功的code
    # print(environ)
    # print(start_response)
    sysout.info(TAG, threading.current_thread())
    start_response('200 OK', [('Content-Type', 'application/json')])
    # environ是当前请求的所有数据，包括Header和URL，body
    request_body = None
    # request_body = environ["wsgi.input"].read(int(environ.get("CONTENT_LENGTH", 0))).decode('utf-8')
    request_body = str(environ["wsgi.input"].read(int(environ.get("CONTENT_LENGTH", 0))), 'utf-8')
    sysout.info(TAG, 'http request ---> ')
    try:
        sysout.info(TAG, str(request_body))
    except Exception as e:
        sysout.error(TAG, 'Exception:' + str(e))

    # global mLoop
    # mLoop = asyncio.get_event_loop()

    request_body = json.loads(request_body)
    response = praseData(request_body)
    try:
        sysout.info(TAG, str(response))
    except Exception as e:
        sysout.error(TAG, 'Exception:' + str(e))

    result = json.dumps(response).encode('utf-8')
    sysout.info(TAG, "http response --> " + str(result))
    return [result]


def run():
    # httpd = HTTPServer(mServer, AmiHTTPServer)
    mPort = config.ns_port_http
    mHost = config.ns_host
    mServer = (mHost, mPort)
    httpd = make_server(mHost, mPort, application)
    # sysout.info(TAG, 'http server is running on ' + str(mServer))
    sysout.info(TAG, "The server now is running on %s in [%s] mode!"%(str(mServer),config.system['mode']))
    httpd.serve_forever()
