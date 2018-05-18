from gevent import monkey
monkey.patch_all(thread=False)
import json

from ws4py.client.threadedclient import WebSocketClient
from ws4py.client.geventclient import WebSocketClient as aWebSocketClient
import gevent
from gevent.socket import socket
from gevent.pool import Group

from .CmdMapping import CommandMapping
from .DataStruct import DataStruct, pack_size_struct, HEAD_SIZE
from svcutils.Glogger import Glogger
from svcutils.tools import DotDict


logger = Glogger.getLogger()

class MbtClient(aWebSocketClient):
    def __init__(self, *args):
        super().__init__(*args)
        self.callback_dict = {}
        self.greenlets = Group()
        self.greenlets.spawn(self.onMessage)
    
    def onMessage(self):
        while True:
            try:
                #收到的data类型为ws4py.messaging.TextMessage
                data = self.receive()
                #data.data是bytes类型，先转化为str
                parsed_data = json.loads(data.data.decode())
                cmd = parsed_data["head"]["cmd"]
                cmd_name = CommandMapping(cmd)
                body_dict = json.loads(parsed_data["body"])
                parsed_data["body"] = body_dict
                self.callback_dict[cmd_name] = DotDict(parsed_data)
                logger.info("Receive data from {}:{}".format(cmd_name, parsed_data))
            except ValueError:
                logger.warn("Receive unknown commandID: {}".format(cmd))
            except TypeError:
                logger.error("Receive invalid data that is not JSON serializable:{}".format(data.data))
    
    def closed(self, code, reason):
        self.greenlets.kill()
        logger.debug("Socket was closed:code-{};reason-{}".format(code, reason))


class PbClient:
    def __init__(self, ip, port):
        self.addr = (ip, int(port)) 
        self.callback_dict = {}
        self.greenlets = Group()
        self.soc = socket()
        self.interval = 1/200
        self.received_data = b''

    def connect(self):
        self.soc.connect(self.addr)
        self.greenlets.spawn(self.on_message)
    
    def send(self, data):
        self.soc.send(data)

    def close(self):
        try:
            self.greenlets.kill()
            self.soc.close()
        except:
            pass
        finally:
            self.soc = None

    def on_message(self):
        try:
            while self.soc:
                temp = self.soc.recv(2048)
                # gevent.sleep(self.interval)
                if temp:
                    self.received_data += temp
                    self.handle_message()
        except EnvironmentError:
            pass
        except:
            raise

    def handle_message(self):
        try:
            if len(self.received_data) < HEAD_SIZE:
                return
            data = self.get_pack_stream()
            data_dict = DotDict(DataStruct.parse(data))
            cmd_name = CommandMapping(data_dict['CommandID'])
            self.callback_dict[cmd_name] = data_dict
            logger.info("Receive data from {}:{}".format(cmd_name, data_dict))
            self.handle_message()
        except ValueError:
            logger.warn("Receive unknown commandID: {}".format(cmd_name))
        except TypeError as e:
            logger.error("Receive invalid data:", exc_info=True)

    def get_pack_stream(self):
        '''获取单个完整包的数据流'''
        size_stream = self.received_data[1:4]
        pack_size = pack_size_struct.parse(size_stream)
        pack_stream = self.received_data[:pack_size]
        self.received_data = self.received_data[pack_size:]
        return pack_stream


class WebClient(WebSocketClient):
    '''线程版mbt客户端'''
    def opened(self):
        logger.debug("Connect to server success!")
        self.callback_dict = {}
        
    def closed(self, code, reason):
        logger.debug("Socket was closed:code-{};reason-{}".format(code, reason))
    
    def received_message(self, data):
        try:
            parsed_data = json.loads(data.data.decode('utf8'))
            cmd = parsed_data["head"]["cmd"]
            cmd_name = CommandMapping(cmd)
            rsp_body = json.loads(parsed_data["body"])
            self.callback_dict[cmd_name] = rsp_body
            logger.info("Receive data from {}:{}".format(cmd_name, data))
        except ValueError:
            logger.warn("Receive unknown commandID: {}".format(cmd))
        except TypeError:
                logger.error("Receive invalid data that is not JSON serializable:{}".format(data.data))

