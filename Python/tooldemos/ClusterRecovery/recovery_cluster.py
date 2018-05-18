#coding:utf-8

from fabric.api import *
from fabric.context_managers import *
from fabric.colors import *
from fabric.contrib.console import confirm
import time
import os


env.user = 'root'
env.password = 'test@2016'
env.hosts = [
    '192.168.1.1:8087', 
    '192.168.1.2:8238',
    '192.168.1.3:8288',
]

#定义服务器分组
env.roledefs = {
    'cloudera_manager': ['192.168.1.1:8087'],
    'agent': ['192.168.1.1:8238','192.168.1.1:8288',]
}

hostsMap = "\\n192.168.1.1 test2.docker.name\\n192.168.1.1 test.docker.name"

@roles('cloudera_manager')
def recovery_manager():
    print yellow("Starting cloudera manager service...")
    with settings(warn_only=True):
        run("service cloudera-scm-server-db start")
        run("service cloudera-scm-server start ")
        run("service httpd start")
    print green("Done!")

@roles('agent')
def recovery_agent():
    print yellow("Starting cloudra agents service....")
    with settings(warn_only=True):
        run("service cloudera-scm-agent start")
        run("service ntpd start")
    print green("Done!")

@task
def recovery_hosts():
    print yellow("sync the hosts files...")
    with settings(warn_only=True):
        run("service iptables stop")
        print hostsMap
        run("echo -e '{0}' >> /etc/hosts".format(hostsMap))
    print green("Cluser is OK!")

@hosts('10.19.144.45:8238')
def start_mysql():
    print yellow("Starting mysql server...")
    with settings(warn_only=True):
        run("mysqld --user=root")
    print green("Done!")


@task
def deploy():
    recovery_manager()
    recovery_agent()
    recovery_hosts()
    start_mysql()








