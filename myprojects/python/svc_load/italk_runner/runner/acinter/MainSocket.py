# coding:utf-8
# from socket import *
from enum import Enum

import gevent
from gevent.pool import Group
from gevent.socket import socket


from acinter.SocPack import SocPack
from acinter.SocPack import commandID
from acinter.Glogger import Glogger
from runner_settings import HB_INTERVAL


class MainSocket:
    '''Socket客户端类

    Attributes：
        greenlet：协程池，用于创建和统一管理协程
        loofpOffset：监听协程接收和解析数据的时间间隔
        call_back_func：回调方法，数据解包后传给该方法处理
        logger：日志处理器
    '''

    socketUserID = 0x00000000000145eb

    def __init__(self, callback_func=None):
        self.greenlet = Group()
        self.__loopOffset = 1 / 100.0   #解析数据的间隔
        self.__callback_func = callback_func
        self.logger = Glogger.getLogger()

    def init(self, host="172.16.16.41", port=6000):
        self.host = host
        self.port = int(port)
        # self.soc = socket(AF_INET, SOCK_STREAM)
        self.soc = socket()
        self.data = b''
        self.tempData = None
        ADDR = (self.host, self.port)
        try:
            self.soc.connect(ADDR)
        except Exception as err:
            raise
        else:
            # self.soc.settimeout(20)
            self.soc.setblocking(0)  # 设置为非阻塞
            self.greenlet.spawn(self.__heart)
            self.greenlet.spawn(self.__loopCheck)

    def sendData(self, data, cmdID, SourceID=0x00000000000145eb, TargetID=0x00):
        bdata = SocPack.topackage(
                data,
                cmdID.value,
                SourceID,
                TargetID
            )
        self.soc.send(bdata)
        self.logger.debug("Send data to {}: {}".format(cmdID, data))
        
    def closeSocket(self):
        try:
            self.soc.close()
        except Exception as e:
            self.logger.error("close socket error:{}".format(e.args))
        finally:
            self.soc = None
            del self.data
            del self.tempData

    # 链接到socket后的长连接心跳
    def __heart(self):
        hb_time = 0
        while self.soc:
            # 当计数器为指定时间(60s)，发送心跳和写日志
            if hb_time == HB_INTERVAL:
                try:
                    self.soc.send(
                        SocPack.topackage(
                            '',
                            commandID.HeartBeat.value,
                            MainSocket.socketUserID
                        )
                    )
                    gevent.sleep(0)
                except Exception as err:
                    raise
                # 发送过消息后，重置计数器
                hb_time = 0
            else:
                # 检查间隔为1s
                hb_time += 1
                gevent.sleep(1)
        else:
            return 0

    # 从socket中读取一段完整的数据
    def __readResponse(self):
        try:
            self.tempData = self.soc.recv(1024)
            if self.tempData:
                self.data += self.tempData
        except EnvironmentError as e:
            pass
        except Exception as e:
            self.logger.error("Read response error:", exc_info=True)

    # 循环读取socket中的数据
    def __loopCheck(self):
        while True:
            if self.soc:
                self.__readResponse()  # 读一次数据
                self.__jiexiData()  # 解析数据包
                gevent.sleep(self.__loopOffset)
            else:
                return 0
    
    def __jiexiData(self):
        size = SocPack.checkPack(self.data)
        if size != 0:
            pack = SocPack.jiemiPack(self.data[0:size], size)
            self.data = self.data[size:]  # 将已读的数据包，从元数据中移除，避免重复读取
            self.__execPack(pack)

    def __execPack(self, packData):
        '''解析包体数据

        解析获取到的包体字节串

        Args：
            packData： 包体字节串
        Returns：
            None
            该函数不反回任何数据，直接将解析后的数据交给回调方法__callback_func处理
        '''
        try:
            #检查返回的commandID是否存在，如果不存在则直接返回，否则继续运行会报错
            cmd_value = int(packData.commandID)
            cmd_enum = commandID(cmd_value)
        except ValueError as err:
            self.logger.warn("Unknow commandID [%s]" % (err,), exc_info=False)
            return

        # 尝试解析函数收包的数据部分。
        try:
            resultData = SocPack.instance().decodePro(
                packData.data, cmd_value
            )
        except Exception as err:
            self.logger.error("falie unpack packet...", exc_info=True)
            return 1

        # 取出数据部分
        resultData = resultData[0]
        
        # 将收取消息的commandID部分的数值转换为commandID枚举类，用于比较
        # packData.commandID = commandID(packData.commandID)
        # self.logger.debug("Receive data from {}: {}".format(cmd_enum, resultData))

        # 将收取到的消息内容回调给逻辑处理部分
        # self.__callback_func(packData.commandID, resultData)
        self.__callback_func(cmd_enum, resultData)

        # 开始处理接受到的数据，进行简单的日志录入
        if cmd_enum == commandID.LoadBalancing:
            # 获得了负载均衡服务返回
            if resultData["RspCode"] == 0:
                # 关闭当前与lbs之间的socket，准备重新连接到acc
                self.soc.close()
                # 从返回结果中提取acc服务器列表
                # serverArr = resultData['Server']
                self.acc_server_list = resultData['Server']

    # 转换字符串IP地址为整数形格式
    def __getIPbyUint32(self, n):
        return '%d.%d.%d.%d' % (n>>24,(n>>16)&0x00ff,(n>>8)&0x0000ff,n&0x000000ff)

    def build_socket_to_acc(self, acc_ip=None, acc_port=None):
        # 如若没有传入的acc地址，直接拾取lbs返回的列表的第一个地址作为连接的地址
        if acc_ip is None and acc_port is None:
            self.host = self.__getIPbyUint32(self.acc_server_list[0]['AccIP'])
            self.port = self.acc_server_list[0]['AccPort'][0]
        else:
            self.host = str(acc_ip)
            self.port = int(acc_port)

        # self.soc = socket(AF_INET, SOCK_STREAM)
        self.soc = socket()
        self.data = b''
        self.tempData = None
        ADDR = (self.host, self.port)
        try:
            self.soc.connect(ADDR)
        except Exception as e:
              raise
        else:
            # self.soc.settimeout(0.1)
            self.soc.setblocking(0)  # 设置为非阻塞
            return True