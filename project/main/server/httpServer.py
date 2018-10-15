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
    userId = ''
    pjId = ''
    pjName = ''
    pjType = ''
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


def praseData(request_body):
    if type(request_body) != type({}):
        return resp_err_params
    else:
        action = request_body['action']
        sysout.info(TAG, 'action=' + str(action))

        if action == 'initProject':
            return initProject(request_body)
        else:
            # pass
            return {'status': 0, 'result': 'bad request 40004'}


# server
def application(environ, start_response):
    # 定义请求的类型和当前请求成功的code
    start_response('200 OK', [('Content-Type', 'application/json')])
    # environ是当前请求的所有数据，包括Header和URL，body
    request_body = environ["wsgi.input"].read(int(environ.get("CONTENT_LENGTH", 0))).decode('utf-8')
    print('http request ---> ' + str(request_body))
    request_body = json.loads(request_body)
    response = praseData(request_body)
    result = json.dumps(response).encode('utf-8')
    print("http response --> " + str(result))
    return [result]


def run():
    # httpd = HTTPServer(mServer, AmiHTTPServer)
    httpd = make_server(mHost, mPort, application)
    print('http server is running on ' + str(mServer))
    httpd.serve_forever()
