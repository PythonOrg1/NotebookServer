#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from http.server import BaseHTTPRequestHandler, HTTPServer
from wsgiref.simple_server import make_server
import json
import threading
import _thread
import asyncio
import os
from os.path import join, getsize

from base import sysout
from manager import projectManager
from config import config
from manager import fileManager

TAG = 'httpServer'

# global response data
resp_err_params = {'status': '0', 'result': 'request params form error!'}

global mLoop


class NotebookHttpServer(threading.Thread):
    def __init__(self, threadId, name, loop):
        threading.Thread.__init__(self)
        self.threadID = threadId
        self.name = name
        self.loop = loop
        mLoop = self.loop

    def run(self):
        t = threading.current_thread()
        sysout.info(TAG, 'NotebookHttpServer is stating at thread %s - %s' % (t.threadID, t.name))
        run(self.loop)


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
    action1 = 'start'  # default : start
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
    res = fileManager.getUserHome(home)
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
            'status': 0,
            'result': "File or directory not found!"
        }
    else:
        return {
            'status': 1,
            'result': res
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
# delete file or dir
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


# public classes dir:
#   /notebook/storage/base/class/classIds/projectIds/version/files...
# copy class's projects and files to user's pj home
#
def copyClassProject(request_body):
    userId = None
    projectIds = []
    # version = 1 #default project version = 1
    try:
        userId = request_body['userId']
        projectIds = request_body['projectIds']
    except Exception as e:
        print(str(e))
        return str(resp_err_params) + str(e)
    return projectManager.copyClassProject(userId, projectIds)


# public datasets dir:
#   /notebook/storage/base/datasets/dataIds
#
def copyClassDataset(request_body):
    coursewateId = None
    projectId = None
    datasetId = None
    userId = None
    datasets = []
    # version = 1 #default project version = 1
    try:
        userId = request_body['userId']
        if ('coursewareId' in request_body.keys()):
            coursewateId = request_body['coursewareId']
        if ('projectId' in request_body.keys()):
            projectId = request_body['projectId']
        if ('datasetId' in request_body.keys()):
            datasetId = request_body['datasetId']
        datasets = request_body['datasets']
    except Exception as e:
        return str(resp_err_params) + str(e)
    # projectManager.copyClassDatasets(coursewateId,userId,datasets)
    _thread.start_new_thread( projectManager.copyClassDatasets, (coursewateId,userId,datasets,projectId,datasetId, ) )
    return {
        'status': 1,
        'result': 'start copying datasets!'
    }


#
# reset some onr or some pj in class
# 1. delete all versions
# 2. hold all versions
#
def resetClassProject(request_body):
    projets = []
    type = request_body['type']
    userId = request_body['userId']
    project = request_body['projectIds']
    projets.append(project)
    if (type == 'all'):
        # reset all pj of this class
        projectManager.delectProject(userId,project['id'],None)
    elif (type == 'one'):
        projectManager.delectProject(userId,str(project['id'])+"/1",None)
    return projectManager.copyClassProject(userId,projets)



async def getDirSize(request_body):
    userId = request_body['userId']
    home = config.dir_home + '/' + str(userId)
    # dir = '/notebook/storage/' + str(userId)
    size = 0
    size = await fileManager.getDirSize(home)
    return {
        'status': 1,
        'result': size
    }

def bindFileToDataset(request_body):
    try:
        files = request_body['files']
        dir = request_body['dir']
        userId = request_body['userId']
    except Exception as e:
        return str(resp_err_params) + str(e)
    return projectManager.bindFileToDataset(userId,files,dir)
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
        elif action == 'getDirSize':
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(getDirSize(request_body))
            # loop.close()
            # return a
            # return getDirSize(request_body, loop)
        elif action == 'copyClassProject':
            return copyClassProject(request_body)
        elif action == 'copyClassDataset':
            return copyClassDataset(request_body)
        elif action == 'resetClassProject':
            return resetClassProject(request_body)
        elif action == 'bindFileToDataset':
            return bindFileToDataset(request_body)
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


def run(loop):
    asyncio.set_event_loop(loop)

    # httpd = HTTPServer(mServer, AmiHTTPServer)
    mPort = config.ns_port_http
    mHost = config.ns_host
    mServer = (mHost, mPort)
    httpd = make_server(mHost, mPort, application)
    # sysout.info(TAG, 'http server is running on ' + str(mServer))
    sysout.info(TAG, "\033[22;32;40m【200 SUCCESS】\033[0m" + " The http_server is now running on %s in [%s] mode!" % (
    str(mServer), config.system['mode']))
    httpd.serve_forever()

    # loop.run_until_complete(httpd)
    # loop.run_until_complete(asyncio.wait(httpd))
    # loop.run_forever()