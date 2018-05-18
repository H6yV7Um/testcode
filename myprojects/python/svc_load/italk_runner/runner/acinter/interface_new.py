#coding:utf-8
import time
import inspect
import random
from collections import defaultdict, deque

import gevent

import acinter.SocPack
from acinter.SocPack import commandID
from acinter.MainSocket import MainSocket
from acinter.Glogger import Glogger
from runner_settings import SVC_TIMEOUT


class acsim(object):
    '''this is a object between meassage control object and socket object.
    '''
    def __init__(self):
        self.connection = None
        self.is_login = False
        self.callback_dict = defaultdict(deque)

    def wait_callback_value(self, commandID, timeout):
        #timeout为数据库中统一设置的值,调用方传值也不会生效
        try:
            timer = gevent.Timeout(SVC_TIMEOUT)
            timer.start()
            while True:
                if commandID in self.callback_dict and len(self.callback_dict[commandID]):
                    result = self.callback_dict[commandID].popleft()
                    return result
                gevent.sleep(0.001)       
        except gevent.Timeout as e:
            if e is timer:
                return {'result': 'time out'}
            return {"error": e.args}
        finally:
            timer.cancel()

    # 传送给底层调用的回调函数，将回调数据放置在self.callback_dict这个字典里
    def callback_data(self, commandID, data):
        # self.callback_dict[commandID] = data
        self.callback_dict[commandID].append(data)

    # 转换字符串IP地址为整数形格式
    def __getIPbyUint32(self, n):
        return '%d.%d.%d.%d' % (n>>24,(n>>16)&0x00ff,(n>>8)&0x0000ff,n&0x000000ff)

    def connect_italk(self, lbs_ip=None, lbs_port=None):
        self.connect_lbs(ip=lbs_ip, port=lbs_port)
        acc_list = self.request_lbs()['Server']
        host = self.__getIPbyUint32(acc_list[0]['AccIP'])
        port = acc_list[0]['AccPort'][0]
        self.connect_acc(host, port)

    def disconnect_italk(self):
        self.connection.closeSocket()
        self.connection = None
        self.callback_dict = defaultdict(deque)

    def connect_lbs(self, ip=None, port=None):
        self.connection = MainSocket(callback_func=self.callback_data)
        self.connection.init(host=ip, port=port)

    def request_lbs(self, FailedServerNum=0, ServerIP=0, IsManualSetting=0,
                    ISPIdx=0, LocationCode=0, timeout=6):
        data = {
            "FailedServerNum": FailedServerNum,
            "ServerIP": ServerIP,
            "IsManualSetting": IsManualSetting,
            "ISPIdx": ISPIdx,
            "LocationCode": LocationCode
        }
        self.connection.sendData(
            data,
            acinter.SocPack.commandID.LoadBalancing
        )
        result = self.wait_callback_value(
            acinter.SocPack.commandID.LoadBalancing,
            timeout
        )
        return result

    def connect_acc(self, ip=None, port=None, ClientType=1, ClientVer=b'v1.00.0001',
                    ClientFlag=b'AutoTest', ClientOSFlag=chr(0).encode(), timeout=6):
        '''如无传入acc ip和port，保持None网络接模块讲默认选择lbs返回的第一个acc服务器。
           建立与acc服务器之间的socket连接
           ClientType取值范围:
            0x01-PC客户端 0x02-Andorid客户端 0x03-IPhone客户端
            0x04-IPad客户端 0x05-Flash白板客户端 0x06-Flash AC客户端
            0x07-Mac客户端 0x08-多说Andorid客户端 0x09-多说IPhone客户端
            0x0A-B2S Andorid客户端 0x0B-B2SIPhone客户端 0x10-Web端
        '''
        if self.connection:
            self.disconnect_italk()
        self.connection = MainSocket(callback_func=self.callback_data)
        self.connection.build_socket_to_acc(acc_ip=ip, acc_port=port)
        data = {
            "ClientType": ClientType,
            "ClientVer": ClientVer,
            "ClientFlag": ClientFlag,
            "ClientOSFlag": ClientOSFlag
        }
        self.connection.sendData(
            data,
            acinter.SocPack.commandID.ClientConnect
        )
        result = self.wait_callback_value(
            acinter.SocPack.commandID.ClientConnect,
            timeout
        )
        return result

    def login(self, Account='123', AccountType=0, AuthTicketLength=0,
              AuthTicket=[1], DefaultStatus=0, ExternPassword='no',
              timeout=6):
        data = {
            "AccountType": AccountType,
            "Account": str(Account).encode(),
            "AuthTicketLength": AuthTicketLength,
            "AuthTicket": [chr(i).encode() for i in AuthTicket],
            "DefaultStatus": DefaultStatus,
            "ExternPassword": ExternPassword.encode()
        }
        self.connection.sendData(
            data,
            acinter.SocPack.commandID.ClientLogin,
        )
        self.is_login = True

        result = self.wait_callback_value(
            acinter.SocPack.commandID.ClientLogin,
            timeout
        )
        return result

    def login_complete(self):
        data = {}
        self.connection.sendData(
            data,
            acinter.SocPack.commandID.ClientLoginComplete,
        )

    def logout(self, timeout=6):
        data = {}
        self.connection.sendData(
            data,
            acinter.SocPack.commandID.ClientLogout,
        )
        self.is_login = False
        # result = self.wait_callback_value(
        #     acinter.SocPack.commandID.ClientLogout,
        #     timeout
        # )
        # return result

    # 使用客户端使用进入教室的默认函数
    def enter_classroom(self, *args, **kwds):
        return(self.enter_classroom_v4(*args, **kwds))

    # 进入教室协议v4
    def enter_classroom_v4(self, SID=0, CID=0, CourseID=0, UserRole=1,
                           Reserved_1=1, Reserved_2=1, Reserved_3=1,
                           UserSwitchFlag=0, UserName=b"test user",
                           AVSDKNum=2, AVSDK=(b'2',b'7'),
                           UserCusData=b"test", timeout=6):
        data = {
            "SID": int(SID),
            "CID": int(CID),
            "CourseID": int(CourseID),
            "UserRole": chr(UserRole).encode(),
            "Reserved_1": chr(Reserved_1).encode(),
            "Reserved_2": chr(Reserved_2).encode(),
            "Reserved_3": chr(Reserved_3).encode(),
            "UserSwitchFlag": int(UserSwitchFlag),
            "UserName": UserName,
            "AVSDKNum": int(AVSDKNum),
            "AVSDK": [b'2',b'7'],
            "UserCusData": UserCusData
        }
        self.connection.sendData(
            data, acinter.SocPack.commandID.EnterClass_v4
        )
        # 使用进入教室协议v4的返回确认与v2的是一致的
        result = self.wait_callback_value(
            acinter.SocPack.commandID.EnterClass,
            timeout
        )
        return result

    def get_enter_class_notify(self, timeout=6):
        self.__is_in_class = True
        result = self.wait_callback_value(
            acinter.SocPack.commandID.EnterClassNotify,
            timeout
        )
        return result

    def enter_class_complete(self, SID=1, CID=None, CourseID=1):
        data = {
            "SID": int(SID),
            "CID": int(CID),
            "CourseID": int(CourseID)
        }
        self.connection.sendData(
            data,
            acinter.SocPack.commandID.EnterClassComplete
        )

    def leave_classroom(self, SID=0, CID=None, CourseID=0, timeout=6):
        data = {"SID": SID, "CID": CID, "CourseID": CourseID}
        self.connection.sendData(
            data, acinter.SocPack.commandID.LeaveClass
        )
        self.__is_in_class = False
        #无需等待结果
        # result = self.wait_callback_value(
        #     acinter.SocPack.commandID.LeaveClass,
        #     timeout
        # )
        # return result

    def chat_in_classroom(self, CID=None, SentTime=0, Option='',
                          Text='testmessage'):
        data = {
            "CID": int(CID),
            "SentTime": SentTime,
            "Option": bytes(Option.encode()),
            "Text": bytes(Text.encode())
        }
        self.connection.sendData(
            data, acinter.SocPack.commandID.ClassChatMessage,
        )

    def recevice_chat_message_ack(self, timeout=6):
        result = self.wait_callback_value(
            acinter.SocPack.commandID.ClassChatMessageAck,
            timeout
        )
        return result

    def get_classroom_chat_messages(self, timeout=6):
        result = self.wait_callback_value(
            acinter.SocPack.commandID.ClassChatMessage,
            timeout
        )
        return result

    def hand_up(self, CID=None, timeout=6):
        data = {"CID": int(CID)}
        self.connection.sendData(
            data, acinter.SocPack.commandID.ClassHandUp,
        )
        result = self.wait_callback_value(
            acinter.SocPack.commandID.ClassHandUp,
            timeout
        )
        return result

    def hand_down(self, CID=None, timeout=6):
        data = {"CID": int(CID)}
        self.connection.sendData(
            data, acinter.SocPack.commandID.ClassHandDown,
        )
        result = self.wait_callback_value(
            acinter.SocPack.commandID.ClassHandDown,
            timeout
        )
        return result

    # 获取更换教材通知
    def recevice_textbook_page(self, timeout=6):
        result = self.wait_callback_value(
            acinter.SocPack.commandID.TextbookPage,
            timeout
        )
        return result

    # 发送更换演示文档页的请求
    def change_textbook_page(self, CID=None, Type=1, TotalPage=20,
                             CurrentPage=10, timeout=6):
        data = {
            "CID": int(CID),
            "Type": chr(Type).encode(),
            "TotalPagePrefix": chr(0).encode(),
            "TotalPage": chr(TotalPage).encode(),
            "CurrentPagePrefix": chr(0).encode(),
            "CurrentPage": chr(CurrentPage).encode(),
        }
        self.connection.sendData(
            data,
            acinter.SocPack.commandID.ChangeTextbookPage
        )
        result = self.wait_callback_value(
            acinter.SocPack.commandID.ChangeTextbookPage,
            timeout
        )
        return result

    # 获取更换教材页码通知
    def recevice_change_textbook_page_notify(self, timeout=6):
        result = self.wait_callback_value(
            acinter.SocPack.commandID.ChangeTextbookPageNotify,
            timeout
        )
        return result
    
    def callService(self, **data):
        '''
        @author：尹志鑫
        @description:调用服务的通用方法
        @param:
        req_type: 1-接口有入参和出参时则调用sendData
                  2-接口有入参无出参时直接退出，无需等待返回
                  其他-接口无入参时，直接等待接口返回值
        '''
        command = data.pop("command", None)
        reqtype = data.pop("reqtype", None)
        timeout = data.pop("timeout", 6)
        if reqtype == 1:
            self.connection.sendData(
                data,
                command
                )
        elif reqtype == 2:
            self.connection.sendData(
                data,
                command
                )
            return True
        result = self.wait_callback_value(
            command,
            timeout
            )
        return result

    def get_pen_color(self, **kwargs):
        data = {
            "command": commandID.GetPenColor,
            "reqtype": 1,
            "timeout": 6,
            "CID": 1
            }
        data.update(kwargs)
        result = self.callService(**data)
        return result

    def add_white_board(self, **kwargs):
        GraphicAdd = [{
            "ClientSeq": 1,
            "GraphicStrData": b"test",
            "GraphicByteDataLen": 2,
            "GraphicByteData": (1, 2)
            }]
        data = {
            "command": commandID.AddWhiteBoardData,
            "reqtype": 1,
            "timeout": 6,
            "CID": 1,
            "TextbookID": 666,
            "TextbookType": b'1',
            "Page": 1,
            "GraphicNum": 1,
            "GraphicDataItems": GraphicAdd
            }
        data.update(kwargs)
        result = self.callService(**data)
        return result

    def modify_white_board(self, **kwargs):
        GraphicModify = [{
            "ServerSeq": 1,
            "GraphicStrData": b"test",
            "GraphicByteDataLen": 1,
            "GraphicByteData": (b'3', b'9')
            }]
        data = {
            "command": commandID.ModifyWhiteBoardData,
            "reqtype": 1,
            "timeout": 6,
            "CID": 1,
            "TextbookID": 666,
            "TextbookType": b'1',
            "Page": 1,
            "GraphicNum": 1,
            "Graphic": GraphicModify
            }
        data.update(kwargs)
        result = self.callService(**data)
        return result

    def delete_white_board(self, **kwargs):
        data = {
            "command": commandID.DeleteWhiteBoardData,
            "reqtype": 1,
            "timeout": 6,
            "CID": 1,
            "TextbookID": 666,
            "TextbookType": b'1',
            "Page": 1,
            "GraphicNum": 2,
            "GraphicServerSeq": [0, 1]
            }
        data.update(kwargs)
        result = self.callService(**data)
        return result

    def get_white_board(self, **kwargs):
        data = {
            "command": commandID.GetWhiteBoardData,
            "reqtype": 2,
            "timeout": 6,
            "CID": 1,
            "TextbookID": 666,
            "TextbookType": b'1',
            "Page": 1,
            "BeginSeq": 0
            }
        data.update(kwargs)
        self.callService(**data)

    def clear_white_board(self, **kwargs):
        data = {
            "command": commandID.CleanWhiteBoardData,
            "reqtype": 1,
            "timeout": 6,
            "CID": 1,
            "TextbookID": 666,
            "TextbookType": b'1',
            "Page": 1
            }
        data.update(kwargs)
        result = self.callService(**data)
        return result

    def add_textbook(self, **kwargs):
        data = {
            "command": commandID.AddTextbookData,
            "reqtype": 1,
            "timeout": 6,
            "CID": 1,
            "TextbookID": 666,
            "TextbookType": b'1',
            "Page": 1,
            "OpDataNum": 2,
            "OpDatas": [
                {"ClientSeq": 1, "OpStrData": b"hello", "OpByteDataLen":1, "OpByteData":[b'1']},
                {"ClientSeq": 2, "OpStrData": b"world", "OpByteDataLen":1, "OpByteData":[b'1']}
                ]
            }
        data.update(kwargs)
        result = self.callService(**data)
        return result

    def modify_textbook(self, **kwargs):
        data = {
            "command": commandID.ModifyTextbookData,
            "reqtype": 1,
            "timeout": 6,
            "CID": 1,
            "TextbookID": 666,
            "TextbookType": b'1',
            "Page": 1,
            "OpDataNum": 1,
            "OpDatas": [
                {"ClientSeq": 1, "OpStrData":b"test", "OpByteDataLen":1, "OpByteData":[b'1']}
                ]
            }
        data.update(kwargs)
        result = self.callService(**data)
        return result
    
    def delete_textbook(self, **kwargs):
        data = {
            "command": commandID.DeleteTextbookData,
            "reqtype": 1,
            "timeout": 6,
            "CID": 1,
            "TextbookID": 666,
            "TextbookType": b'1',
            "Page": 1,
            "OpDataNum": 2,
            "OpDataServerSeq": [0,1]    
            }
        data.update(kwargs)
        result = self.callService(**data)
        return result

    def clear_textbook(self, **kwargs):
        data = {
            "command": commandID.ClearTextbookData,
            "reqtype": 1,
            "timeout": 6,
            "CID": 1,
            "TextbookID": 666,
            "TextbookType": b'1',
            "Page": 1
            }
        data.update(kwargs)
        result = self.callService(**data)
        return result

    def push_message(self, **kwargs):
        '''请求发布通用用户push消息给客户端：0x0019004E'''
        data = {
            "command": commandID.PushParticularMsgReq,
            "reqtype": 2,
            "timeout": 10,
            "MsgID": 123,
            "TargetUIDNum": 1,
            "TargetUIDs": [123]
            }
        data.update(kwargs)
        self.callService(**data)
        data_rsp = {
            "command": commandID.PushParticularMsgAck,
            "reqtype": 0,
            "timeout": 30
        }
        data_rsp.update(kwargs)
        result = self.callService(**data_rsp)
        return result

    def receive_pushed_message(self, **kwargs):
        '''下发通用用户push消息：0x00190056'''
        data = {
            "command": commandID.PushMsg,
            "reqtype": 0,
            "timeout": 30
            }
        data.update(kwargs)
        result = self.callService(**data)
        return result
    
    def received_ack(self, **kwargs):
        '''向服务端上报确认已收到的通用用户push消息：0x00190057'''
        data = {
            "command": commandID.PushMsgRsp,
            "reqtype": 2,
            "timeout": 6,
            'MsgNum': 1,
            'MsgSeqList': [123]
            }
        data.update(kwargs)
        self.callService(**data)

    