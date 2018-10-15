# charst=utf-8

import os

from project.main.system import shell
from project.main.base import sysout
from project.main.config import config
from project.main.manager import jupyter

TAG = 'filemanager'


def createDir(dir):
    sysout.log(TAG, 'dir= ' + dir)
    exist = os.path.exists(dir)
    if not exist:
        os.makedirs(dir)
    exist = os.path.exists(dir)
    return exist

#
# copy init common project to user's dir for preview
# path -- absolute path of the file
# filePath -- relative path of the  user's dir
#
def createPreProject(path, projectId, projectName, type, filePath):
    notebook = config.getNotebook(type)
    if notebook is not None:
        nb = notebook.get("nb")
        h5 = notebook.get("h5")
        shell.execute('cp ' + nb + ' ' + path + '/')
        shell.execute('cp ' + h5 + ' ' + path + '/')
        # if projectId != None:
        #     shell.execute('mv ' + config.getNotebookName() + ' ' + str(projectId) + '.ipynb')
        #     shell.execute('mv ' + config.getH5Name() + ' ' + str(projectId) + '.ipynb')

        jupyter.executingNb(path, config.getNotebookName(), type)

        return {
            'projectId':projectId,
            'projectName': projectName,
            'projectType':type,
            'notebook': config.ns_doname + '/notebooks' + filePath + '/' + config.getNotebookName(),
            'html': config.ns_doname + '/notebooks' + filePath + '/' + config.getH5Name()
        }
    else:
        return None
