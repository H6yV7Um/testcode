#coding:utf-8
import urllib
import urllib2
import requests
import cookielib
import os

''' suning login test!'''
#url
loginurl = 'https://passport.suning.com/ids/login'
verifycodeurl = 'https://passport.suning.com/ids/needVerifyCode'

#data
verifydata = urllib.urlencode({'username':'13681028312'})

cookie = cookielib.CookieJar()
cj = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(cj)

firstlogin = opener.open(loginurl)
print cookie
for ck in cookie:
    cookies = ''' 
        __wmv=1450252581.1; __wms=1450254381; _fp_t_=123,1450252651003; _portoData=1868dfdb-f3dd-4df1-98d5-5604a324519e; _device_session_id=p_03cb4010-a83d-4c13-b102-d13f7ab2b738; _snma=1%7C145025257318675410%7C1450252573186%7C1450252573186%7C1450252648273%7C2%7C1; _snmc=1; _snsr=direct%7Cdirect%7C%7C%7C; _snmb=145025257318672478%7C1450252648491%7C1450252648273%7C2; _snmp=145025264827320087; _ga=GA1.2.325052665.1450252590; _gat=1; WC_PERSISTENT=Dr%2f2hSM0X0t5sd6m87QSYXy7xjw%3d%0a%3b2015%2d12%2d16+15%3a56%3a34%2e099%5f1450252594098%2d56253%5f10052; WC_SESSION_ESTABLISHED=true; WC_AUTHENTICATION_-1002=%2d1002%2cjnefR7OrhqcfkBcZd%2bCp0iOYFhA%3d; WC_ACTIVEPOINTER=%2d7%2c10052; WC_USERACTIVITY_-1002=%2d1002%2c10052%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2cHfu4AyHVyTEH5%2fLoLwRp0%2frI3cWrBquyD%2fSaNhM3UZ0lBXgogKjO%2fnlhmMBqRneXQjTSWuCB4hcc%0a2xWGNR%2bKeJqOf4Qk3VWp48uPUqnhkivRIO3xZnYYaEqjRp4EEKh76mqnqWam0%2bClp%2fY%2bzt%2fu5Q%3d%3d; WC_GENERIC_ACTIVITYDATA=[20000146622180957%3atrue%3afalse%3a0%3auF7dX1rqvuIveQAOTHBbyc69cj0%3d][com.ibm.commerce.context.audit.AuditContext|1450252594098%2d56253][com.ibm.commerce.store.facade.server.context.StoreGeoCodeContext|null%26null%26null%26null%26null%26null][CTXSETNAME|Store][com.ibm.commerce.context.globalization.GlobalizationContext|%2d7%26CNY%26%2d7%26CNY][com.ibm.commerce.catalog.businesscontext.CatalogContext|null%26null%26false%26false%26false][com.suning.commerce.context.common.SNContext|9173%26%2d1%26null%26172%2e19%2e136%2e192%26null%26null%26null%26null%26null%26null%26null%26null%26null%26null%26null%26null%26null%26null%26null%26null%26null%26null][com.ibm.commerce.context.base.BaseContext|10052%26%2d1002%26%2d1002%26%2d1][com.ibm.commerce.context.experiment.ExperimentContext|null][com.ibm.commerce.context.entitlement.EntitlementContext|10007%2610007%26null%26%2d2000%26null%26null%26null][com.ibm.commerce.giftcenter.context.GiftCenterContext|null%26null%26null]
    ''' 
print cookies
headers = {
    'Host':'passport.suning.com',
    'Upgrade-Insecure-Requests':'0',
    'Cookie':cookies
}
verifystatus = urllib2.urlopen(urllib2.Request(verifycodeurl,verifydata,headers=headers)).read()
print verifystatus

'''os.path.dirname  testing'''
filedir = os.path.dirname(os.path.abspath(__file__))
print filedir