#-*- coding:utf-8 -*-
''' wxpython test!'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import unittest, time, re
import threading
import pytesseract
import Image
import urllib2
import wx

info = u'欢迎使用！'
def bidtest(itemid,login,pwd):        #定义参数：拍品ID，出价次数上限，开拍定时
    global info
    driver = webdriver.Chrome()
    driver.implicitly_wait(30)
    driver.get('http://pai.suning.com/shanpai/detail/d/%s-1.htm' %itemid)
    driver.maximize_window()
    mainhandle = driver.current_window_handle   #主窗口句柄
    print mainhandle        #调试信息：确认主窗口句柄是否获取到
    driver.find_element_by_id("depositBtn_%s" %itemid).click()
    time.sleep(2)
    try:
        driver.switch_to_frame("iframeLogin")       #切换到登陆窗口
    except NoSuchFrameException,e:
        info = u'未找到缴纳保证金按钮，拍卖已全部结束'
        return
    driver.find_element_by_id("loginName").clear()
    driver.find_element_by_id("loginName").send_keys(login)
    driver.find_element_by_id("loginPassword").clear()
    driver.find_element_by_id("loginPassword").send_keys(pwd)
    driver.find_element_by_id("loginBtn").click()
    driver.switch_to_window(mainhandle)
    time.sleep(3)
    try:
    #driver.find_element_by_link_text(u"出价").click()
        WebDriverWait(driver,60).until(lambda the_driver: the_driver.find_element_by_name('detail_action_bid_chujia').is_displayed())
    except TimeoutException,e:
        info = u'等待超时，请重试！'
        return
        
    display = driver.find_element_by_name('detail_action_bid_chujia').is_displayed()
    try:
        while display == True:
        #for i in range(num):        #后边需改为while循环，判断出价按钮不显示时停止循环
            driver.find_element_by_name('detail_action_bid_chujia').click()
    except NoSuchElementException,e:
        info = u'拍卖未开始或已结束！'
        return
    except ElementNotVisibleException,msg:
        info = u'出价按钮不可见，本轮拍卖已结束，请等待下轮'
        return
    finally:
        time.sleep(3)
        #driver.quit()      #关闭浏览器驱动和浏览器窗口

class TextFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u"闪拍刷价器",size=(300,300))
        panel=wx.Panel(self,-1)
        
        #添加用户名 文本输入框
        self.IDLabel=wx.StaticText(panel,-1,u"拍品编码:")
        self.IDText=wx.TextCtrl(panel,-1,u"输入拍品ID",size=(175,-1))
        #设置默认的插入点，整数索引，开始位置为0
        self.IDText.SetInsertionPoint(0)
        
        #添加出价次数 输入框
        #numlabel=wx.StaticText(panel,-1,u"出价次数:")
        #self.numText=wx.TextCtrl(panel,-1,u'输入次数',size=(175,-1))
        #self.numText.SetInsertionPoint(0)
        
        #添加定时运行时间 文本输入框
        #timeLabel=wx.StaticText(panel,-1,u"定时时间:")
        #self.timeText=wx.TextCtrl(panel,-1,u'输入时间（默认分钟数）',size=(175,-1))
        #self.timeText.SetInsertionPoint(0)
        
        #添加易购账号 文本输入框
        userLabel=wx.StaticText(panel,-1,u"账号:")
        self.userText=wx.TextCtrl(panel,-1,u'13681028312',size=(175,-1))
        self.userText.SetInsertionPoint(0)
        
        #添加易购密码 文本输入框
        passwdLabel=wx.StaticText(panel,-1,u"密码:")
        self.passwdText=wx.TextCtrl(panel,-1,'xin044605',size=(175,-1),style = wx.TE_PASSWORD)
        self.passwdText.SetInsertionPoint(0)
                               
        #添加调用按钮
        self.bidbutton=wx.Button(panel,-1,u'开始',pos=(150,150))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.bidbutton)
        self.bidbutton.SetDefault()
        
        #添加提示信息文本区
        self.infotext = wx.StaticText(panel,-1,info)
    
        #用sizer控制界面布局,添加页面控件
        sizer=wx.FlexGridSizer(cols=2,hgap=6,vgap=6)
        sizer.AddMany([userLabel,self.userText,passwdLabel,self.passwdText,self.IDLabel,self.IDText,self.bidbutton,self.infotext])
        panel.SetSizer(sizer)
    def OnClick(self,event):
        global info
        ItemID=self.IDText.GetValue()
        #num=int(self.numText.GetValue())
        #mintime=self.timeText.GetValue()
        login=self.userText.GetValue()
        pwd=self.passwdText.GetValue()
        #print ItemID + num      #调试：确认参数是否获取到
        bidtest(ItemID,login,pwd)
        info = u"竞拍中...."
  
class MyApp(wx.App):
    def OnInit(self):
        frame=TextFrame()
        frame.Show(True)
        return True #如果没有返回值，结果一闪而过，不能驻留窗口
     
       
def main():
    app=MyApp()
    app.MainLoop()
    
if __name__=="__main__":
    main()