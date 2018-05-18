# coding:utf-8
import struct

import gevent
from gevent.pool import Group
from gevent.socket import *
from gevent.queue import Queue
from tomorrow import threads

from acinter.SocPack import SocPack
from acinter.SocPack import commandID
from acinter.Glogger import Glogger
from runner_settings import HB_INTERVAL


class MainSocket:

    socketUserID = 0x00000000000145eb

    def __init__(self, callback_func=None):
        self.greenlet = Group()
        self.logger = Glogger.getLogger()
        self.data = b''
        self.__callback_func = callback_func
        self.soc = None

    def _connect(self, host, port):
        self.host = host
        self.port = int(port)
        self.soc = socket(AF_INET, SOCK_STREAM)
        ADDR = (self.host, self.port)
        self.soc.connect(ADDR)
        self.greenlet.spawn(self.on_message)
        self.greenlet.spawn(self.send_heartbeat)
 
    def init(self, host="172.16.16.41", port=6000):
        self._connect(host, port)
        self.logger.debug("Connect to {}:{}".format(host, port))
        
    # 向服务器发送协议
    def sendData(self, data, cmdID, SourceID=0x00000000000145eb, TargetID=0x00):
        bdata = SocPack.topackage(
                data,
                cmdID.value,
                SourceID,
                TargetID
            )
        self.soc.send(bdata)
        self.logger.debug("Send data to {}: {}".format(cmdID, data))
        
    # 关闭socket
    def closeSocket(self):
        try:
            self.greenlet.kill()
            self.soc.close()
        except Exception as e:
            self.logger.error("close socket error:{}".format(e.args))
        finally:
            self.soc = None

    def send_heartbeat(self):
        while self.soc:
            try:
                self.soc.send(
                    SocPack.topackage(
                        '',
                        commandID.HeartBeat.value,
                        MainSocket.socketUserID
                    )
                )
                gevent.sleep(HB_INTERVAL)
            except Exception as e:
                self.logger.error("Send HeartBeat Error:", exc_info=True)

    def on_message(self):
        while self.soc:
            self.readResponse()

    def readResponse(self):
        try:
            temp = self.soc.recv(2048)
            if temp:
                self.data += temp
                self.parse_data()
        except Exception as e:
            self.logger.error("read error:{}".format(e))

    def parse_data_old(self, data=None):
        try:  
            size = SocPack.checkPack(self.data)
            if size:
                data = self.data[0:size]
                pack = SocPack.jiemiPack(data, size)
                self.data = self.data[size:]  # 将已读的数据包，从元数据中移除，避免重复读取
                self.run_callback(pack)
                self.parse_data()
        except: 
            self.logger.error("Parse data error:{}".format(data), exc_info=True)
    
    def parse_data(self, data=None):
        '''递归解析存在于协议号配置中的数据包'''
        try:
            size, is_valid = self.check_data()
            if size:
                if is_valid:
                    data = self.data[0:size]
                    pack = SocPack.jiemiPack(data, size)
                    self.run_callback(pack)
                self.data = self.data[size:]
                self.parse_data()
        except:
            self.logger.error("Parse data error:{}".format(data), exc_info=True)
    
    def check_data(self):
        blen = len(self.data)
        # mem = memoryview(self.data)
        is_valid = True
        if blen < 41:
            is_valid = False
            return 0, is_valid
        size = struct.unpack('>I', self.data[2:6])[0]
        if blen < size:
            is_valid = False
            return 0, is_valid
        try:
            #检查协议号是否在协议号映射配置中，不存在则跳过解包
            cmd = struct.unpack('>I', self.data[11:15])
            commandID(cmd[0])
        except ValueError as e:
            is_valid = False
            self.logger.warn("Unknow commandID [%s], unpack and skipped" % e)
            return size, is_valid
        return size, is_valid

    def run_callback(self, packData):
        try:
            #检查返回的commandID是否存在，如果不存在则直接返回，否则继续运行会报错
            cmd_name = commandID(packData.commandID)
            resultData = SocPack.instance().decodePro(
                packData.data, packData.commandID
            )
            # 取出数据部分
            resultData = resultData[0]
        except ValueError as err:
            self.logger.warn("Unknow commandID [%s]" % (err,))
            return
        except Exception as err:
            self.logger.error("falie unpack packet...", exc_info=True)
            return 1

        # 将收取到的消息内容回调给逻辑处理部分
        self.__callback_func(cmd_name, resultData)
        self.logger.debug("Receive data from {}: {}".format(cmd_name,resultData))
                
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
        self.init(self.host, self.port)
        return True