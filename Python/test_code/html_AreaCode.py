#coding: utf-8
''' this program use to capture the area code and area name,then we use the data to retrive the info
of the ID'''

from BeautifulSoup import BeautifulSoup as BS
import urllib2
import re
import time
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

ident = "110000198810230011"
iareacode = ident[0:6]
iseqcode = ident[-4:-1]
ibirth = ident[6:14]
sourceurl = "http://www.stats.gov.cn/tjsj/tjbz/xzqhdm/201504/t20150415_712722.html"
sourcepage = urllib2.urlopen(sourceurl).read()
shtml = BS(sourcepage)
ptags = shtml.findAll('p',limit=10)
areadict = {}
for i in range(len(ptags)):
    areacode = ptags[i].findAll('span')[0].text[0:6]
    areaname = ptags[i].findAll('span')[2].text
    areadict.setdefault(areacode, areaname)
print areadict
if iareacode in areadict:
    print areadict.get(iareacode,'not found!')
    if int(iseqcode) % 2==0:
        print "性别：女"
    else:
        print "性别：男"
    start = time.mktime(time.strptime(ibirth,'%Y%m%d')) #将字符串转化为时间戳
    x = time.localtime(start)   #时间戳封装为localtime
    birthday = time.strftime('%Y-%m-%d',x)  #将localtime转化为指定的字符串格式
    print "出生日期："+ birthday
    #print u"出生日期："+ ident[6:10]+u"年"+ident[10:12]+u"月"+ident[12:14]+u"日"
else:
    print "not found!"


    