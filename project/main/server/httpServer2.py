#!/usr/bin/env python
# -*- coding: utf-8 -*-

from project.main.base import sysout

from http.server import BaseHTTPRequestHandler, HTTPServer
# from wsgiref.simple_server import make_server
import json


TAG = 'httpServer2'

mPort = 8100
mHost = '127.0.0.1'
# mHostAmi = '207.148.97.99'

mServer = (mHost, mPort)


#
class NotebookHTTPServer(BaseHTTPRequestHandler):
    #GET
    def get(self):
        reply = False
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 0, 'result': 'bad request 40004'}))


def saveEmail(email):
    response = ''
    # sql = 'INSERT INTO '+confDb.tbUser +'('+confDb.rowEmail + ") VALUES ('"+email +"')"
    # done = amDbUtil.saveData(sql)
    # if done:
    #     response = {'status': '1', 'result': '操作成功！'}
    # else:
    #     response = {'status': '0', 'result': '信息存储失败!'}
    return response



def praseData(request_body):
    print(request_body)
    # action = request_body['action']
    # sysout.info(TAG, 'action='+str(action))
    # if action == 'save_email':
    #     #save email request
    #     return saveEmail(request_body['email'])
    # else:
    #     # pass
    #     return {'status': '0', 'result': 'bad request 40004'}
    return {'status': 0, 'result': 'bad request 40004'}

#server
def application(environ, start_response):
    # 定义请求的类型和当前请求成功的code
    start_response('200 OK', [('Content-Type', 'application/json')])
    # environ是当前请求的所有数据，包括Header和URL，body
    request_body = environ["wsgi.input"].read(int(environ.get("CONTENT_LENGTH", 0))).decode('utf-8')
    sysout.info(TAG, 'request: '+str(request_body))
    # request_body = json.loads(request_body)
    response = praseData(request_body)
    return [json.dumps(response)]
    # return response


def run():
    httpd = HTTPServer(mServer, NotebookHTTPServer)
    # httpd = make_server(mHost, mPort, application)
    sysout.info(TAG, 'http server is running on ' + str(mServer))
    # httpd = NotebookHTTPServer(mServer)
    httpd.serve_forever()

run()