# charset=utf-8

from base import sysout
from config import config, string
from manager import fileManager, vmManager
from system import shell
import os
import json

TAG = "projectManager"

# response of error message
resp_err_version_invlid = {'status': 0, 'result': 'incorrect version number!'}
resp_err_version_old_err = {'status': 0, 'result': 'current project is not exists!'}
resp_err_version_create_dir_err = {'status': 0, 'result': 'system error on create new directory!'}


#
# check the version of pj is exists?
#
def checkVersion(userId, projectId, v):
    if v == None:
        return (False, resp_err_version_invlid)
    maxVersion = int(fileManager.getDirNumber(
        config.dir_home + config.dir_home_user + '/' + str(userId) + '/system/' + str(projectId) + '/'))
    if (v <= 0 or v > maxVersion):
        return (False, resp_err_version_invlid)
    return (True, maxVersion)


# create user's project
#
# projectType -- 'PYTHON3' | 'PYTHON2' | 'R'
#
def createPreProject(userId, projectId, projectName, projectType):
    pjHome = ''
    if config.dir_home_user != "":
        pjHome = config.dir_home + "/" + config.dir_home_user + '/' + str(userId) + '/system'
    else:
        pjHome = config.dir_home + '/' + str(userId) + '/system'
    if not os.path.exists(pjHome):
        os.makedirs(pjHome)
        shell.execute('cp ' + config.file_system_readme + ' ' + pjHome + '/')

    #create directory for users's dataSets
    pathDsets = config.dir_home + "/" + config.dir_home_user + '/' + str(userId) + '/system/datasets'
    if not os.path.exists(pathDsets):
        os.makedirs(pathDsets)

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
            shell.execute('cp ' + curNb + ' ' + dir + '/')
            shell.execute('cp ' + curH5 + ' ' + dir + '/')
            shell.execute('cp ' + curPY + ' ' + dir + '/')
            return {
                'projectId': projectId,
                'projectName': projectName,
                'version': version,
                'notebook': config.ns_doname + '/notebooks' + path + '/' + config.getNotebookName(),
                'html': config.ns_doname + '/notebooks' + path + '/' + config.getH5Name(),
                'py': config.ns_doname + '/notebooks' + path + '/' + config.getPYName()
            }
    else:
        return resp_err_version_create_dir_err


def runWithVm(userId, projectId, projectName, version, vmId, passwd, isoName, isoRemarks, gpu, cpu, memory,
              action='start', pstartTime = None, pendTime = None):
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
def bindDataWithProject(userId, projectId, version, dataIds, isUbind = False):
    if not isUbind:
        #bind dataset
        paths = []
        for i in range(len(dataIds)):
            pathPj = config.dir_home + config.dir_home_user + '/' + str(userId) + '/system/' + str(projectId) + '/' + str(version) + '/dataset/'
            if not os.path.exists(pathPj):
                os.mkdir(pathPj)
            # pathDset = config.dir_home + config.path_dataset + '/' + str(dataIds[i])
            pathDset = config.dir_home + "/" + config.dir_home_user + '/'+str(userId) + '/system/datasets/' + str(dataIds[i])
            if not os.path.exists(pathDset):
                return {
                    'status' : 0,
                    'result' : 'Dataset file not exists!'
                }
            shell.execute('ln -s ' + pathDset + ' ' + pathPj)
            pathDsetln = 'dataset/' + str(dataIds[i]) + '/'
            paths.append(pathDsetln)

        return {
            'status': 1,
            'result': {
                'message':"dataset bind successde!",
                'path': paths
            }
        }

    else:
        #unbind dataset
        done = {}
        for i in range(len(dataIds)):
            path = config.dir_home + config.dir_home_user + '/' + str(userId) + '/system/' + str(projectId) + '/' + str(version) + '/dataset/' + str(dataIds[i])
            if not os.path.exists(path):
                #the data not binded
                done[str(i)] = 'data hava not been binded bebindDataWithProjectfore!'
            elif os.path.exists(path):
                try:
                    shell.execute('rm -rf ' + path)
                    done[str(i)] = 1
                except Exception as e:
                    sysout.err(TAG, e)
                    done[str(i)] = str(e)
        success = True
        for k in range(len(dataIds)):
            if not done[str(k)] == 1:
                success = False

        if success :
            return {
                'status': 1,
                'result': "unbind datasets success!"
            }
        else:
            return {
                'status': 0,
                'result': done
            }
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
