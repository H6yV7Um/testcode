#coding=utf-8
from selenium import webdriver
import time,os


#访问百度
#System.setProperty("webdriver.ie.driver", "C:\\Program Files\\Internet Explorer\\IEDriverServer.exe");
#WebDriver driver = new InternetExplorerDriver();
#iedriver = "C:\\Program Files\\Internet Explorer\\IEDriverServer.exe"
#os.environ["webdriver.ie.driver"] = iedriver
driver=webdriver.Ie()
driver.get("http://www.baidu.com")
driver.maximize_window()
driver.implicitly_wait(30)

    
#搜索
driver.find_element_by_id("kw").send_keys("selenium")
driver.find_element_by_id("su").click()
time.sleep(3)

#将页面滚动条拖到底部
js="var q=document.documentElement.scrollTop=10000"
driver.execute_script(js)
time.sleep(3)


#将滚动条移动到页面的顶部
js="var q=document.documentElement.scrollTop=0"
driver.execute_script(js)
time.sleep(3)
driver.add_cookie({'name':'yinzhixin','value':'88888888'})
cookies=driver.get_cookies()
for cookie in cookies:
	print "%s -> %s" %(cookie['name'],cookie['value'])
driver.delete_cookie("yinzhixin")
for cookie in cookies:
	print "%s -> %s" %(cookie['name'],cookie['value'])
driver.quit()
