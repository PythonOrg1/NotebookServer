# charst=utf-8

import os
from system import shell
from base import sysout
from config import config
from manager import jupyter

TAG = 'filemanager'


def createDir(dir):
    sysout.log(TAG, 'dir= ' + dir)
    exist = os.path.exists(dir)
    if not exist:
        os.makedirs(dir)
    exist = os.path.exists(dir)
    return exist


#
# get all files & dirs of the directory
#   response:
#   [
#        {'pwd': '/Users/jerryyin/.jupyter',            //current directory
#         'dirs': ['nbconfig', 'custom'],                //child dir
#         'files': ['.DS_Store', 'migrated', 'jupyter_notebook_config.py', 'jupyter_notebook_config.json2']      //all files
#         }, ...
#   ]
#
def getAllFiles(dir, containSystem=True):
    if dir == None or (not os.path.exists(dir)):
        return None
    result = []
    for pwd, d, file in os.walk(dir):
        if not (not containSystem and 'system' in str(pwd)):
            result.append({
                'pwd': pwd,
                'dirs': d,
                'files': file
            })
    return result


#
# get only one file name of the dir
# --fileForm:  .ipynb / .html / .py
#
def getOneNbFileName(dir, fileForm):
    # print("getOneNbFileName...")
    # print(str(dir) + '/ ' + str(fileForm))
    if dir == None or (not os.path.exists(dir)):
        return None
    data = getAllFiles(dir)
    if data == None:
        return None
    parentFiles = (data[0])['files']
    fileName = None
    for f in parentFiles:
        if str(fileForm) in str(f):
            fileName = str(f)
    return fileName


#
# get all the files & dirs of the user
# ** Except 'system' directory
#
def getUserHome(home):
    all = getAllFiles(home, False)
    print(all)
    return all


#
# @params dir:
#
# dirname | file | size | timeModify | timeAccess
# for one dir: name | totalSize | numDir | numFile | modifyTime | viewTime
#
#
def getFilesInfoOfPath(dir):
    if dir == None or (not os.path.exists(dir)) or (not os.path.isdir(dir)):
        return None
    contents = os.listdir(dir)
    if contents == None:
        return None
    if len(contents) == 0:
        return {}
    else:
        files = []
        dirs = []
        unknown = []
        for i in range(len(contents)):
            c = contents[i]
            filePath = ''
            if str(dir).endswith("/"):
                filePath = str(dir) + str(c)
            else:
                filePath = str(dir) + "/" + str(c)

            timeAccess = os.path.getatime(filePath)
            timeModify = os.path.getmtime(filePath)
            timeCreate = os.path.getctime(filePath)
            size = os.path.getsize(filePath)
            if os.path.isfile(filePath) or (not str(c).startswith(".") and "." in str(c)):
                #is a file
                # files.append(c)
                #get file's properties
                file = {
                    "name":c,
                    "locate":filePath,
                    "size":size,
                    "timeCreate":timeCreate,
                    "timeModify":timeModify,
                    "timeAccess":timeAccess
                }
                files.append(file)

            elif os.path.isdir(filePath) :
                # else:
                #is a dir
                isSystem = "system" in str(c)

                info = getAllFiles(filePath)
                print(info)
                numDirs = 0
                if len(info) > 1:
                    numDirs = len(info) - 1
                numFiles = 0
                for i in info:
                    numFiles += len(i['files'])

                d = {
                    "name": c,
                    "size": size,
                    "timeCreate": timeCreate,
                    "timeModify": timeModify,
                    "timeAccess": timeAccess,
                    "numDir":numDirs,
                    "numFiles":numFiles,
                    "system": isSystem
                }
                dirs.append(d)
            else:
                print(str(c)+" is unknown")
                unknown.append(c)
        result = {
            'files': files,
            'dirs': dirs,
            'unknown':unknown
        }
        return result

    # content = contents[0]       # all files & firs of the current dir

    # return content


def moveFile(fileName, dir, dirTo):
    # todo

    pass


def renameFile(file, newFileName):
    # todo

    pass


def getFileInfo(file, path):
    # todo

    pass


#
# get the directory number int the 'dir'
# linux :
#   get dir number of the dir
#       #ls -l |grep "^d"|wc -l
#
#   get file num of the dir
#       #ls -l |grep "^-"|wc -l
#
def getDirNumber(dir):
    cmd = 'ls -l ' + str(dir) + ' |grep "^d"|wc -l'
    n = os.popen(cmd).read()
    return n


#
# copy init common project to user's dir for preview
# path -- absolute path of the file
# filePath -- relative path of the  user's dir
#
def createProject(path, projectId, projectName, type, filePath):
    notebook = config.getNotebook(type)
    if notebook is not None:
        nb = notebook.get("nb")
        h5 = notebook.get("h5")
        py = notebook.get('py')
        shell.execute('cp ' + nb + ' ' + path + '/')
        shell.execute('cp ' + h5 + ' ' + path + '/')
        shell.execute('cp ' + py + ' ' + path + '/')
        shell.execute('cp  ~/.jupyter/custom/custom.css ' + path + '/')
        # if projectId != None:
        #     shell.execute('mv ' + config.getNotebookName() + ' ' + str(projectId) + '.ipynb')
        #     shell.execute('mv ' + config.getH5Name() + ' ' + str(projectId) + '.ipynb')

        # jupyter.executingNb(path, config.getNotebookName(), type)

        return {
            'projectId': projectId,
            'projectName': projectName,
            'projectType': type,
            'version': 1,
            'notebook': config.ns_doname + '/notebooks/storage' + filePath + '/' + config.getNotebookName(),
            'html': config.ns_doname + '/notebooks/storage' + filePath + '/' + config.getH5Name(),
            'py': config.ns_doname + '/notebooks/storage' + filePath + '/' + config.getPYName()
            # 'notebook': config.ns_doname + '/notebooks' + filePath + '/' + config.getNotebookName(),
            # 'html': config.ns_doname + '/notebooks' + filePath + '/' + config.getH5Name(),
            # 'py': config.ns_doname + '/notebooks' + filePath + '/' + config.getPYName()
        }
    else:
        return None


#
# response:
#         1 : 'Delete Sccess!',
#         0 : 'Delete Failed, cause: ',
#         2 : 'File not exists!'
#
def deleteFile(path):
    try:
        if os.path.exists(path):
            d = shell.execute('rm -rf ' + path)
            print("d ======== ")
            print(d)
            return (1, 'Delete Sccess!')
        else:
            return (2, 'File not exists!')
    except Exception as e:
        return (0, 'Delete Failed, cause: ' + e)

# for test
# if __name__ == '__main__':
#     getAllFiles('/Users/jerryyin/notebook')
