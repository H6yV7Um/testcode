import unittest
from svccore.DataStruct import DataStruct
from svccore.ProtoBody_pb2 import PbLoadBalancing


class DataStructTest(unittest.TestCase):

    def setUp(self):
        self.cmd = 0x00300010
        self.body = {"cli_type": 16, "app_id":"123"}
        self.ds = DataStruct(self.cmd, self.body, seq=123, target=321)
        self.data = self.ds.build()

    def test_build(self):
        self.assertEqual(len(self.data), self.ds.packet_size)

    def test_parse(self):
        c = DataStruct.parse(self.data)
        self.assertSequenceEqual(
            [self.cmd,self.ds.seq, self.ds.target, self.ds.packet_size],
            [c.CommandID, c.Sequence, c.Target, c.PacketSize]
        )
        self.assertSequenceEqual(
            [self.body['cli_type'], self.body['app_id']],
            [c.Body.cli_type, c.Body.app_id]
        )

if __name__ == '__main__':
    unittest.main()
