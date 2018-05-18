#coding: utf-8

import os 
from random import shuffle
import sys

from fabric.api import *
from fabric.contrib import django
django.project('TestManagement')
django.settings_module('TestManagement.settings')
from django.conf import settings

from dataprocess import DBConnection
from svc.sql import enable_clients_ip_sql, master_ip_sql, locust_master_ip_sql


#----------------------------- general config ----------------------------
#并行模式默认关闭，1.3以上支持, win不支持
env.parallel = False
#关闭默认的hosts去重功能
env.dedupe_hosts = False
#遇到错误只warn而不会abort
env.warn_only = True
#重试连接次数，默认为1
env.connection_attempts = 2
#连接超时，默认10s
env.timeout = 5
#跳过连接失败或报错的host
env.skip_bad_hosts = True
env.keepalive = 10
env.use_shell = False
#禁用pty提高cmd执行成功率，默认为True
env.always_use_pty =False
#eagerly_disconnect = True
#host的登陆账号密码
env.user = 'root'
env.password = '51talk'

#这种方式可以为evn.hosts中的host指定其他账号密码
#这种方式指定密码时，host_string必须为完整格式：user@host:port
env.passwords = {
    "root@172.16.16.43:22": "51talk"
}

#master和slaves都必须为list
db = DBConnection(db='svc_load') 
def get_slave_ip():
    slave_list = db.query(enable_clients_ip_sql)
    dup_slave_ip = []
    uniq_slave_ip = [client.client_ip for client in slave_list]
    for client in slave_list:
        per_client_slave_list = [client.client_ip]*client.slave_count
        dup_slave_ip.extend(per_client_slave_list)
    shuffle(dup_slave_ip)
    return uniq_slave_ip, dup_slave_ip

master = [master.client_ip for master in db.query(master_ip_sql)]
unique_slaves, dup_slaves = get_slave_ip()
LOCUST_MASTER = db.query(locust_master_ip_sql)[0].value

#-------------------- Env Configration Part --------------------------

env.hosts = unique_slaves
# env.hosts = ["172.16.16.88", "172.16.16.87"]

env.roledefs.update({
    "master_servers": master,
    # "master_servers": ["172.16.16.73"],
})

#------------------ Execution Configration --------------------------
#path config
base_path = "/opt/"
venv_path = "pyvenv36"
# base_venv_path = base_path + "venv_python2.7.13"
# venv_tar_name = "venv_python2.7.13.locust.tgz"
base_venv_path = base_path + venv_path
venv_tar_name = "venv_cpy36.tgz"
source_tar_name = "svc_load.tgz"
app_path = base_path + "svc_load/webapp"
source_package_path = base_path + source_tar_name
source_code_path = base_path + "svc_load"
locust_file_path = source_code_path + "/locust_test"
venv_source_path = base_path + venv_tar_name
venv_locust = base_venv_path + "/bin/locust"
venv_python = base_venv_path + "/bin/python"
venv_fab = base_venv_path + "/bin/fab"
scripts_path = os.path.join(settings.BASE_DIR, 'deploy', 'deploy_load_env.py')

#cmd config
tar_source_code = "tar czf {} --exclude=*.log --exclude=*.out svc_load".format(source_tar_name)
untar_source_code = "tar xzf " + source_tar_name
remove_source_tar = "rm -fr " + source_tar_name
tar_venv = "tar czf {} {}".format(venv_tar_name, venv_path)
untar_venv = "tar xzf " + venv_tar_name
remove_venv_tar = "rm -fr " + venv_tar_name
start_app_cmd = "sh runapp.sh"
start_master_cmd = "sh start_master.sh"
start_slave_cmd = "sh start_slave.sh %s" % LOCUST_MASTER
stop_locust_cmd = "pkill locust"
#程序运行很长时间后，有时通常的kill无法停止进程，需要用-9进行强杀
kill_locust_cmd = "pkill -9 locust"
#同步服务器时间
install_ntp_cmd = "yum install -y ntp"
sync_ntp = "ntpdate cn.ntp.org.cn"
#清楚无用的文件等
clear_cmd = "rm -fr {}"

#cmd map
cmd_map = {
    1: "restart_masters",
    2: "stop_masters",
    3: "restart_slaves",
    4: "stop_slaves",
    5: "deploy_source",
    6: "deploy_venv",
    7: "restart_all",
    8: "sync_os_time",
    9: "clear"
}


if __name__ == '__main__':
    pass