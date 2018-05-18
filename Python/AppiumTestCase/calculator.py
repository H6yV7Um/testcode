#coding=utf-8
from appium import webdriver
import time
import os
import HTMLTestRunner
import unittest

class AndroidTest(unittest.TestCase):
    """docstring for AndroidTest"""
    def setUp(self):     
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4.2'
        desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['appPackage'] = 'com.suning.mobile.ebuy'
        desired_caps['appActivity'] = '.base.host.InitialActivity'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.set_network_connection(6)
        page = self.driver.page_source       #输出当前页面的xml形式，一般用于调试定位元素
        print page
    def tearDown(self):
        self.driver.quit()
    def test_lauch_app(self):
        #self.driver.find_element_by_android_uiautomator('new UiSelector().resourceId("com.suning.mobile.ebuy:id/iv_4")').click()
        time.sleep(1)
        self.driver.find_element_by_class_name('android.widget.ImageButton').click()
        time.sleep(3)
        #self.driver.launch_app('com.suning.mobile.ebuy')
        #driver.swipe(0,500,0,1000,2000)
if __name__ == '__main__':
    unittest.main()
    '''
    suite = unittest.TestSuite()
    suite.addTest(AndroidTest("test_lauch_app"))
    timestr = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    filename ='D:\\test\\result_'+ timestr + '.html'
    print filename
    fp =open(filename,'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title=u'测试报告',description=u'UI自动化测试报告如下：')
    runner.run(suite)
    fp.close()
    '''


    
