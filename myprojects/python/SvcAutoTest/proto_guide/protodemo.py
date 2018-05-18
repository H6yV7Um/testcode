import time
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from google.protobuf.json_format import MessageToDict, ParseDict
from protobuf_demo_pb2 import OnlineUser


class Client:
    def __init__(self, ip, port):
        self.soc = socket(AF_INET, SOCK_STREAM)
        self.soc.connect((ip, port))
        self.listener = Thread(target=self.on_message)
        self.listener.setDaemon(True)
        self.listener.start()

    def on_message(self):
        while self.soc:
            data = self.soc.recv(4096)
            if data:
                print("Received pb data:", data)
                #实际应用时，这里应该先解析到单个数据包的大小，再截取对应长度的数据做解析
                user.ParseFromString(data)
                #将反序列化后的user转换为字典对象，protobuf还提供了MessageToJson用来转换为json对象
                user_dict = MessageToDict(user, 
                                    including_default_value_fields=True, 
                                    preserving_proto_field_name=True)
                print("Parse pb to dict:", user_dict)

    def send_data(self, data):
        self.soc.send(data)
        print("Send pb data:", data)
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.soc.close()

user1 = {
    "uid": 123456,
    "usre_name": 'tester',
    "type": 2,
    "phone_num": "119",
    "cli_type": 5
}
demo_struct = {
    "rsp_code": 0,
    "product": None,
    "query_time": int(time.time()),
    # "random": [888， 999],
    "user_list": [user1]
}

#实例化一个protobuf message对象
user = OnlineUser()
#将字典对象的数据赋值给message对象
ParseDict(demo_struct, user)
#message对象可以直接通过属性访问
print("User list:", user.user_list)
#序列化为pb二进制数据用于IO操作
ser_user = user.SerializeToString()
print("Serialized user:", ser_user)

with Client('127.0.0.1', 6000) as client:
    client.send_data(ser_user)
    time.sleep(1)
