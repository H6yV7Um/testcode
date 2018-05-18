# coding:utf-8

import time
import sys
import os
from collections import defaultdict
import logging

from fabric.api import *
from fabric.context_managers import *
from fabric.colors import *
from fabric.contrib.console import confirm

from utils import DictObj
from Glogger import Glogger


# server distribution
# env.parallel = True
env.colorize_errors = True
env.warn_only = True
env.skip_bad_hosts = True
env.user = 'root'
#env.sudo_user = 'italk'
env.password = '51talk'

# 这种方式指定密码时，host_string必须为完整格式：user@host:port
env.passwords = {
    "root@172.16.16.43:22": "51talk"
}

env.hosts = [
    "172.16.16.44",
    # "172.16.16.73"

]
env.roledefs.update({
    "master_servers": ["172.16.16.73"],
    "acc_class_servers": ["172.16.0.115", "172.16.0.136"],
    "class_servers": ["172.16.0.115", "172.16.0.136", "172.16.0.139"],
    "class_mgr_servers": ["172.16.0.139"]
})

#path config
base_path = "/opt"
source_package_path = "/opt/testlocust.tgz"
source_code_path = "/opt/locust_test"
venv_source_path = "/opt/venv_python2.7.13.tgz"
venv_locust = "/opt/venv_python2.7.13/bin/locust"
venv_python = "/opt/venv_python2.7.13/bin/python"

#cmd config
tar_source_code = "tar czf testlocust.tgz testlocust"
start_master_cmd = "nohup " + venv_locust + " -f testlocustfile.py --master &"
start_slave_cmd = venv_locust + " -f testlocustfile.py --slave --master-host=" + env.roledefs['master_servers'][0]
stop_slave_cmd = "pgrep locust|xargs -i kill -9 {}"

logger = logging.getLogger(__name__)

class DeployError(Exception):
    pass

def check_path(path, local=False):
    '''校验文件路径是否存在'''
    if local:
        resutl = local("cd %s" % path)
    else:
        result = run("cd %s" % path)
    if result.succeeded:
        return True

def check_cmd_status(return_obj):
    '''检查命令执行状态，并对成功和失败状态做相应处理'''
    if return_obj.succeeded:
        status = {"status": "success"}
    else:
        status = {"status": "fail"}
    return status

def tar_source_code():
    with cd(base_path):
        retobj = local(tar_source_code)
    if retobj.succeeded:
        logger.info("package finished!")
    else:
        raise DeployError("package failed!")

def distribute_source_file():
    '''func doc'''
    retobj = put(source_code_path, base_path)
    return check_cmd_status(retobj)

def distribute_venv():
    '''func doc'''
    retobj = put(venv_source_path, base_path)
    return check_cmd_status(retobj)

@roles('master_servers')
def start_master():
    '''master server just start a webserver'''
    with cd(source_code_path):
        retobj = run(start_master_cmd)
    if retobj.succeeded:
        logger.info("start master successfully!")
    else:
        raise DeployError("start master fail!")

@roles('master_servers')
def stop_master():
    '''func doc'''
    retobj = run(stop_slave_cmd)
    return check_cmd_status(retobj)

def restart_master():
    '''func doc'''
    execute(stop_master)
    time.sleep(1)
    execute(start_master)

def start_slave():
    '''func doc'''
    if check_path(source_code_path):
        with cd(source_code_path):
            retobj = run(start_slave_cmd)
            status = check_cmd_status(retobj)
    else:
        status = {'status':"fail"}
    return status

def stop_slave():
    '''func doc'''
    retobj = run(stop_slave_cmd)
    return check_cmd_status(retobj)

def restart_slave():
    '''func doc'''
    execute(stop_slave)
    time.sleep(1)
    execute(start_slave)

@runs_once
def start_deploy():
    '''func doc'''
    logger.info("deploying...")
    final_result = DictObj()
    # final_result.start_master = execute(start_master)
    final_result.start_slave = execute(start_slave)
    # final_result.stop_slave = execute(stop_slave)
    logger.info(final_result)
