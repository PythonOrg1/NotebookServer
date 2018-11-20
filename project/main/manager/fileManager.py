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
# ls -l|grep
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
# get files number of one dir
# By Linux CMD
#
def getFileNumber(dir, containChildDir=False):
    if dir == None or (not os.path.exists(dir)):
        return None
    cmd = 'ls -l '+ dir + ' |grep "^-"| wc -l'
    if containChildDir:
        cmd = 'ls -lR '+ dir + ' |grep "^-"| wc -l'
    popen = shell.SubProcessCmd(cmd)
    num = popen.getOutBuff()
    popen.close()
    return num

#
# get dir number of one dir
# By Linux CMD
#
def getDirNumber(dir, containChildDir=False):
    if dir == None or (not os.path.exists(dir)):
        return None
    cmd = 'ls -l '+ dir + ' |grep "^d"| wc -l'
    if containChildDir:
        cmd = 'ls -lR '+ dir + ' |grep "^d"| wc -l'
    popen = shell.SubProcessCmd(cmd)
    num = popen.getOutBuff()
    popen.close()
    return num

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
    dataHome = home + '/数据集'
    datasetHome = home + '/system/datasets'
    if not os.path.exists(dataHome):
        os.makedirs(dataHome)
        if os.path.exists(datasetHome):
            shell.execute('ln -s ' + datasetHome + '/* ' + dataHome + '/')

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

    arr = str(dir).split('/')
    if not arr == None and len(arr) >= 3 and arr[2].isdigit():
        # dir = "/notebook/storage/userId"
        # is user's root /home
        dataHome = dir + '/数据集'
        datasetHome = dir + '/system/datasets'
        if not os.path.exists(datasetHome):
            os.makedirs(datasetHome)

        if not os.path.exists(dataHome):
            os.makedirs(dataHome)
            shell.execute('ln -s ' + datasetHome + '/* ' + dataHome + '/')

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
            if not str(contents[i]) == 'system':
                c = contents[i]
                filePath = ''
                if str(dir).endswith("/"):
                    filePath = str(dir) + str(c)
                else:
                    filePath = str(dir) + "/" + str(c)
                try:
                    timeAccess = str(os.path.getatime(filePath)).split(".")[0]
                    timeModify = str(os.path.getmtime(filePath)).split(".")[0]
                    timeCreate = str(os.path.getctime(filePath)).split(".")[0]
                    size = 0
                    if os.path.isfile(filePath) or (not str(c).startswith(".") and "." in str(c)):
                        # is a file
                        # files.append(c)
                        # get file's properties
                        size = os.path.getsize(filePath)
                        file = {
                            "name": c,
                            "locate": filePath,
                            "size": size,
                            "timeCreate": timeCreate,
                            "timeModify": timeModify,
                            "timeAccess": timeAccess
                        }
                        files.append(file)

                    elif os.path.isdir(filePath):
                        # else:
                        # is a dir
                        isSystem = "system" in str(c)

                        if filePath.endswith('/数据集'):
                            # '/notebook/storage/userId/数据集'
                            filePath = filePath.split('/数据集')[0] + '/system/datasets'
                        size = getDirSize(filePath)
                        # info = getAllFiles(filePath)
                        # print(info)
                        # numDirs = 0
                        # if len(info) > 1:
                        #     numDirs = len(info) - 1
                        # numFiles = 0
                        # for i in info:
                        #     numFiles += len(i['files'])
                        numDirs = getDirNumber(filePath, True)
                        numFiles = getFileNumber(filePath, True)
                        d = {
                            "name": c,
                            "size": size,
                            "timeCreate": timeCreate,
                            "timeModify": timeModify,
                            "timeAccess": timeAccess,
                            "numDir": numDirs,
                            "numFiles": numFiles,
                            "system": isSystem
                        }
                        dirs.append(d)
                    else:
                        print(str(c) + " is unknown")
                        u = {
                            "name": c,
                            "msg": 'unknown file or directory!'
                        }
                        unknown.append(u)
                except Exception as  e:
                    sysout.err(TAG, e)
                    u = {
                        "name": c,
                        "msg": 'unknown file or directory, cause ' + str(e)
                    }
                    unknown.append(u)
        result = {
            'files': files,
            'dirs': dirs,
            'unknown': unknown
        }
        return result

    # content = contents[0]       # all files & firs of the current dir

    # return content


#
#
#
def getDirSize(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
    return size

#
# move file to dir
#
# file, dir -- abs path
#
def moveFile(file, dir):
    if file == None:
        return (0, 'File can not be null !')
    if dir == None:
        return (0, 'Directory can note be null !')
    if not os.path.exists(file):
        return (0, 'File ' + str(file) + ' not exists !')
    if not os.path.exists(dir):
        return (0, 'Directory ' + str(dir) + ' not exists !')
    try:
        if (str(dir).endswith("/")):
            shell.execute('mv ' + str(file) + ' ' + str(dir))
        else:
            shell.execute('mv ' + str(file) + ' ' + str(dir) + '/')
        return (1, 'File move successed !')
    except Exception as e:
        sysout.err(TAG, e)
        return (0, 'File move failed, ' + str(e))


#
# rename file or dir
#
def rename(src, dst):
    sysout.log(TAG, "src: " + str(src))
    sysout.log(TAG, "dst: " + str(dst))
    if src == None:
        return {
            'status': 0,
            'result': 'Src can not be null !'
        }
    if dst == None:
        return {
            'status': 0,
            'result': 'Dst can not be null !'
        }
    if not os.path.exists(src):
        return {
            'status': 0,
            'result': str(src) + ' not found !'
        }

    src = str(src)
    s = src.split("/")
    i = len(s) - 1
    if src.endswith("/"):
        i = len(s) - 2
    name = s[i]
    path = src.split("/" + str(name))[0]
    dst = path + "/" + dst

    if os.path.exists(dst):
        return {
            'status': 0,
            'result': str(dst) + ' is already exists !'
        }
    try:
        os.rename(src, dst)
        if not os.path.exists(src) and os.path.exists(dst):
            return {
                'status': 1,
                'result': 'rename success !'
            }
        else:
            return {
                'status': 0,
                'result': 'rename falied !'
            }
    except Exception as e:
        sysout.err(TAG, e)
        return {
            'status': 0,
            'result': 'rename failed, ' + str(e)
        }


def makeDir(dir):
    if dir == None:
        return (0, 'Directory can not be null !')
    if "/" not in str(dir):
        return (0, 'Directory form not support, should be absolute path !')
    else:
        try:
            shell.execute("mkdir " + dir)
            return (1, 'Create successed !')
        except Exception as  e:
            return (0, 'Create directory failed, ' + str(e))


def createFile(file):
    if dir == None:
        return (0, 'File can not be null !')
    if "/" not in str(dir):
        return (0, 'File form not support, should be absolute path !')
    else:
        try:
            shell.execute("touch " + file)
            return (1, 'Create successed !')
        except Exception as  e:
            return (0, 'Create file failed, ' + str(e))

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
            if '(' in path:
                path = str(path).replace('(', '\(')
            if ')' in path:
                path = str(path).replace(')', '\)')

            d = shell.execute('rm -rf ' + path)
            print("d ======== ")
            print(d)
            if d == 0:
                return (1, 'Delete Sccess!')
            else:
                return (0, 'Delete Failed, Please check file format!')
        else:
            return (2, 'File not exists!')
    except Exception as e:
        return (0, 'Delete Failed, cause: ' + e)

def deleteFiles(paths):
    result = []
    for p in paths:
        code, msg = deleteFile(p)
        result.append({
            'code': code,
            'msg': msg
        })
    return result

# for test
# if __name__ == '__main__':
#     getFileNumber('/Users/jerryyin/notebook')
