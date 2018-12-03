# global config file

from base import sysout

TAG = "config"
system = {
    'app_name': "极算云notebook文件管理分发系统",
    'version': "v1.0.1",
    'author': "JayYin",
    'mode': 'DEV'
    # 'mode': 'RELEASE'
    # 'mode': 'LOCALHOST'
}

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

## http request config for vm server
vms_port = 18883
vms_host_dev = '121.40.62.80'  # dev
vms_host_release = '60.12.136.59'  # release
vms_host = vms_host_release     # default : arelease

## notebook server config
## default config mode : RELEASE
ns_host = '172.16.59.99'  # _release server cloudyotech.com
ns_port_http = 8100
ns_port = 8888
ns_doname = 'https://g.cloudyotech.com/notebook'
# system home dir
dir_home = '/notebook/storage'
dir_home_user = ''
file_system_readme = dir_home + '/base/readme'

#/notebook/storage/base/class/classIds/projectIds
#/notebook/storage/base/datasets/
dir_pub_class = dir_home + '/base/class'
dir_pub_dsets = dir_home + '/base/datasets'
#
#



# ----------- RELEASE ------------
ns_config_release = {
    'ns_host': '172.16.59.99',  # _release server cloudyotech.com',
    'ns_host_pub': '120.26.57.100',
    'ns_port_http': 8100,
    'ns_port': 8888,
    'ns_doname ': 'https://g.cloudyotech.com/notebook',
    # system home dir
    'dir_home': '/notebook/storage',
    'dir_home_user': '',
    'file_system_readme': '/notebook/storage/base/readme',
    'dir_log':'/notebook/NotebookServer/logs/NotebookServer.log'
}

# ----------- DEV ------------
ns_config_dev = {
    'ns_host': '172.16.3.254',
    'ns_host_pub': '120.26.48.110',
    'ns_port_http': 8100,
    'ns_port': 8888,
    'ns_doname': 'https://dev.dongxicc.cn/notebook',
    # system home dir
    'dir_home': '/notebook/storage',
    'dir_home_user': '',
    'file_system_readme': '/notebook/storage/base/readme',
    'dir_log': '/notebook/NotebookServer/logs/NotebookServer.log'
}

# ----------- DEV2 for 18.18.18.174 ------------
ns_config_dev2 = {
    'ns_host': '18.18.18.174',
    'ns_host_pub': '120.26.48.110',
    'ns_port_http': 8100,
    'ns_port': 8888,
    'ns_doname': 'https://18.18.18.174:8888',
    # system home dir
    'dir_home': '/notebook/storage',
    'dir_home_user': '',
    'file_system_readme': '/notebook/storage/base/readme',
    'dir_log': '/notebook/NotebookServer/logs/NotebookServer.log'
}

# ----------- localohst ------------
ns_config_local = {
    'ns_host': '127.0.0.1',
    'ns_host_pub': '120.26.48.110',
    'ns_port_http': 8100,
    'ns_port': 8888,
    'ns_doname': 'https://127.0.0.1:8888',
    # system home dir
    'dir_home': '/Users/jerryyin/workspace/notebook/storage',
    'dir_home_user': '',
    'file_system_readme': '/Users/jerryyin/workspace/notebook/storage/base/readme'
    # 'dir_pub_class': '/Users/jerryyin/workspace/notebook/storage/base/class',
    # 'dir_pub_dsets': '/Users/jerryyin/workspace/notebook/storage/base/datasets'
}


def initConfig():
    sysout.info(TAG, 'init system config of model [%s] ..' % system['mode'])
    global vms_host,ns_host_pub, ns_host, ns_port, ns_port_http, ns_doname, dir_home, dir_home_user, file_system_readme, dir_pub_class, dir_pub_dsets
    if system['mode'] == 'DEV':
        vms_host = vms_host_dev
        ns_host_pub = ns_config_dev['ns_host_pub']
        ns_host = ns_config_dev['ns_host']
        ns_port_http = ns_config_dev['ns_port_http']
        ns_port = ns_config_dev['ns_port']
        ns_doname = ns_config_dev['ns_doname']
        dir_home = ns_config_dev['dir_home']
        dir_home_user = ns_config_dev['dir_home_user']
        file_system_readme = ns_config_dev['file_system_readme']
    elif system['mode'] == 'RELEASE':
        vms_host = vms_host_release
        ns_host_pub = ns_config_release['ns_host_pub']
        ns_host = ns_config_release['ns_host']
        ns_port_http = ns_config_release['ns_port_http']
        ns_port = ns_config_release['ns_port']
        ns_doname = ns_config_release['ns_doname']
        dir_home = ns_config_release['dir_home']
        dir_home_user = ns_config_release['dir_home_user']
        file_system_readme = ns_config_release['file_system_readme']
    elif system['mode'] == 'LOCALHOST':
        vms_host = vms_host_dev
        ns_host_pub = ns_config_local['ns_host_pub']
        ns_host = ns_config_local['ns_host']
        ns_port_http = ns_config_local['ns_port_http']
        ns_port = ns_config_local['ns_port']
        ns_doname = ns_config_local['ns_doname']
        dir_home = ns_config_local['dir_home']
        dir_home_user = ns_config_local['dir_home_user']
        file_system_readme = ns_config_local['file_system_readme']
        dir_pub_class = ns_config_local['dir_home'] + '/base/class'
        dir_pub_dsets = ns_config_local['dir_home'] + '/base/datasets'
    sysout.info(TAG, 'init system config successed! ')


# cmd
# sshfs for storage on StorageServer
# cmd_sshfs_mount_storage = 'sshfs -o reconnect user@hostname:remote_dir local_dir'
#
# cmd = 'sshfs -o reconnect -o ssh_command "sshpass -p fd324;1 ssh" root@60.12.136.60:/sshfs /sshfs -o ConnectTimeout=30 -o StrictHostKeyChecking=no'
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
