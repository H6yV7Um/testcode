from .CmdMapping import CommandMapping
from .Interface import CommonInterface
from .SocketClients import PbClient
from .DataStruct import DataStruct
from svcutils.tools import unit32_to_ip


class PbInterface(CommonInterface):

    def etablish_con(self, ip, port, **kwargs):
        if self.client:
            self.close()
        self.client = PbClient(ip, port)
        self.client.connect()
        self.logger.debug("Connect to {}:{}".format(ip, port))

    def send_data(self, cmd_name, dict_data):
        data = self._pack_data(cmd_name, dict_data)
        self.client.send(data)
        self.logger.info("Send data to {}: {}".format(cmd_name, dict_data))
    
    def _pack_data(self, cmd_name, body_dict):
        '''将数据打包为二进制'''
        self.seq += 1
        data = DataStruct(
                cmd_name.value, 
                body_dict,
                self.seq, 
                self.target
            ).build()
        return data

    def get_acc_list(self, **kwargs):
        '''向lbs发送请求获取acc地址列表'''
        data = {
            "cli_type": 16,
            # "device_id": [b"123", b"113"],
            "app_id": "123"
        }
        self.update_data(data, kwargs)
        self.send_data(CommandMapping.PbLoadBalancing, data)
        response = self.get_response(CommandMapping.PbLoadBalancingRsp, timeout=5)
        if "timeout" in response:
            raise KeyError("Get acc list timeout")
        return response.body
