# global config file

app_name = "极算云notebook管理分发系统"
version = "v1.0.1"
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

## http request server for vm
vms_port = 18883
vms_host_dev = '121.40.62.80'       #dev
vms_host_release = '60.12.136.59'   #release
vms_host = vms_host_dev


# ----------- RELEASE ------------
# ns_host = '172.16.59.99'        #_release server cloudyotech.com
# ns_port_http = 8100
# ns_port = 8888
# ns_doname = 'https://g.cloudyotech.com/notebook'
# # ns_doname = 'http://' + ns_host + ":" + str(ns_port)
#
# # system home dir
# dir_home_release = '/notebook/storage'
# dir_home = dir_home_release
#
# # dir_home_user = '/users'
# dir_home_user = ''
# # user's project dir:   homeDir/users/userId/projectId/version/xxx-nb
#
# file_system_readme = dir_home +'/base/readme'


# ----------- DEV ------------
ns_host = '172.16.3.254'
ns_port_http = 8100
ns_port = 8888
ns_doname = 'https://dev.dongxicc.cn/notebook'
## ns_doname = 'http://' + ns_host + ":" + str(ns_port)

# system home dir
dir_home = '/notebook/storage'
# dir_home_user = '/users'
dir_home_user = ''
# user's project dir:   homeDir/users/userId/projectId/version/xxx-nb
file_system_readme = dir_home +'/base/readme'


# ----------- DEV2 for 18.18.18.174 ------------
# ns_host = '18.18.18.174'
# ns_port_http = 8100
# ns_port = 8888
# ns_doname = 'https://18.18.18.174:8888'
# ## ns_doname = 'http://' + ns_host + ":" + str(ns_port)
#
# # system home dir
# dir_home = '/notebook/storage'
# # dir_home_user = '/users'
# dir_home_user = ''
# # user's project dir:   homeDir/users/userId/projectId/version/xxx-nb
# file_system_readme = dir_home +'/base/readme'


# ----------- localohst ------------
# ns_host = '127.0.0.1'   #_localhost
# ns_port_http = 8100
# ns_port = 8888
# ns_doname = 'http://' + ns_host + ":" + str(ns_port)
#
# ## system home dir
# dir_home = '/Users/jerryyin/workspace/notebook/storage-dev'
# # dir_home_user = '/users'
# dir_home_user = ''
# ## user's project dir:   homeDir/users/userId/projectId/version/xxx-nb
# file_system_readme = dir_home +'/base/readme'



#cmd
#sshfs for storage on StorageServer
# cmd_sshfs_mount_storage = 'sshfs -o reconnect user@hostname:remote_dir local_dir'
#
#cmd = 'sshfs -o reconnect -o ssh_command "sshpass -p fd324;1 ssh" root@60.12.136.60:/sshfs /sshfs -o ConnectTimeout=30 -o StrictHostKeyChecking=no'
#
sshfs_pwd = 'fd324;1'

# release
# sshfs  root@60.12.136.60:/sshfs/ /notebook/storage
# pwd: fd324;1

#
# dev              [common network]
#  sshfs  root@60.12.136.61:/mnt
# sshfs_pwd = 'abcd#12345'

# path of the user's dataset
# path_dataset = '/file/datasets'

# sshfs -C -o reconnect root@60.12.136.61:/mnt /notebook/storage


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