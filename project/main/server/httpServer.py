#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from http.server import BaseHTTPRequestHandler, HTTPServer
from wsgiref.simple_server import make_server
import json

from project.main.base import sysout
from project.main.manager import projectManager
from project.main.config import config

TAG = 'httpServer'

mPort = config.ns_port_http
mHost = config.ns_host
mServer = (mHost, mPort)

# global response data
resp_err_params = {'status': '0', 'result': 'request params form error!'}


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
    # todo delete
    userId = None
    pjId = None
    version = None
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
    except Exception as e:
        return resp_err_params + str(e)
    return projectManager.runWithVm(str(userId), str(pjId), pjName, str(version), str(vmId), passwd, isoName,
                                    isoRemarks, gpu, cpu, str(memory))


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
        else:
            return {'status': 0, 'result': 'request & params not support!!!'}


# server
def application(environ, start_response):
    # 定义请求的类型和当前请求成功的code
    start_response('200 OK', [('Content-Type', 'application/json')])
    # environ是当前请求的所有数据，包括Header和URL，body
    request_body = environ["wsgi.input"].read(int(environ.get("CONTENT_LENGTH", 0))).decode('utf-8')
    print('http request ---> ' + str(request_body))
    request_body = json.loads(request_body)
    response = praseData(request_body)
    print(response)
    result = json.dumps(response).encode('utf-8')
    print("http response --> " + str(result))
    return [result]


def run():
    # httpd = HTTPServer(mServer, AmiHTTPServer)
    httpd = make_server(mHost, mPort, application)
    print('http server is running on ' + str(mServer))
    httpd.serve_forever()
