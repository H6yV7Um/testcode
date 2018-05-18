#coding:utf-8
import requests
from BeautifulSoup import BeautifulSoup
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

''''S码推送接口测试Demo'''

def send():
    '''请求报文'''
    data = '''
        <MbfService xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <input1>
        <MbfHeader>
            <ServiceCode>ActivityReminder</ServiceCode>
            <Operation>activityReminder</Operation>
            <AppCode>NMPS</AppCode>  
            <UId>414d5120514d5f6c6f63616c202020203baa474c20012802</UId>
            <AuthId>B2C;password</AuthId>
        </MbfHeader>
        <MbfBody>
                <appCode>NMPS</appCode>
                <templateId>10000040</templateId>
                <msgType>2</msgType>
                <smsContentTemplate></smsContentTemplate>
                <msgName>消息提醒测试</msgName>
                <msgContentTemplate>消息提醒测试消息提醒测试消息提醒测试消息提醒测试消息提醒测试</msgContentTemplate>
                <pageName>测试</pageName>
                <skipLink>http://www.suning.com</skipLink>
        </MbfBody>
    </input1>
</MbfService>
'''
    url = 'http://smasit.service.cnsuning.com/sma-service/esb/activityReminder.htm'
    response = requests.post(url, data=data).text
    return response
def check():
    xml = str(send())
    #tree = ET.parse("test.xml") #从xml文件读取
    #root = tree.getroot()  #读取文件后获取root节点
    root = ET.fromstring(xml)
    #status = root.findall('.//Status').text   #xpath定位元素，findall返回列表
    status = root.find('.//Status').text
    rescode = root.find('.//resCode').text
    print status,rescode
    if status == 'COMPLETE' and rescode==1:
        return 'pass'
    else:
        return 'fail'

def output():
    ''''返回报文'''
    output = '''
        <?xml version="1.0" encoding="UTF-8"?>
        <MbfService>
        <output1>
        <MbfHeader>
          <ServiceCode>ActivityReminder</ServiceCode>
          <Operation>activityReminder</Operation>
          <AppCode>NMPS</AppCode>
          <UId>414d5120514d5f6c6f63616c202020203baa474c20012802</UId>
          <ServiceResponse>
            <Status>COMPLETE</Status>
          </ServiceResponse>
        </MbfHeader>
        <MbfBody>
          <resCode>1</resCode>
        </MbfBody>
        </output1>
        </MbfService>
        '''
    return output
    

if __name__ == '__main__':
    print "--------------------------result-----------------------------"
    print check()
