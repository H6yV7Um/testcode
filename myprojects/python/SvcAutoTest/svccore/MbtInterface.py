import copy
import json

from .Interface import CommonInterface
from .CmdMapping import CommandMapping
from .SocketClients import MbtClient
from .DataStruct import json_struct
from svcutils.tools import unit32_to_ip, CJsonEncoder, bin_to_b64str


class MbtInterface(CommonInterface):

    def __init__(self):
        super().__init__()
        self.head_dict = {} #自定义的head，方便扩展
        
    def etablish_con(self, ip, port, *, wss=False, acc=False):
        if self.client:
            self.close()
        protocol = 'ws' if not wss else 'wss'
        path = 'web_lbs' if not acc else 'web_acc'
        self.url = "{}://{}:{}/{}".format(protocol, ip, port, path)
        self.client = MbtClient(self.url)
        self.client.connect()
        self.logger.debug("Connect to {}".format(self.url))
    
    def send_data(self, cmd_name, dict_data):
        '''如果body数据为空，则传空字典'''
        data = self._pack_data(cmd_name, dict_data)
        self.client.send(data)
        self.logger.info("Send data to {}: {}".format(cmd_name, data))

    def _pack_data(self, cmd_name, body_dict):
        '''封装json包数据'''
        self.seq += 1
        data = copy.deepcopy(json_struct)
        data['head']['cmd'] = cmd_name.value
        data['head']['seq'] = self.seq
        data['head']['target'] = self.target
        #body必须为字符串
        data['body'] = json.dumps(body_dict, cls=CJsonEncoder)
        return json.dumps(data)

    def get_acc_list(self, **kwargs):
        '''
        向lbs发送请求获取acc地址列表
        @return: {'acc_addrs': [{'ip': 2886733849, 'ports': [4910, 4911]}]}
        '''
        data = {
            "cli_type": 0,
            "device_id": bin_to_b64str(b"123"),
            "app_id": "0"
        }
        self.update_data(data, kwargs)
        self.send_data(CommandMapping.LoadBalancing, data)
        result = self.get_response(CommandMapping.LoadBalancingRsp, timeout=6)
        if "timeout" in result:
            raise KeyError("Get acc list timeout")
        return result['body']
