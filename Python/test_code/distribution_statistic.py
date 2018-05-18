#coding:utf-8
#!/usr/bin/python

import os
import subprocess
import sys
import re
from collections import deque
from fabric.api import *
from fabric.context_managers import *
from fabric.decorators import *

usage = """useage: statistic the num of parsed result
                eg: python statistic.py meituan 20160810"""

env.user = 'map'
env.password = 'Wm16$DA_SYs'
env.hosts = [
    #'192.168.236.131',
    'szwg-m52-do01-hadoop014.szwg01.baidu.com'
]

env.passwords = {
    'root@192.168.236.131': '123qwe',
    #'map@szwg-m52-do01-hadoop014.szwg01.baidu.com' : 'Wm16$DA_SYs',
    #'map@szwg-m52-do01-hadoop028.szwg01.baidu.com' : 'zkxlc1sjha9qw',

}

env.roledefs = {
    'ele': ['szwg-m52-do01-hadoop014.szwg01.baidu.com'],
    'meituan': ['szwg-m52-do01-hadoop028.szwg01.baidu.com']
}

script_path = "/home/work/do/etl/wmphp/application/cache/compete/output"
#target_path = "/home/map/wmphp/application/cache/compete/output"
target_path = "~/test"

class ObjectDict(dict):
    """docstring for ObjectDict"""
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

def get_file_list(source, date):
    pat = re.compile('^%s.+\.%s$' % (source, date))
    total_list = os.listdir('.')
    target_list = [f for f in total_list if pat.match(f)]
    return target_list

@runs_once
def upload_script():
    """upload the statistic script to remote servers"""

    print yellow("uploading the statistic script...")
    with settings(warn_only=True):
        put(script_path, target_path)
    print green("upload script successfully!")

#@roles('ele')
def get_ele_stat(*target_list):
    """get the statistic data from remote server of ele"""
    result = ObjectDict()
    for f in target_list:
        result.f = deque([])
        with cd(target_path):
            rnum = run("cat %s|wc -l" % f, quiet=True, timeout=60)
            result.f.appendleft(rnum)
        with lcd(target_path):
            lnum = local("cat %s|wc -l" % f, capture=True)
            result.f.appendleft(lnum)
        diff = int(lnum) - int(rnum)
        result.f.append(diff)
    return result


#@roles('meituan')
def get_meituan_stat():
    """get the statistic data from remote server of meituan"""
    result = ObjectDict()
    for f in target_list:
        result.f = deque([])
        with cd(target_path):
            rnum = run("cat %s|wc -l" % f, quiet=True, timeout=60)
            result.f.appendleft(rnum)
        with lcd(target_path):
            lnum = local("cat %s|wc -l" % f, capture=True)
            result.f.appendleft(lnum)
        diff = int(lnum) - int(rnum)
        result.f.append(diff)
    return result

def format_result(result):
    print "-"*80
    print "{0:<40}|{1:<15}|{2:<15}|{3:<15}".format("file_name", "local_num", "remote_num", "diff")
    print "-"*80
    for name, num_list in result.items():
        print "{0:<40}|{1[0]:<15}|{1[1]:<15}|{1[2]:<15}".format(name, num_list)
        print "-"*80

@task
def start(*param):
    target_list = get_file_list(param[0], param[1])
    if param[0] == 'ele':
        result = get_ele_stat(*target_list)
    elif param[0] == 'meituan':
        result = get_meituan_stat(*target_list)
    else:
        print useage
        return
    format_result(result)






