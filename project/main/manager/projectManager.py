# charset=utf-8

from base import sysout
from config import config, string
from manager import fileManager, vmManager
from system import shell
from hashlib import md5
import os
import json
import threading, time

TAG = "projectManager"

# response of error message
resp_err_version_invlid = {'status': 0, 'result': 'incorrect version number!'}
resp_err_version_old_err = {'status': 0, 'result': 'current project is not exists!'}
resp_err_version_create_dir_err = {'status': 0, 'result': 'system error on create new directory!'}


#
# public check method
#
def checkClassUsrPj(userId, classId, pjIds):
    pathClass = config.dir_pub_class + '/' + str(classId)
    print(pathClass)
    if classId == None or not os.path.exists(pathClass):
        return {
            'status': 0,
            'result': 'No such Class, please check the path!'
        }
    numPjs = fileManager.getDirNumber2(pathClass)
    # size have to same
    if not numPjs == str(len(pjIds)):
        return {
            'status': 0,
            'result': 'Class and Project Size error! ' + str(numPjs) + ' projects in class but ' + str(
                len(pjIds)) + ' project ids.'
        }
    pathUser = config.dir_home + '/' + str(userId)
    if not os.path.exists(pathUser):
        return {
            'status': 0,
            'result': "No such user, please check again!"
        }
    # success checked
    return None


#
# check the version of pj is exists?
#
def checkVersion(userId, projectId, v):
    if v == None:
        return (False, resp_err_version_invlid)
    maxVersion = int(fileManager.getDirNumber2(
        config.dir_home + config.dir_home_user + '/' + str(userId) + '/system/' + str(projectId) + '/'))
    if (v <= 0 or v > maxVersion):
        return (False, resp_err_version_invlid)
    return (True, maxVersion)


# create user's project
#
# projectType -- 'PYTHON3' | 'PYTHON2' | 'R'
#
def createPreProject(userId, projectId, projectName, projectType):
    userHome = ''
    pjHome = ''
    dirData = ''
    if config.dir_home_user != "":
        userHome = config.dir_home + "/" + config.dir_home_user + '/' + str(userId)
    else:
        userHome = config.dir_home + '/' + str(userId)
    pjHome = userHome + '/system'
    if not os.path.exists(pjHome):
        os.makedirs(pjHome)
        shell.execute('cp ' + config.file_system_readme + ' ' + pjHome + '/')

    # create directory for users's dataSets
    pathDsets = config.dir_home + "/" + config.dir_home_user + '/' + str(userId) + '/system/datasets'
    if not os.path.exists(pathDsets):
        os.makedirs(pathDsets)

    dirData = userHome + '/数据集'
    if not os.path.exists(dirData):
        os.makedirs(dirData)
        shell.execute('ln -s ' + pathDsets + '/* ' + dirData + '/')

    path = config.dir_home_user + '/' + str(userId) + '/system/' + str(
        projectId) + '/1'  # 1--version of pj， vesionInit=1
    dir = config.dir_home + path
    if (fileManager.createDir(dir)):
        notebook = fileManager.createProject(dir, projectId, projectName, projectType, path)
        sysout.log(TAG, "first project = " + str(notebook))
        return notebook
    return 'System can not create user dir of -- ' + dir


#
# versionCur -- version of current project
#       Attention: current version maybte != the most new version ,
#       cause user can checkout to any history version then edit and create new version !
#
#
def createNewVersion(userId, projectId, projectName, versionCur):
    (exist, result) = checkVersion(userId, projectId, versionCur)
    if not exist:
        return result
    maxVersion = result
    curPath = config.dir_home_user + '/' + str(userId) + '/system/' + str(projectId) + '/' + str(versionCur)
    curNb = config.dir_home + curPath + '/' + config.getNotebookName()
    curH5 = config.dir_home + curPath + '/' + config.getH5Name()
    curPY = config.dir_home + curPath + '/' + config.getPYName()

    version = maxVersion + 1
    path = config.dir_home_user + '/' + str(userId) + '/system/' + str(projectId) + '/' + str(version)
    dir = config.dir_home + path
    if (fileManager.createDir(dir)):
        print(config.dir_home + curPath)
        if not os.path.exists(config.dir_home + curPath):
            return resp_err_version_old_err
        else:
            # cmd = 'cp / notebook / storage / 416 / system / 35 / 15 / edit.ipynb / notebook / storage / storage / 416 / system / 35 / 26 /'
            shell.execute('cp ' + curNb + ' ' + dir + '/')
            shell.execute('cp ' + curH5 + ' ' + dir + '/')
            shell.execute('cp ' + curPY + ' ' + dir + '/')
            # shell.execute('cp -r ' + config.dir_home + curPath + '/dataset' + ' ' + dir + '/')
            shell.execute('cp  ~/.jupyter/custom/custom.css ' + dir + '/')
            return {
                'projectId': projectId,
                'projectName': projectName,
                'version': version,
                'notebook': config.ns_doname + '/notebooks/storage' + path + '/' + config.getNotebookName(),
                'html': config.ns_doname + '/notebooks/storage' + path + '/' + config.getH5Name(),
                'py': config.ns_doname + '/notebooks/storage' + path + '/' + config.getPYName()
            }
    else:
        return resp_err_version_create_dir_err


def runWithVm(userId, projectId, projectName, version, vmId, passwd, isoName, isoRemarks, gpu, cpu, memory,
              action='start', pstartTime=None, pendTime=None):
    res = None
    # if action != None and action == 'stop':
    #     # shutdown vm
    #     res = vmManager.startVm(userId, isoName, vmId, passwd, gpu, cpu, memory, isoRemarks, action, pstartTime, pendTime)
    # else:
    #     # run vm
    res = vmManager.startVm(userId, isoName, vmId, passwd, gpu, cpu, memory, isoRemarks, action, pstartTime, pendTime)
    if res['status'] == 1:
        # start vm success
        # {
        #  'status': 1,
        #  'result': {
        #     'jupyeter': 'http://'],
        #     'message': (result['result'])['message']
        #  }
        # }
        path = res['result'].get('jupyter', '') + '/notebooks/system/' + str(projectId) + '/' + str(version)
        parentPath = config.dir_home + '/' + str(userId) + '/system/' + str(projectId) + '/' + str(version)
        notebook = path + '/' + fileManager.getOneNbFileName(parentPath, '.ipynb')
        html = path + '/' + fileManager.getOneNbFileName(parentPath, '.html')
        py = path + '/' + fileManager.getOneNbFileName(parentPath, '.py')

        result = {
            'status': 1,
            'result': {
                'projectId': projectId,
                'projectName': projectName,
                'version': version,
                'notebook': notebook,
                'html': html,
                'py': py
            }
        }
        # sysout.log(TAG, json.loads(result))
        return result

    else:
        # 'status' == 0
        sysout.log(TAG, res)
        return res


#
# delete project by user
#
def delectProject(userId, pjId, pjName):
    projectPath = config.dir_home + config.dir_home_user + '/' + str(userId) + '/system/' + str(pjId) + '/'
    return fileManager.deleteFile(projectPath)


#
# bind dataset with project
# isUnbind = True --> unbind dataset
#
def bindDataWithProject(userId, projectId, version, dataIds, isUbind=False):
    if not isUbind:
        # bind dataset
        paths = []
        for i in range(len(dataIds)):
            pathPj = ""
            pathDset = ""
            if config.dir_home_user != '':
                pathPj = config.dir_home + config.dir_home_user + '/' + str(userId) + '/system/' + str(
                    projectId) + '/' + str(version) + '/dataset/'
                # pathDset = config.dir_home + config.dir_home_user + '/' + str(userId) + '/system/datasets/' + str(dataIds[i])
            else:
                pathPj = config.dir_home + '/' + str(userId) + '/system/' + str(projectId) + '/' + str(
                    version) + '/dataset/'
                # pathDset = config.dir_home + '/' + str(userId) + '/system/datasets/' + str(dataIds[i])

            # pathPj = '/data/system/' + str(projectId) + '/' + str(version) + '/dataset/'
            pathDset = '/data/system/datasets/' + str(dataIds[i])

            if not os.path.exists(pathPj):
                os.mkdir(pathPj)
            # pathDset = config.dir_home + config.path_dataset + '/' + str(dataIds[i])
            # pathDset = config.dir_home + config.dir_home_user + '/'+str(userId) + '/system/datasets/' + str(dataIds[i])
            if not os.path.exists(pathDset):
                shell.execute('mkdir ' + pathDset)
                # return {
                #     'status' : 0,
                #     'result' : 'Dataset file not exists!'
                # }
            shell.execute('ln -s ' + pathDset + ' ' + pathPj)
            pathDsetln = 'dataset/' + str(dataIds[i]) + '/'
            paths.append(pathDsetln)

        return {
            'status': 1,
            'result': {
                'message': "dataset bind successde!",
                'path': paths
            }
        }

    else:
        # unbind dataset
        done = {}
        for i in range(len(dataIds)):
            path = ''
            path1 = ''
            if config.dir_home_user != '':
                path = config.dir_home + config.dir_home_user + '/' + str(userId) + '/system/' + str(
                    projectId) + '/' + str(version) + '/dataset/' + str(dataIds[i])
                path1 = config.dir_home + config.dir_home_user + '/' + str(userId) + '/system/' + str(
                    projectId) + '/' + str(version) + '/dataset'
            else:
                path = config.dir_home + '/' + str(userId) + '/system/' + str(projectId) + '/' + str(
                    version) + '/dataset/' + str(dataIds[i])
                path1 = config.dir_home + '/' + str(userId) + '/system/' + str(projectId) + '/' + str(
                    version) + '/dataset'

            # path = config.dir_home + config.dir_home_user + '/' + str(userId) + '/system/' + str(projectId) + '/' + str(version) + '/dataset/' + str(dataIds[i])

            haveException = False
            try:
                shell.execute('rm -r ' + path)
                # shell.execute('rm -r ' + path1)
            except Exception as e:
                sysout.err(TAG, e)
                done[str(i)] = str(e)
                havaException = True

            if not os.path.exists(path):
                # the data not binded
                # done[str(i)] = 'data hava not been binded before!'
                done[str(i)] = 1
            else:
                if not havaException:
                    done[str(i)] = "delete failed !"

        success = True
        for k in range(len(dataIds)):
            if not done[str(k)] == 1:
                success = False

        if success:
            return {
                'status': 1,
                'result': "unbind datasets success!"
            }
        else:
            return {
                'status': 0,
                'result': done
            }


def deleteDataset(userId, dataId):
    try:
        path = ''
        pathDsetFile = ''

        # first unbind dataset of all project
        if config.dir_home_user != '':
            path = config.dir_home + config.dir_home_user + '/' + str(userId) + '/system/'
            pathDsetFile = config.dir_home + config.dir_home_user + '/' + str(userId) + '/system/datasets/' + str(
                dataId)
        else:
            path = config.dir_home + '/' + str(userId) + '/system/'
            pathDsetFile = config.dir_home + '/' + str(userId) + '/system/datasets/' + str(dataId)

        content = fileManager.getAllFiles(path)
        for i in range(len(content)):
            # is project's dataset dir ? == 1. 'dataset/dataId' is in pwd   and   2. len(pwds) == 8
            files = (content[i])['files']
            pwd = (content[i])['pwd']
            if ('dataset/' + str(dataId)) in pwd:
                pwds = str(pwd).split('/')
                if len(pwds) == 8:
                    # pwd = '/notebook/storage/userId/system/projectId/version/dataset/dataId'
                    projectId = pwds[4]
                    version = pwds[5]
                    bindDataWithProject(userId, projectId, version, [dataId], True)

        # second delete file
        (code, msg) = fileManager.deleteFile(pathDsetFile)
        if code == 1:
            return {
                'status': 1,
                'result': "delete dataset success!"
            }
        else:
            return {
                'status': 0,
                'result': msg
            }
    except Exception as e:
        sysout.err(TAG, e)
        return {
            'status': 0,
            'result': "delete failed! " + e
        }


#
# @param pjVersion : default 1
#
def copyClassProject(classId, userId, pjIds):
    pathClass = config.dir_pub_class + '/' + str(classId)
    pathUser = config.dir_home + '/' + str(userId)

    check = checkClassUsrPj(userId, classId, pjIds)
    if not check == None:
        return check

    # check done, start copy
    pjIdsInClass = os.listdir(pathClass)  # normal: only have directories of all projects
    projects = []
    for i in range(len(pjIds)):
        version = 1  # default project version = 1
        pathPj = pathUser + '/system/' + str(pjIds[i]) + '/' + str(version)
        nbFileName = fileManager.getOneNbFileName(pathClass + '/' + pjIdsInClass[i], '.ipynb')
        fileName = str(nbFileName).split('.ipynb')[0]
        try:
            if not os.path.exists(pathPj):
                os.makedirs(pathPj)
            shell.execute('cp -r ' + pathClass + '/' + str(pjIdsInClass[i]) + '/* ' + pathPj + '/')

            fileUrl = config.ns_doname + '/notebooks/storage' + '/' + str(userId) + '/system/' + str(
                pjIds[i]) + '/' + str(version) + '/'

            projects.append({
                'fileName': fileName,
                'projectId': pjIds[i],
                'version': version,
                'notebook': fileUrl + nbFileName,
                'html': fileUrl + fileManager.getOneNbFileName(pathClass + '/' + pjIdsInClass[i], '.html'),
                'py': fileUrl + str(fileName) + '.py',  # maybe not have the .py file
                'code': 1,
                'msg': 'init project success!'
            })

        except Exception as e:
            sysout.err(TAG, str(e))
            # return {
            #     'status': 0,
            #     'result': 'Init class failed, cause ' + str(e)
            # }
            projects.append({
                'fileName': fileName,
                'projectId': pjIds[i],
                'version': version,
                'notebook': None,
                'html': None,
                'py': None,
                'code': 0,
                'msg': 'init project failed, cause ' + str(e)
            })

    return {
        'status': 1,
        'result': projects
    }


async def copyClassDatasets(userId, classId, binds, onProcess, websocket):
    pathClass = config.dir_pub_class + '/' + str(classId)
    pathUser = config.dir_home + '/' + str(userId)

    if classId == None or not os.path.exists(pathClass):
        return {
            'status': 0,
            'result': 'No such Class, please check the path!'
        }
    if not os.path.exists(pathUser):
        return {
            'status': 0,
            'result': "No such user, please check again!"
        }
    if binds == None or len(binds) <= 0:
        return {
            'status': 0,
            'result': 'Params "binds" error, please check it !'
        }

    sizeTotal = 0  # datasets file size of all files
    sizeDone = 0  # done copy files size
    process = 0.00  # process
    numDsetTotal = 0
    numDsetCur = 0
    numPjCur = 0

    arr = []
    for b in binds:
        numDsetTotal += len(b['dsetIds'])
    #     for d in b['dsetIds']:
    #         if d not in arr:
    #             arr.append(d)
    # numDsetTotal = len(arr)

    print('numDsetTotal=' + str(numDsetTotal))
    for i in range(len(binds)):
        bind = binds[i]
        pjId_c = bind['classPjId']
        pjId = bind['pjId']
        version = 1
        dsetIds = bind['dsetIds']
        numPjCur = i + 1

        try:
            version = bind['version']
        except:
            sysout.log(TAG, 'Params not contains "version", default : 1 !')
            version = 1

        for d in dsetIds:
            # check data
            path_c = config.dir_pub_dsets + '/' + str(d)
            path = pathUser + '/system/datasets/' + str(d)
            print(path_c)
            print(path)
            if os.path.exists(path_c):
                print('have path_c .')
                if not os.path.exists(path):
                    print('mkdirs path_u')
                    os.makedirs(path)
                    numDsetCur = dsetIds.index(d) + 1
                    print(numDsetCur)
                    # onProcess(numDsetCur, numDsetTotal)
                    # t = threading.Thread(target=startProcessCounting(userId, classId, binds, path_c, path, numDsetCur, numDsetTotal, sizeTotal, sizeDone,websocket))
                    # t.start()
                    await startProcessCounting(userId, classId, binds,
                                               path_c, path,
                                               numDsetCur, numDsetTotal, sizeTotal, sizeDone,
                                               websocket)
                    # if numDsetCur == numDsetTotal:
                    #     #copy done
                    #     await websocket.send()
                else:
                    # if have some datas copyed before but not full datas;
                    #todo continue to copy
                    pass

        return {
            'status': 1,
            'result': 'Datasets copy successed !'
        }


#
# return the data copy process by the websocket
#
async def startProcessCounting(userId, classId, binds, path_c, path, numDsetCur, numDsetTotal, sizeTotal, sizeDone,websocket):
    sysout.info(TAG, "start copy dset " + str(numDsetCur) + '/' + str(numDsetTotal))
    process = str(numDsetCur) + '/' + str(numDsetTotal)
    # todo cal numCur = ?
    # numDsetCur = ?

    rep_proocess = {
        'userId': userId,
        'classId': classId,
        'binds': binds,
        'sizeTotal': sizeTotal,
        'sizeDone': sizeDone,
        'numDsetTotal': numDsetTotal,
        'numDsetCur': numDsetCur,
        'process': process,

    }
    print('ws_send:')
    print(rep_proocess)
    await websocket.send(json.dumps(rep_proocess))
    shell.execute('cp -r ' + path_c + '/* ' + path + '/')
    print('copy done')
    # while not websocket == None and numDsetCur <= numDsetTotal:
    #     # process = 0.00
    #     process = str(numDsetCur) + '/' + str(numDsetTotal)
    #     # todo cal numCur = ?
    #     # numDsetCur = ?
    #
    #     rep_proocess = {
    #         'userId': userId,
    #         'classId': classId,
    #         'binds': binds,
    #         'sizeTotal': sizeTotal,
    #         'sizeDone': sizeDone,
    #         'numDsetTotal': numDsetTotal,
    #         'numDsetCur': numDsetCur,
    #         'process': process,
    #
    #     }
    #     await websocket.send(json.dumps(rep_proocess))
    #
    #     if numDsetCur == numDsetTotal:
    #         break
    #     else:
    #         time.sleep(0.25)  # 1/4 of second
    #         continue


class ProcessLisener(threading.Thread):
    def __init__(self, userId, classId, binds, path_c, path, numDsetCur, numDsetTotal, sizeTotal, sizeDone, websocket):
        threading.Thread.__init__(self)
        # self.threadID = threadId
        self.name = 'nb_ws_processListener'
        self.userId = userId
        self.classId = classId
        self.binds = binds
        self.path_c = path_c
        self.path = path
        self.numDsetTotal = numDsetTotal
        self.numDseCur = numDsetCur
        self.sizeTotal = sizeTotal
        self.sizeDone = sizeDone
        self.websocket = websocket

    def run(self):
        t = threading.current_thread()
        sysout.info(TAG, 'websocketServer is stating at thread %s - %s' % (t.threadID, t.name))
        startProcessCounting(self.userId, self.classId, self.binds,
                             self.path_c, self.path, self.numDsetCur,
                             self.numDsetTotal, self.sizeTotal, self.sizeDone, self.websocket)

#
#
# cmd:path_dataset
#
# def generateCode(userId, projectId, projectName, version):
#     (exist, result) = checkVersion(userId, projectId, version)
#     if not exist:
#         return result
#     maxVersion = result


# for test
# if __name__ == '__main__':

#     print('test...')
#     runWithVm(userId='39', projectId=113, projectName='my first pj', version=1, vmId='c4851539075413000', passwd='yy123456', isoName='60.12.136.59/ocdeep/b3',
#               isoRemarks='remaraks test', gpu='geforce gtx 1070', cpu='i7-7700k', memory='16')

# res = delectProject(2, 12, 'ddd')
# print(res)
