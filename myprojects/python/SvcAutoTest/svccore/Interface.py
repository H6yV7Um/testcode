import json
import time
import copy
from hashlib import md5

import gevent
from gevent.pool import Group
import requests

from .CmdMapping import CommandMapping
from svcutils.Glogger import Glogger
from svcutils.tools import unit32_to_ip, bin_to_b64str


class CommonInterface:
    '''通用接口类，所有新增接口都补充到该类中'''
    logger = Glogger.getLogger()

    def __init__(self):
        self.client = None
        self.greenlets = Group()
        self.loop_check_interval = 1/100
        self.hb_interval = 30
        self.hb_version = 0
        self.app_id = "123"
        self.cli_type = 123
        #包头中的sequence字段，每发送后自增
        self.seq = 0
        #包头中的target字段
        self.target = 0

    def connect_to_svc(self, lbsip='172.16.16.25', port=6000):
        '''1.连接lbs获取acc地址列表 2.连接acc获取并更新心跳策略 '''
        self.etablish_con(ip=lbsip, port=port)
        acc_list = self.get_acc_list()
        acc_ip, acc_port = self.get_first_accaddr(acc_list)
        self.etablish_con(ip=acc_ip, port=acc_port, acc=True)
        self.start_heart_beat()
        self.update_heartbeat()
        self.report_hb_version()
        self.client_access()
    
    def connect_to_acc(self, ip, port):
        '''连接指定的acc server'''
        self.etablish_con(ip, port, acc=True)
        self.start_heart_beat()
        self.report_hb_version()
        self.update_heartbeat()
        self.client_access()

    def get_first_accaddr(self, acc_list):
        try:
            acc_ip = unit32_to_ip(acc_list['acc_addrs'][0]['ip'])
            acc_port = int(acc_list['acc_addrs'][0]['ports'][0])
        except KeyError:
            self.close()
            raise KeyError("Received acc list is empty, unable to continue,exit!") from None
        return acc_ip, acc_port
    
    def start_heart_beat(self):
        def _heart_beat():
            self.logger.debug("Heart beat thread started!")
            try:
                while self.client:
                    self.send_data(CommandMapping.HeartBeat, {})
                    gevent.sleep(self.hb_interval)
                self.logger.debug("Socket close, stop sending heart beat.")
            except Exception as e:
                self.logger.error("HeartBeat greenlet error:{}".format(e.args))
        self.greenlets.spawn(_heart_beat)

    def get_response(self, cmd, timeout=5):
        '''获取指定cmd的响应结果'''
        try:
            timer = gevent.Timeout(timeout)
            timer.start()
            while True:
                if cmd in self.client.callback_dict:
                    result = self.client.callback_dict.pop(cmd)
                    return result
                gevent.sleep(0.01)             
        except gevent.Timeout as t:
            if t is timer:
                return {'timeout': timeout}
            else:
                raise
        finally:
            timer.cancel()

    def close(self):
        if self.client:
            self.client.close()
        self.client = None    
        self.greenlets.kill()

    def update_data(self, d1, d2):
        for key in d2.keys():
            if key not in d1:
                raise KeyError("Default param:{} has no key {}".format(d1, key))
        d1.update(d2)
        return d1

    def get_heartbeat_conf(self, **kwargs):
        '''
        根据客户端类型获取对应的心跳配置
        @return: {"version":1,"send_sec":15,"check_sec":30,"bt_timeout":60}
        '''
        data = {"cli_type": 0}
        self.update_data(data, kwargs)
        self.send_data(CommandMapping.GetHeartBeatConf, data)
        result = self.get_response(CommandMapping.GetHeartBeatConfRsp)
        return result

    def update_heartbeat(self):
        '''根据获取的心跳配置更新本地的心跳发送策略'''
        try:
            conf = self.get_heartbeat_conf()['body']
            self.hb_interval = int(conf["send_sec"])
            self.hb_version = int(conf["version"])
        except KeyError:
            self.logger.error("Get HB conf timeout, use the default 30s")

    def report_hb_version(self):
        '''获取到心跳配置后上报心跳版本号'''
        data = {"version": self.hb_version}
        self.send_data(CommandMapping.ClientReportHbConf, data)
        return self.get_response(CommandMapping.ClientReportHbConfRsp)

    def client_access(self, **kwargs):
        '''客户端接入，要确保所有传入的app_id和cli_type都一致'''
        data = {
            "app_id": self.app_id,
            "cli_type": self.cli_type,
            "cli_version": "16",
            "cli_os_ver": 0,
            "cli_mac": "test",
            # "device_id": b'119'
        }
        self.update_data(data, kwargs)
        self.send_data(CommandMapping.ClientAccess, data)
        return self.get_response(CommandMapping.ClientAccessRsp)

    def login(self, **kwargs):
        '''账号登陆,该服务暂时未启用，后期可能会用到'''
        data = {
            "account_type": 2,
            "account": "123123",
            "auth_ticket": md5('hello'.encode()).hexdigest(),
            "online_status": 1,
            "cli_type": 0,
            # "device_id": bin_to_b64str(b'123'),
            "app_id": '0x0001'
        }
        self.update_data(data, kwargs)
        self.send_data(CommandMapping.UserLogin, data)
        return self.get_response(CommandMapping.UserLoginRsp)

    def anonymous_login(self, **kwargs):
        '''匿名登陆'''
        data = {
            "uid": 666,
            "online_status": 1,
            "cli_type": self.cli_type,
            # "device_id": b'234',
            "app_id": self.app_id
        }
        self.update_data(data, kwargs)
        self.send_data(CommandMapping.AnonymousLogin, data)
        return self.get_response(CommandMapping.AnonymousLoginRsp)

    def get_anonymous_uid(self, **kwargs):
        '''获取匿名登陆账号'''
        self.send_data(CommandMapping.GetAnonymousUid, {})
        return self.get_response(CommandMapping.GetAnonymousUidRsp)

    def token_login(self, **kwargs):
        '''token登陆'''
        data = {
            "uid": self.uid,
            "token": self.token,
            "online_status": 1,
            "cli_type": self.cli_type,
            # "device_id": bin_to_b64str(b'123'),
            "app_id": self.app_id
        }
        self.update_data(data, kwargs)
        self.send_data(CommandMapping.TokenLogin, data)
        return self.get_response(CommandMapping.TokenLoginRsp)

    def login_complete(self):
        self.send_data(CommandMapping.LoginComplete, {})

    def logout(self):
        '''用户登出'''
        self.send_data(CommandMapping.UserLogout, {})
        response = self.get_response(CommandMapping.UserLogoutRsp)
        if "timeout" in response:
            return False
        return True

    def update_token(self, **kwargs):
        '''通过refresh_token更新token'''
        data = {
            "refresh_token": "123",
            "cli_type": 0,
            "device_id": "123"
            }
        self.update_data(data, kwargs)
        self.send_data(CommandMapping.UpdateToken, data)
        return self.get_response(CommandMapping.UpdateTokenRsp)

    def update_refresh_token(self, **kwargs):
        '''通过refresh token更新refresh token'''
        data = {
            "refresh_token": "123",
            "cli_type": self.cli_type,
            # "device_id": '123',
            "app_id": self.app_id
            }
        self.update_data(data, kwargs)
        self.send_data(CommandMapping.UpdateRefreshToken, data)
        return self.get_response(CommandMapping.UpdateRefreshTokenRsp)

    def enter_class(self, cid, **kwargs):
        '''进入教室'''
        data = {
            "user_name": "user1",
            "cus_data": "test"
        }
        self.target = cid
        self.update_data(data, kwargs)
        self.send_data(CommandMapping.EnterClass, data)
        return self.get_response(CommandMapping.EnterClassRsp)

    def enter_class_notify(self):
        '''接收某个用户进入教室的通知'''
        return self.get_response(CommandMapping.EnterClassNotify)

    def enter_class_complete(self):
        self.send_data(CommandMapping.EnterClassComplete, {})
    
    def leave_class(self):
        '''退出教室'''
        self.send_data(CommandMapping.LeaveClass, {})
        return self.get_response(CommandMapping.LeaveClassRsp)

    def leave_class_notify(self):
        '''退出教室通知'''
        return self.get_response(CommandMapping.LeaveClassNotify)

    def force_leave_class(self, **kwargs):
        '''强制某个用户退出教室'''
        data = {
            "uid": 123,
            "reason": 0
        }
        self.update_data(data, kwargs)
        self.send_data(CommandMapping.ForceLeaveClass, data)
        return self.get_response(CommandMapping.ForceLeaveClassRsp)

    def force_leave_class_notify(self):
        '''强制退出教室通知'''
        return self.get_response(CommandMapping.ForceLeaveClassNotify)

    def shutdown_class(self, **kwargs):
        '''关闭教室'''
        data = {"reason": 0}
        self.update_data(data, kwargs)
        self.send_data(CommandMapping.CloseClass, data)
        return self.get_response(CommandMapping.CloseClassRsp)

    def shutdown_class_notify(self):
        '''关闭教室通知'''
        return self.get_response(CommandMapping.CloseClassNotify)

    def send_chat_message(self, **kwargs):
        '''用户在教室内发送聊天消息'''
        data = {
            "cli_seq": 0,
            "send_tm": int(time.time()),
            "type": 0,
            "option": "font=宋体",
            "chat_msg": "hello world"
        }
        self.update_data(data, kwargs)
        self.send_data(CommandMapping.UserSendMessage, data)
        return self.get_response(CommandMapping.UserSendMessageRsp)

    def receive_chat_message(self):
        '''用户在教室内接收消息'''
        message = self.get_response(CommandMapping.UserReceiveMessage)
        if "timeout" not in message:
            data = {"msg_id": message["body"]["msg_id"]}
            self.send_data(CommandMapping.UserReceiveMessageRsp, data)
        return message

    def receive_offline_chat_message(self):
        '''用户接收离线消息'''
        return self.get_response(CommandMapping.ReceiveOfflineMessage)

    def hand_up(self):
        '''举手'''
        self.send_data(CommandMapping.HandUp, {})
        return self.get_response(CommandMapping.HandUpRsp)

    def hand_down(self):
        '''放手'''
        self.send_data(CommandMapping.HandDown, {})
        return  self.get_response(CommandMapping.HandDownRsp)

    def change_speak_list(self, **kwargs):
        '''修改发言列表'''
        data = {
            "op_type": 1,
            "target_uid": 123
        }
        self.update_data(data, kwargs)
        self.send_data(CommandMapping.ChangeSpeakOrder, data)
        return self.get_response(CommandMapping.ChangeSpeakOrderRsp)

    def change_speak_list_notify(self):
        '''修改发言列表通知'''
        return self.get_response(CommandMapping.ChangeSpeakOrderNotify)

    def http_request(self, url, method, data):
        self.logger.info("Send request:URL-{} Method-{} Data-{}".format(url, method, data))
        response = requests.request(method, url, params=data, json=data)
        status = response.status_code
        if status == requests.codes.ok:
            r = response.json()
            self.logger.info("Reponse from {}: {}".format(url, r))
        else:
            r = str(response.content)
            self.logger.error("Request fail:http_code:{},msg:{}".format(status, r))
        return r

    class HttpLoginError(Exception):
        pass

    def http_login(self, **kwds):
        '''http账号密码登陆接口'''
        
        url = "http://api.mebutoo.com/namelogin"
        data = {
            "uname":"test1916",
            "password":"123",
            "online_status":1,
            "ctype":self.cli_type,
            "app_id": self.app_id
        }
        self.update_data(data, kwds)
        response = self.http_request(url, 'POST', data)
        if response.get('rsp_code') != 0:
            raise HttpLoginError(response)
        self.token = response['token']
        self.refresh_token = response['refresh_token']
        self.uid = response['uid']
        return response

    def http_regist(self, **kwds):
        '''http用户注册接口'''
        url = "http://api.mebutoo.com/nameregist"
        data = {
            "uname":"test1916",
            "password":"123",
            # "device_id": "123",
            "app_id": self.app_id,
            "client_version": "1.0",
            "client_type": self.cli_type
        }
        self.update_data(data, kwds)
        response = self.http_request(url, 'POST', data)
        return response

    def http_anonymous_login(self, **kwds):
        url = "http://api.mebutoo.com/anylogin"
        data = {
            "uid": self.http_get_anonymous_uid(),
            "online_status": 1,
            "ctype": self.cli_type,
            # "deviceid": "123",
            "app_id": self.app_id
        }
        self.update_data(data, kwds)
        response = self.http_request(url, 'POST', data)
        if response.get('rsp_code') != 0:
            raise HttpLoginError(response)
        self.token = response['token']
        self.refresh_token = response['refresh_token']
        self.uid = response['uid']
        return response
    
    def http_get_anonymous_uid(self, **kwds):
        url = "http://api.mebutoo.com/anyregist"
        data = {"app_id": self.app_id}
        self.update_data(data, kwds)
        r = self.http_request(url, 'GET', data)
        uid = r['uid'] if r.get('rsp_code', 0)==0 else -1
        return uid 

    def http_get_state(self, **kwds):
        url = "http://api.mebutoo.com/oauthstate"
        data = {
            "cli_type": self.cli_type,
            # "device_id":"123",
            "app_id": self.app_id,
            "target":123
        }
        self.update_data(data, kwds)
        return self.http_request(url, 'GET', data)




    