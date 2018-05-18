# coding:utf-8

import time
import sys
import os
from collections import defaultdict
from fabric.api import *
from fabric.context_managers import *
from fabric.colors import *
from fabric.contrib.console import confirm
from Glogger import Glogger


# server distribution
# env.parallel = True
env.colorize_errors = True
env.warn_only = True
env.skip_bad_hosts = True
env.user = 'root'
env.sudo_user = 'italk'
env.password = '51talk.com'

# 这种方式指定密码时，host_string必须为完整格式：user@host:port
env.passwords = {
    "root@172.16.16.43:22": "51talk"
}

env.hosts = [
    "172.16.0.115",
    "172.16.0.136",
    "172.16.0.139"

]
env.roledefs.update({
    "source_servers": ["172.16.16.43"],
    "acc_class_servers": ["172.16.0.115", "172.16.0.136"],
    "class_servers": ["172.16.0.115", "172.16.0.136", "172.16.0.139"],
    "class_mgr_servers": ["172.16.0.139"]
})

# path
source_code_path = r"/root/update/"
target_code_base_path = "/data/italk/"
svn_update_path = "/root/italkIM_update/"
path_level = "/debug"

# command
get_latest_code_path = r"`ls -ltr|tail -n 1|awk '{print $9}'`"
copy_source_to_svnpath = "\cp -f {0} {1}"
svn_commit = "svn commit {0} -m '{1}'"
svn_update = "svn update {0}"
start_service = "./service.sh {} restart"
backup_file = "mv {0} {0}_bak"
restore_file = "\cp -f {0}_bak {0}"
get_md5 = "md5sum ./*"

#结果对象
temp_result = defaultdict(list)
final_result = {}

#日志
logger = Glogger.getLogger()

def parseString(attrstr):
    '''
    run("ls")返回以空白符分割的字符串，且前三个字符串为对象属性字符串，没有用处，
    其余的为ls实际返回的目录列表，所以在split后从第四个字符串取值
    '''
    try:
        rlist = attrstr.split()[3:]
        if rlist[0].startswith('italk_'):
            source_map = {item: item[6:] for item in rlist}
            return source_map
        else:
            return rlist
    except Exception as e:
        print e
        sys.exit(2)


def checkPath(path):
    '''校验文件路径是否存在'''
    result = run("cd %s" % path)
    if result.succeeded:
        return True

def checkStatus(return_obj, filename):
    '''检查命令执行状态，并对成功和失败状态做相应处理'''
    if return_obj.succeeded:
        temp_result["success"].append(filename)
    else:
        temp_result["fail"].append(filename)
    result = temp_result.copy()
    return result

def getFuncName(obj):
    '''获取调用者函数的名称'''
    func_name = inspect.stack()[1][3]
    func_obj = getattr(obj, func_name)
    return func_obj.func_name

@roles("source_servers")
def copySourceFile(flag=True):
    '''
    @description: 在43机器上将最新的代码拷贝到纳入svn版本管理的目录
                  并返回文件名称与服务目录的映射对象
    @return: {host1: files，host2: files},host是fabric自动加的key，为执行服务器的IP
    '''
    with cd(source_code_path):
        latest_code_folder = run(r"ls -ltr|tail -n 1|awk '{print $9}'")
        latest_code_folder = parseString(latest_code_folder)
        with cd(latest_code_folder[0]):
            rawstr = run("ls")
            files = parseString(rawstr)
            if flag:
                for filename, fpath in files.items():
                    target_path = svn_update_path + fpath + path_level
                    run(copy_source_to_svnpath.format(filename, target_path))
    return files


@roles("source_servers")
def commitToSvn(source_map):
    '''在43机器上提交最新的代码到svn'''
    message = prompt("please type commit message:")
    for filename, fpath in source_map.items():
        with cd(svn_update_path + fpath + path_level):
            # r = run(svn_commit.format(filename, message))
            r = run('ls')
            result = checkStatus(r, filename)
    temp_result.clear()
    print message
    return result


def updateServiceCode(source_map):
    '''从svn拉取最新代码并备份旧的'''
    for filename, dirname in source_map.items():
        if not checkPath(target_code_base_path + dirname):
            continue
        with cd(target_code_base_path + dirname + path_level):
            sudo(backup_file.format(filename))
            r = sudo(svn_update.format(filename))
            # r = run('ls')
            result = checkStatus(r, filename)
    temp_result.clear()
    return result


def restartService(source_map):
    '''重启更新过的服务'''
    for filename, dirname in source_map.items():
        if not checkPath(target_code_base_path + dirname):
            continue
        with cd(target_code_base_path):
            r = sudo(start_service.format(dirname))
            # r = run('ls')
            result = checkStatus(r, filename)
    temp_result.clear()
    return result


def restoreLastVersion(source_map):
    '''恢复到上个版本,并重启服务'''
    for filename, dirname in source_map.items():
        if not checkPath(target_code_base_path + dirname):
            continue
        with cd(target_code_base_path + dirname + path_level):
            sudo(restore_file.format(filename))
    restartService(source_map)


def checkMd5(source_map):
    '''Function Doc'''
    pass


@runs_once
def start():
    '''Function Doc'''
    source_map = execute(copySourceFile)
    source_map = source_map[env.roledefs['source_servers'][0]]
    #source_map格式如下
    #source_map = {'italk_class': 'class'}
    if source_map:
        final_result['source_code'] = source_map
        # final_result['commited_code'] = execute(commitToSvn, source_map)
        # final_result['update_service'] = execute(updateServiceCode, source_map)
        final_result['restart_service'] = execute(restartService, source_map)
        logger.info(final_result)
        logger.info(source_map)
    else:
        print "Error!"


@runs_once
def revert():
    '''Function Doc'''
    source_map = execute(copySourceFile, False)
    source_map = source_map[env.roledefs['source_servers'][0]]
    final_result['revert'] = execute(restoreLastVersion, source_map)
    logger.info(final_result)
