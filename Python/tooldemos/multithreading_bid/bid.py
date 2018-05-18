#coding:utf-8
__author__ = 'yinzx'
import urllib
import urllib2
import json
import cookielib
import sys
import os
import requests
import threading
import ast
try:
    path = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(path)
    from common import SuperPath, SuperConfig
except ImportError, e:
    print "import common failed!"

#环境开关
env = SuperConfig.readconf('switch', 'env')
s = requests.Session()
#s.keep_alive = False   #requests默认是长连接，可通过此设置修改连接方式
#requests.adapters.DEFAULT_RETRIES = 5  #设置重试连接次数


def login():
    url = SuperConfig.readconf(env, 'loginurl')
    data = json.loads(SuperConfig.readconf(env, 'logindata'))   #将json字符串转换为dict对象，json字符串必须用双引号，否则解码报错
    #print data
    #print type(data)
    response = s.post(url, data=data)
    if response.text[2:9] == 'success':
        print response.text
        return True
    else:
        print response.text
        return False


def bid(low, top):
    while True:
        r = s.get(SuperConfig.readconf(env, 'pushurl'))
        response = json.loads(r.text[3:].strip('()'))
        #print response
        if response['m2']:
            curprice = response['m2'][0]['a']
            print curprice
            browsertime = response['m2'][0]['c']
            if low <= curprice < top:
                biddata = json.loads(SuperConfig.readconf(env, 'biddata') % browsertime)
                #print biddata
                bidresponse = s.post(SuperConfig.readconf(env, 'bidurl'), data=biddata).text
                print bidresponse
            elif curprice >= top:
                print 'auction is over!'
                break
        else:
            print 'auction do not start!'


def start_thread(l, t, *timer):
    for i in xrange(10):
        if timer and isinstance(timer[0], int):
            tr = threading.Timer(timer[0], bid, args=(l, t))
            print "wait %s seconds to start thread %s" % (timer[0], i)
        else:
            tr = threading.Thread(target=bid, args=(l, t))
            print "------------------Thread %s start!---------------------" % i
            print "l:%s,t:%s" % (l, t)
        tr.setDaemon(True)
        tr.start()
        #tid = tr.ident     #获取线程ID

    tr.join()
    print 'All threads have been done!'

if __name__ == '__main__':
    low = int(SuperConfig.readconf(env, 'low'))
    top = int(SuperConfig.readconf(env, 'top'))
    timer = SuperConfig.readconf(env, 'timer')
    if timer != 'none':
        timer = int(timer)
    if login():
        start_thread(low, top, timer)
    else:
        print "login failed!"

