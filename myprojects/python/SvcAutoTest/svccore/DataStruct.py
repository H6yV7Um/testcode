import json
import base64
import logging

import construct
from construct import *
from google.protobuf.json_format import MessageToDict, ParseDict

from .CmdMapping import CommandMapping
from svcutils.tools import DotDict
from .ProtoBody_pb2 import *

logger = logging.getLogger(__name__)

#websocket所用的json格式的数据包结构，其中body的value必须为字符串
json_struct = {
    "head": {
        "flag": 104,
        "type": 0,
        "off_act": 0,
        "com_type": 0,
        "cmd": 0,
        "seq": 0,
        "target": 0
    },
    "exthead": {},
    "body": ""  
}

#二进制流的包头数据格式
HEAD_SIZE = 28
head_struct = Struct(
    HeadFlag=Const(Int8ub, 0X68),
    PacketSize=BytesInteger(3),
    PacketType=Const(Int8ub, 0),
    ExtheadSize=BytesInteger(3),
    BitFields01=EmbeddedBitStruct(
        "OfflineAct"/Const(Nibble, 0),  #Nibble <=> BitsInteger(4)
        "EncryptType"/Const(Nibble, 0)
    ),
    PubKeyIndex=Const(Int16ub, 0),
    BitFields02=EmbeddedBitStruct(
        "CompressType"/Const(Nibble, 0),
        "DataType"/Const(Nibble, 0)
    ),
    CommandID=Int32ub,
    Sequence=Int32ub,
    Target=Int64ub
    # Exthead=Const(Int32ub, 0),
)
#用于单独解析包长度是s[1:4]
pack_size_struct = BytesInteger(3)


class DataStruct:
    head_size = HEAD_SIZE
    def __init__(self, commandID, body_dict, seq=0, target=0):
        self.packet_size = 0    
        self.exthead_size = 0
        self.seq = seq
        self.target = target
        self.cmd = commandID
        self.body = body_dict

    def _build_head(self):
        return head_struct.build(dict(
            CommandID=self.cmd,
            PacketSize=self.packet_size,
            ExtheadSize=self.exthead_size,
            Sequence=self.seq,
            Target=self.target
            )
        )
    
    def build_body(self):
        '''将body序列化为PB二进制串'''
        if not self.body:
            return b""
        proto_ins = self.convert_to_proto(self.cmd)
        ParseDict(self.body, proto_ins)
        return proto_ins.SerializeToString()
        
    def build(self):
        body = self.build_body()
        self.packet_size = self.head_size + len(body)
        head = self._build_head()
        return head + body
    
    @classmethod
    def convert_to_proto(cls, cmd):
        '''将协议号对应的名称转化为相应的proto message实例'''
        return eval(CommandMapping(cmd).name)()

    @classmethod
    def parse_body(cls, cmd, cbody):
        '''将body解析为字典对象'''
        proto_ins = cls.convert_to_proto(cmd)
        proto_ins.ParseFromString(cbody)
        return MessageToDict(proto_ins, 
                            including_default_value_fields=True, 
                            preserving_proto_field_name=True)

    @classmethod
    def parse(cls, data):
        '''解析整个数据包，返回一个字典'''
        try:
            bhead = data[:cls.head_size]
            bbody = data[cls.head_size:]
            data_dict = head_struct.parse(bhead)
            cmd = data_dict['CommandID']
            body_dict = cls.parse_body(cmd, bbody)
            data_dict['body'] = body_dict
            return data_dict
        except TypeError as e:
            logger.error("Received invalid data:{}".format(e.args)) 
        

