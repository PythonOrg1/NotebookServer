# charset=utf-8

from project.main.base import sysout
from project.main.config import config, string
from project.main.manager import fileManager
from project.main.system import shell
import os

TAG = "projectManager"

# response of error message
resp_err_version_invlid = {'status': 0, 'result': 'incorrect version number!'}
resp_err_version_old_err = {'status': 0, 'result': 'current project is not exists!'}
resp_err_version_create_dir_err = {'status': 0, 'result': 'system error on create new directory!'}





# create user's project
#
# projectType -- 'PYTHON3' | 'PYTHON2' | 'R'
#
def createPreProject(userId, projectId, projectName, projectType):
    path = config.dir_home_user + '/' + str(userId) + '/' + str(projectId) + '/1'  # 1--version of pj， vesionInit=1
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
    if versionCur == None:
        return resp_err_version_invlid

    maxVersion = int(fileManager.getDirNumber(config.dir_home + config.dir_home_user + '/' + str(userId) + '/' + str(projectId) + '/'))
    if (versionCur <= 0 or versionCur > maxVersion):
        return resp_err_version_invlid

    curPath = config.dir_home_user + '/' + str(userId) + '/' + str(projectId) + '/' + str(versionCur)
    curNb = config.dir_home + curPath + '/' + config.getNotebookName()
    curH5 = config.dir_home + curPath + '/' + config.getH5Name()

    version = maxVersion + 1
    path = config.dir_home_user + '/' + str(userId) + '/' + str(projectId) + '/' + str(version)
    dir = config.dir_home + path
    if (fileManager.createDir(dir)):
        print(config.dir_home + curPath)
        if not os.path.exists(config.dir_home + curPath):
            return resp_err_version_old_err
        else:
            shell.execute('cp ' + curNb + ' ' + dir + '/')
            shell.execute('cp ' + curH5 + ' ' + dir + '/')
            return {
                'projectId': projectId,
                'projectName': projectName,
                'version': version,
                'notebook': config.ns_doname + '/notebooks' + path + '/' + config.getNotebookName(),
                'html': config.ns_doname + '/notebooks' + path + '/' + config.getH5Name()
            }
    else:
        return resp_err_version_create_dir_err
