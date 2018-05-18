#!/usr/bin/env python
# coding=utf-8
import sys
import unittest
import acinter
import commom


data = commom.reader.runnerConfig()
LBS_IP = data.lbs_ip()
LBS_PORT = data.lbs_port()


class BaseTest(unittest.TestCase):
    '''
    用于测试连接acc，并进行登陆
    '''
    @classmethod
    def setUpClass(self):
        '''
        所有连接都必须先执行connect_lbs，这样才能初始化网络模块的线程.
        '''
        self.ac = acinter.interface.acsim()
        self.ac.connect_lbs(LBS_IP, LBS_PORT)
        self.ac.request_lbs()

    def setUp(self):
        pass

    # 测试lbs默认返回的acc列表的第一个
    def test_connect_def_acc(self):
        '''客户端接入: 0x00110011 '''
        self.assertEqual(
            self.ac.connect_acc().get('RspCode'),
            0
        )

    # 测试测试单个acc列表的函数
    def connect_test(self, server):
        acc_ip, acc_port = server
        self.assertEqual(
            self.ac.connect_acc(
                ip=acc_ip,
                port=acc_port
            ).get('RspCode'),
            0
        )

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(self):
        self.ac.disconnect_italk()

if __name__ == '__main__':
    unittest.main()
