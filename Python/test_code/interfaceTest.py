# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
import json
import urllib
import urllib2
import hashlib
import time
import re
import unittest

#MD5 encode
#m=hashlib.md5()
#pswstr='6322939'
#m.update(pswstr.encode("gb2312"))
#psw=m.hexdigest()
#print(psw)

hbcode='1nk7t48qqae1'
nomessage=0
success=0
messagewrong=0
#大循环
count=1
#print u"你好".encode("GBK")
print u'------------------------------华丽丽的分割线------------------------------'
for itotal in range (count):
	print itotal+1,'/',count
	target1=requests.get('http://api.taomapt.com/http.do?action=getPhones&userID=13564873528&password=bc5010cefe7ebd7d2ba2b015d6daae16&projectID=938&size=1')
	json_result = json.loads(target1.text)
	#print(json_result)
	mobile=json_result['mobiles'][0]
	print '拿到号码 ：',mobile
	#成功拿到手机号mobile


	#拆红包+发验证码
	url='https://login.vip9999.com/?s=api4-redpacket-receive'

	postdata=urllib.urlencode({'mobile':mobile,'captcha':'','step':1,'code':hbcode,'from':'qq'})
	postdata=postdata.encode('utf-8')
	req=urllib2.Request(url,postdata)
	res=urllib2.urlopen(req)
	res_load=json.loads(res.read().decode())
	#res_load=json.loads(res.read().decode())
	
	print '拆红包成功',res_load['message'],'短信接收中………………'
  
	if(res_load['code']==-1):
		print 'send code fail!'



	#开始请求验证码answer了
	#8次循环
	time.sleep(5)
	for i in range (30):
		time.sleep(1)
		target2=requests.get('http://api.taomapt.com/http.do?action=getMessages&userID=13564873528&password=bc5010cefe7ebd7d2ba2b015d6daae16&projectID=938&mobile='+mobile+'&softAuthor=13564873528')
		json_result_message=json.loads(target2.text)
		'''
		if (json_result_message['msg']!=''):
			print(json_result_message['msg'])

			yzm=str(json_result_message['msg'][14]+json_result_message['msg'][15]+json_result_message['msg'][16]+json_result_message['msg'][17]+json_result_message['msg'][18])
			print(json_result_message)
			print('验证码已经拿到',yzm)
			break
		以上是老版本的做法了
		'''
		if (json_result_message['msg']!=''):
			print json_result_message['msg']
			yzmarr=re.findall(r'\d{5}',json_result_message['msg'])
			if len(yzmarr)>0:
				yzm=yzmarr[0]
				print '拿到验证码，耗时 -',i+1,'秒',yzm
				break
			else:
				print 'code match error'

		
		
		#print('这是第',i+1,'次拿数据','-------这次没拿到，等5秒再拿一次---------')
	if (json_result_message['msg']==''):
		nomessage=nomessage+1
		yzm=''
		print '获取验证码失败'
		addblack=requests.get('http://api.taomapt.com/http.do?action=addBlackMobiles&13564873528&password=bc5010cefe7ebd7d2ba2b015d6daae16&mobiles=mobile&projectID=938')
		#加黑名单
		
	#填码领红包，建立关系
	url2='https://login.vip9999.com/?s=api4-redpacket-receive'
	
	'''	postdata=urllib.urlencode({'mobile':mobile,'captcha':'','step':1,'code':hbcode,'from':'qq'})
	postdata=postdata.encode('utf-8')
	req=urllib2.Request(url,postdata)
	res=urllib2.urlopen(req)
	res_load=json.loads(res.read())
	#res_load=json.loads(res.read().decode())
	'''

	postdata2=urllib.urlencode({'mobile':mobile,'captcha':yzm,'step':2,'code':hbcode,'from':'qq'})
	postdata2=postdata2.encode('utf-8')
	req2=urllib2.Request(url2,postdata2)
	res2=urllib2.urlopen(req2)
	res2_load=json.loads(res2.read().decode())
	#print(res2_load['message'])
	if( res2_load['code'] == -1 ):
		print 'fail to updata code:',res2_load['message']
		messagewrong=messagewrong+1
	else:
		success=success+1
		print 'all success:',res2_load['message']
		#print(res2.status, res2.reason,'finsh')
		
	print '------------------------------华丽丽的分割线------------------------------'
messagewrong=messagewrong-nomessage
print 'success/nomessage/messagewrong/total'
print success,'/',nomessage,'/',messagewrong,'/',count


