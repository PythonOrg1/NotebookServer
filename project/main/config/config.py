# global config file

app_name = "极算云notebook管理分发系统"
version = "v1.0.0"
author = "JayYin"

# server
# demo_svr_host="cloudolize.cn"
# demo_svr_port=22
# demo_svr_usr="root"
# demo_svr_pwd="Dtx700pp"
#
# path_tomcat = "/usr/local/tomcat8"
# cmd_start_tomcat = "sh "+path_tomcat+"/bin/startup.sh"
# cmd_stop_tomcat = "sh"+path_tomcat+"/bin/shutdown.sh"


# config of system file url

# ns_host = '127.0.0.1'
ns_host = '192.168.188.105'
ns_port_http = 8100
ns_port = 8888
ns_doname = 'http://' + ns_host + ":" + str(ns_port)

# system home dir
dir_home_localhost = '/Users/jerryyin/workspace/notebook'
dir_home_dev = ''
dir_home = dir_home_localhost

dir_home_user = '/users'
# user's project dir:   homeDir/users/userId/projectId/version/xxx-nb


# the common base nb of the sys
nb_base_python3 = dir_home + '/base/python3/edit.ipynb'
h5_base_python3 = dir_home + '/base/python3/edit.html'
py_base_python3 = dir_home + '/base/python3/edit.py'

nb_base_python2 = dir_home + '/base/python2/edit.ipynb'
h5_base_python2 = dir_home + '/base/python2/edit.html'
py_base_python2 = dir_home + '/base/python2/edit.py'

nb_base_r = dir_home + '/base/r/edit.ipynb'
h5_base_r = dir_home + '/base/r/edit.html'
py_base_r = dir_home + '/base/r/edit.py'


def getNotebook(projectType):
    return {
        'PYTHON3': {
            'nb': nb_base_python3,
            'h5': h5_base_python3,
            'py': py_base_python3
        },

        'PYTHON2': {
            'nb': nb_base_python2,
            'h5': h5_base_python2,
            'py': py_base_python2
        },
        'R': {
            'nb': nb_base_r,
            'h5': h5_base_r,
            'py': py_base_r
        }
    }.get(str(projectType).upper())


def getNotebookName():
    return 'edit.ipynb'

def getH5Name():
    return 'edit.html'

def getPYName():
    return 'edit.py'