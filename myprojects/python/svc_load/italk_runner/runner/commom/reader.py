#!/usr/bin/env python
# coding=utf-8
# 作用：模块用于读取italk_runner的配置文件，并根据
# 历史：yuyong_id 2016-10-17

import ConfigParser
import os
import random
from settings import BASE_DIR

__metaclass__ = type


def singleton(cls):
    instances = {}
    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

@singleton
class runnerConfig(object):
    '''
    counter will return some random config data,
    if config file did not fill in a real config data
    '''

    def __init__(self, *args, **kwargs):
        config_file = os.path.join(BASE_DIR, "config", "runner.config")
        self.config = self.read_file(config_file)

    def read_file(self, config_file):
        cf = ConfigParser.ConfigParser()
        cf.read(config_file)
        try:
            self.lbsIP = cf.get("italk", "lbsIP")
            self.lbsPort = cf.getint("italk", "lbsPort")
            self.accIP = cf.get("italk", "accIP")
            self.accPort = cf.getint("italk", "accPort")
            self.statusMgrIP = cf.get("italk", "statusMgrIP")
            self.statusMgrPort = cf.get("italk", "statusMgrPort")
            self.pvpMgrIP = cf.get("italk", "pvpMgrIP")
            self.pvpMgrPort = cf.get("italk", "pvpMgrPort")
            self.dbIP = cf.get("italk", "dbIP")

            self.uid = cf.getint("runner", "uid")
            self.cid = cf.getint("runner", "cid")
        except ConfigParser.NoOptionError as err:
            print('error:something wrong with config file' + config_file)
            print("错误：配置文件错误！！")
            print(err)
            raise

    def __random_account(slef, mark):
        # id根据，将mark值右移56位
        return random.randint(1, 0xffffffffffffff) + (mark << 56)

    def __class_id(self, mark=0):
        if self.cid != 0:
            return self.cid
        # 当配置文件的值为0时，根据mark值生成随机id
        return self.__random_account(mark)

    def __user_id(self, mark=0):
        if self.uid != 0:
            return self.uid
        # 当配置文件的值为0时，根据mark值生成随机id
        return self.__random_account(mark)

    def class_id(self):
        '''get a commom class id, 1v1 class'''
        return self.__class_id(0)

    def public_class_id(self):
        '''get a public class id'''
        return self.__class_id(1)

    def b2s_class_id(self):
        '''get a B2S class id'''
        return self.__class_id(12)

    def student_id(self):
        '''get a student user id'''
        return self.__user_id(0)
    
    def customize_class_id(self, mark):
        return self.__class_id(mark)

    def teacher_id(self):
        '''get a teacher user id'''
        return self.__user_id(1)

    def __choice_ip(self, ip_list):
        # ip将单独的字符串转换成列表
        ip_list = ip_list.split(',')
        # 随机选取列表中的一个ip
        return random.choice(ip_list)

    def lbs_ip(self):
        '''get lbs ip'''
        return self.__choice_ip(self.lbsIP)

    def lbs_port(self):
        return self.lbsPort

    def acc_ip(self):
        '''get acc ip'''
        return self.__choice_ip(self.accIp)

    def acc_port(self):
        return self.accPort

    def status_mgr_ip(self):
        return self.statusMgrIP

    def status_mgr_port(self):
        return self.statusMgrPort

    def pvp_mgr_ip(self):
        return self.pvpMgrIP

    def pvp_mgr_port(self):
        return self.pvpMgrPort

    def database_ip(self):
        return self.dbIP
    
    
if __name__ == '__main__':
    conf = runnerConfig()
    print conf.lbs_ip()
