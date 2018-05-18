#coding: utf-8

import os 
from random import shuffle
import sys

from fabric.api import *
from fabric.contrib import django
django.project('TestManagement')
django.settings_module('TestManagement.settings')
from django.conf import settings

from svc.sql import enable_clients_ip_sql, master_ip_sql, locust_master_ip_sql


USER = 'root'
PASSWD = '51talk'


LOCUST_MASTER = db.query(locust_master_ip_sql)[0].value


#------------------ Execution Configration --------------------------
#path config
base_path = "/opt"
base_venv_path = base_path + "/pyvenv36"
source_code_path = base_path + "/svc_load"
app_path = base_path + "/svc_load/webapp"
deploy_path = app_path + "/salt_deploy"
locust_file_path = source_code_path + "/locust_test"
source_package_path = "/opt/svc_load.tgz"
venv_source_path = "/opt/pyvenv36.tgz"
venv_locust = base_venv_path + "/bin/locust"
venv_python = base_venv_path + "/bin/python"
venv_salt = base_venv_path + "/bin/salt-ssh"
master_config = deploy_path + "/deploy_master"
slave_config = deploy_path + "/deploy_salve"
dup_slave_config = deploy_path + "/deploy_dup_slave"
all_config = deploy_path + "/deploy_all"

#cmd config
salt_ssh_param = venv_salt + "-i -r --output=yaml --roster-file={} '*' '{}'"
tar_source_code = "tar czf svc_load.tgz --exclude=*.log --exclude=*.out svc_load"
untar_source_code = "tar xzf svc_load.tgz"
untar_venv = "tar xzf pyvenv36.tgz"
start_master_cmd = "sh start_master.sh"
start_slave_cmd = "sh start_slave.sh %s" % LOCUST_MASTER
stop_locust_cmd = "pkill locust"
#程序运行很长时间后，有时通常的kill无法停止进程，需要用-9进行强杀
kill_locust_cmd = "pkill -9 locust"
#同步服务器时间
all_sync_os_time = "yum install -y ntp;ntpdate pool.ntp.org"

#cmd map
cmd_map = {
    1: "master_restart",
    2: "master_stop",
    3: "dup_slave_restart",
    4: "slave_stop",
    5: "slave_deploy_source",
    6: "slave_deploy_venv",
    7: "all_restart",
    8: "all_sync_os_time"
}


if __name__ == '__main__':
    pass