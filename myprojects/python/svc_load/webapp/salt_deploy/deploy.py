#coding: utf-8

import random
import time
import subprocess
from hashlib import md5
import yaml

from svc.models import SvcLoadClient
from deploy_settings import *


class Deployment:
    US_CACHE = []
    DS_CACHE = []
    M_CHACHE = []
    def __init__(self, model=SvcLoadClient):
        self.cmd_map = cmd_map or {}
        self.objects = model.objects
        self.user = USER
        self.passwd = PASSWD

    def run(self, opcode):
        '''
        1.cmd router to check where to run on
        2.check cache to determine whether rewrite yaml config or not
        3.run cmd
        '''
        pass

    def _deploy_router(self, opcode):
        ''' call first for deciding to get whitch ips'''
        cmd_str = cmd_map.get(opcode)
        self.cmd = eval(cmd_str)
        if cmd_str.startswith('master'):
            self.ips = [r.ip for r in self.objects.filter(role='1', status=1)]
            self.cache = self.M_CHACHE
            self.config_file = master_config
        elif cmd_str.startswith('slave'):
            self.ips = [r.ip for r in self.objects.filter(role='2', status=1)]
            self.cache = self.US_CACHE
            self.config_file = slave_config
        elif cmd_str.startswith('dup_slave'):
            self.ips = []
            for r in self.objects.filter(role='2', status=1):
                self.ips.extend([r.ip]*r.slave_count)
            self.cache = self.DS_CACHE
            self.config_file = dup_slave_config
        else:
            self.ips = [r.ip for r in self.objects.filter(status=1)]
            self.cache = self.M_CHACHE+self.US_CACHE
            self.config_file = all_config

    def _make_config(self):
        if sorted(self.ips) != sorted(self.cache):
            self.cache = self.ips
            config = {}
            for ip in ips:
                key = self.uniq_suffix
                config[key] = {}
                config[key]['host'] = ip
                config[key]['user'] = self.user
                config[key]['passwd'] = self.passwd
            with open(self.config_file, 'w') as f:
                yaml.dump(config, f)

    def load_config(self):
        pass

    def _run_cmd(self):
        # /opt/pyvenv36/bin/salt-ssh -r -i --output=yaml --roster-file=$1 "*" "$2"
        args = salt_ssh_param.format(self.config_file, self.cmd)
        instance = subprocess.Popen([venv_salt, args], stdout=subprocess.PIPE, encoding='utf-8')
        result = instance.communicate()[0]

    @property
    def uniq_suffix(self):
        return md5(str(time.time() + random.randint(0,10000)).encode('utf-8')).hexdigest()


class Item(dict):
    def __init__(self, host, user, passwd):
        self.tag = {}
        self.uniq_suffix = {}
        self.host = str(host)
        self.user = user
        self.passwd = passwd
        
    def __repr__(self):
        return "%s(host=%r, user=%r, passwd=%r)" % (
            self.__class__.__name__, self.host, self.user, self.passwd
        )
    
    @property
    def uniq_suffix(self):
        return md5(str(time.time() + random.randint(0,10000)).encode('utf-8')).hexdigest()

    def __setattr__(self, attr, value):
        if attr != 'uniq_suffix':
            self['uniq_suffix'][attr] = value
        else:
            if hasattr(self, attr):
                self[getattr(self, attr, 'tag')] = {}
            else:
                self[attr] = value
        
    def __getattr__(self, key):
        if key in self['tag']:
            return self['tag'][key]
        else:
            return self[key]



if __name__ == '__main__':
    # print yaml.dump_all([Item(123,123,123), Item(456,456,456)])
    a = Deployment()
    a._make_config([123,123,123], ())

    