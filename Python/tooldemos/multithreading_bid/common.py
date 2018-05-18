#coding:utf-8
import os
import re
import time
import random
import inspect
import urllib2
from BeautifulSoup import BeautifulSoup
from ConfigParser import ConfigParser,NoSectionError,NoOptionError

timestr = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime())

class SuperPath(object):
    """测试结果文件路径类"""
    def __init__(self):
        super(SuperPath, self).__init__()
        #self.arg = arg       
    @staticmethod
    def basepath():
        path = os.path.abspath(os.path.dirname(__file__))
        return path
    @staticmethod
    def imagepath(dir='screen_shot'):
        resultpath = os.path.join(SuperPath.basepath(),'test_result')
        if os.path.exists(resultpath):
            os.chdir(resultpath)
        else:
            os.mkdir(resultpath)
            os.chdir(resultpath)
        if os.path.exists(dir):
            screenshot_dir = os.path.abspath(dir)
        else:
            os.mkdir(dir)
            screenshot_dir = os.path.abspath(dir)
        os.chdir(screenshot_dir)
        if os.path.exists(timestr):
            screenshot_subdir = os.path.abspath(timestr)
        else:
            os.mkdir(timestr)
            screenshot_subdir = os.path.abspath(timestr)
        return screenshot_subdir
    @staticmethod
    def imagename(name):
        timestamp = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime())
        imagename = os.path.join(SuperPath.imagepath(),name +'_' + timestamp + '.jpeg')
        return imagename
    @staticmethod
    def get_current_function_name():
        '''获取当前调用方的函数名称'''
        return inspect.stack()[1][3]

    def testfunction(self):
        '''测试获取当前的函数名称'''
        #funcinfo = inspect.getmembers(self.testfunction)
        #funcname = dict(funcinfo)['func_name']
        funcname = SuperPath.get_current_function_name()
        return funcname     #返回当前函数名称testfunction

confpath = os.path.join(SuperPath.basepath(),'config.ini')

class SuperConfig(object):
    """读取配置文件类"""
    def __init__(self, path=confpath):
        super(SuperConfig, self).__init__()
        self.path = path
        #self.cf = ConfigParser()
        #self.cf.read(path)
    @staticmethod
    def readconf(section,option):       #静态方法和类方法classmethod不可以访问实例变量self.path
        try:
            cf = ConfigParser()
            cf.read(confpath)
            value = cf.get(section,option)
            return value
        except NoSectionError,e:
            print "section not found!"
        except NoOptionError,e:
            print "option not found!"
    @staticmethod
    def addconf(section,option,value):
        cf = ConfigParser()
        cf.read(confpath)
        if cf.has_section(section):
            cf.set(section,option,value)
        else:
            cf.add_section(section)
            cf.set(section,option,value)
        return

def randitem():
    items = []
    siturl = SuperConfig.readconf('siturl', 'homeurl')
    html = urllib2.urlopen(siturl).read()
    soup = BeautifulSoup(html)
    itemlist = soup.findAll('input',id= re.compile("^itemId"))
    for i in xrange(0,len(itemlist)):
        item = itemlist[i]['value']
        items.append(item)
    randitem = random.choice(items)
    #randitem = '9920140912496'
    itemid = "itemName_i_" + randitem
    return itemid

if __name__ == '__main__':
    randomitem()


    

