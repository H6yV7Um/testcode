# coding:utf-8

import time
import sys

from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.files import exists

from deploy_settings import *


#-----------------------Function Defintion Part----------------------
class DeployError(Exception):
    pass

def check_cmd_status(return_obj):
    '''检查命令执行状态，并对成功和失败状态做相应处理'''
    if return_obj.succeeded:
        status = {"status": "success"}
    else:
        status = {"status": "fail"}
    return status

@roles('master_servers')
def pack_source_code():
    '''func doc'''
    with cd(base_path):
        retobj = run(tar_source_code)
    if not retobj.succeeded:
        raise DeployError("package failed!")

def unpack_source_code():
    '''解压源码包'''
    with cd(base_path):
        retobj = run(untar_source_code)
    return check_cmd_status(retobj)

def unpack_venv():
    '''func doc'''
    with cd(base_path):
        retobj = run(untar_venv)
    return check_cmd_status(retobj)

def distribute_source_file():
    '''func doc'''
    retobj = put(source_package_path, base_path)
    return check_cmd_status(retobj)

def distribute_venv():
    '''func doc'''
    retobj = put(venv_source_path, base_path)
    return check_cmd_status(retobj)

@roles("master_servers")
def start_webapp():
    '''func doc'''
    with cd(app_path):
        retobj = run(start_app_cmd)
    if not retobj.succeeded:
        raise DeployError("start master fail!")

@roles('master_servers')
def start_master():
    '''master server just start a webserver'''
    with cd(locust_file_path):
        retobj = run(start_master_cmd)
    if not retobj.succeeded:
        raise DeployError("start master fail!")

@roles('master_servers')
def stop_master():
    '''func doc'''
    retobj = run(stop_locust_cmd)
    return check_cmd_status(retobj)

@roles('master_servers')
def kill_master():
    '''func doc'''
    retobj = run(kill_locust_cmd)
    return check_cmd_status(retobj)

@hosts(dup_slaves)
@parallel(pool_size=10)
def start_slave():
    '''func doc'''
    with cd(locust_file_path):
        run(start_slave_cmd)

def stop_slave():
    '''func doc'''
    retobj = run(stop_locust_cmd)
    return check_cmd_status(retobj)

def kill_slave():
    '''func doc'''
    retobj = run(kill_locust_cmd)
    return check_cmd_status(retobj)

@parallel
def ntpdate():
    run(install_ntp_cmd)
    run(sync_ntp)

def clear_useless(path, base):
    target = os.path.join(base, path)
    if exists(target):
        run(clear_cmd.format(target))
    else:
        return False



#--------------------------execute part-----------------------------------
@runs_once
def deploy_source():
    '''部署源码以及运行环境'''
    execute(pack_source_code)
    execute(distribute_source_file)
    execute(unpack_source_code)

@runs_once
def deploy_venv():
    '''部署python沙箱环境'''
    execute(distribute_venv)
    execute(unpack_venv)

@runs_once
def start_all():
    '''启动master.slave.webapp'''
    # execute(start_webapp)
    execute(start_master)
    execute(start_slave)

def restart_all():
    '''强杀重启所有节点'''
    execute(restart_masters)
    execute(kill_slave)
    execute(start_slave)

@runs_once
def stop_all():
    '''func doc'''
    execute(kill_master)
    execute(kill_slave)

@runs_once
def restart_masters():
    '''func doc'''
    execute(stop_master)
    execute(start_master)

@runs_once
def stop_masters():
    '''func doc'''
    execute(stop_master)

@runs_once
def start_slaves():
    '''func doc'''
    execute(start_slave)

@runs_once
def restart_slaves():
    '''func doc'''
    execute(stop_slave)
    execute(start_slave)
    
@runs_once
def stop_slaves():
    '''func doc'''
    # execute(stop_slave)
    execute(kill_slave)

@runs_once
def sync_os_time():
    '''同步服务器时间'''
    execute(ntpdate)

@runs_once
def clear(path, base=base_path):
    '''删除无用文件'''
    execute(clear_useless, path, base)