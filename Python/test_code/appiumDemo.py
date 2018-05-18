#coding:utf-8

'''
@author: Administrator
'''

import os
import unittest
import time
import HTMLTestRunner
from appium import webdriver
from time import sleep


PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class AndroidTest(unittest.TestCase):
    def setUp(self):
        #unittest.TestCase.setUp(self)
        desired_caps = {}
        desired_caps['platformName']='android'
        desired_caps['platformVersion'] = '4.4'
        desired_caps['deviceName'] = '4df1b62275664f45'
        #desired_caps['app'] = 'Calculator.apk'
        desired_caps['appPackage'] = 'xxx'
        desired_caps['appActivity'] = 'xxx'
        self.driver= webdriver.Remote('http://192.168.9.105:4723/wd/hub', desired_caps)
    
    def tearDown(self):
        self.driver.close_app()
        self.driver.quit()
   
    def test_login(self):
        nameEditText = self.driver.find_element_by_id("xxx:id/nameET")
        nameEditText.clear()
        nameEditText.send_keys("1")
        passwordEditText = self.driver.find_element_by_id("xxx:id/passwordET")
        passwordEditText.clear()
        passwordEditText.send_keys("1")
        loginButton = self.driver.find.element_by_id("xxx:id/loginBtn")
        loginButton.click()
        sleep(1)
        
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(AndroidTest("test_login"))
    timestr = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    filename ='D:\\test\\result_'+ timestr + '.html'
    print filename
    fp =open(filename,'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='测试结果',description='测试报告')
    runner.run(suite)
    fp.close()
    
     
        