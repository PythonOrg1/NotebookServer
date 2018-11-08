#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import socketserver

baseHome = ''

class FileTransportServer(socketserver.BaseRequestHandler):

    def upload(self):
        conn = self.request
        s = str(conn.recv(1024), encoding='utf-8')
        fileName, fileSize = s.split('&&')
        newFileName = os.path.join(baseHome, fileName)
        if fileName in baseHome :
            #file already exists
            recvdSize = os.stat(baseHome).st_size  #calculate temp file size

            conn.sendall(bytes(recvdSize, encoding='utf-8'))  # process

            with open(newFileName, 'ab') as f:
                data = conn.recv(1024)
                f.write(data)
                recvdSize += len(data)

            # if recvdSize < int(fileSize):
            #     # continue upload


        else:
            #new upload
            recvdSize = 0
            # conn.sendall(bytes()) #reply
            with open(newFileName) as f:
                data = conn.recv(1024)
                f.write(data)
                recvdSize += len(data)



    def download(self):
        pass
