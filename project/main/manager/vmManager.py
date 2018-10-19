
from project.main.config import config
from project.main.interfece.onResponseListener import onResponseListener
from project.main.utils import socketUtils
from project.main.base import sysout

import json

TAG = "vmManager"


def startVm(userId, isoName, vmId, passwd, gpu, cpu, memory, isoRemarks, action='start'):
    sysout.log(TAG, 'startVm...')
    host = config.vms_host
    port = config.vms_port

    p_body = {
        "iname": isoName,
        "cname": vmId,
        "user": userId,
        "action": action,
        "password": passwd,
        "nname": isoRemarks,
        "gpu": gpu,
        "cpu": cpu,
        "mem": memory
    }
    p_body = json.dumps(p_body)
    params = ("new_task_publish@" + p_body).encode('utf-8')
    # params = json.dumps().encode('utf-8')

    result = socketUtils.sendSocket(host, port, params)
    if result != None:
        sysout.log(TAG, result)
        if type(result) == type({}):
            if result['status'] == 200:
                # start vm success
                # resp example
                # {
                #     "status": 200,
                #     "result": {
                #         "jupyter": "http://xxx:000/xxx/notebooks/"
                #         "message": "xxx"
                #     }
                # }
                return {
                    'status': 1,
                    'result': result['result']
                }
            else:
                # start fail
                return {
                    'status': 0,
                    'result': 'start vm failed! cause: ' + str(result['result'])
                }
        else:
            return {
                'status': 0,
                'result': 'start vm failed! cause: Server response form error.'
            }
    else:
        return {
            'status': 0,
            'result': 'start vm failed! cause: Server have no response.'
        }


def resetPortJupyter(cname, index, action='start'):
    sysout.log(TAG, 'resetPortJupyter...')
    host = config.vms_host
    port = config.vms_port

    p_body = {
        "action": action,
        "cname": cname,
        "index": index
    }
    params = ("new_task_ssh@:" + json.dumps(p_body)).encode('utf-8')

    result = socketUtils.sendSocket(host, port, params)
    if result != None:
        sysout.log(TAG, result)
        if type(result) == type({}):
            if result['status'] == '200':
                # start vm success
                return {
                    'status': 1,
                    'result': 'reset port success!'
                }
            else:
                # start fail
                return {
                    'status': 0,
                    'result': 'reset port failed! cause: ' + result['result']
                }
        else:
            return {
                'status': 0,
                'result': 'reset port failed! cause: Server response form error.'
            }
    else:
        return {
            'status': 0,
            'result': 'reset port failed! cause: Server have no response.'
        }
