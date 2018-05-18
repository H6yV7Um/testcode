import unittest

from svccore.PbInterface import PbInterface
from svccore.MbtInterface import MbtInterface
from GlobalSettings import LBS_IP, MBT_PORT, PB_PORT


class InterfaceTest(unittest.TestCase):

    def tes_pbinterface(self):
        pb = PbInterface()
        pb.connect_to_svc(LBS_IP, PB_PORT)
        pb.login()
        pb.login_complete()
        pb.anonymous_login()
        pb.close()

    def test_mbtinterface(self):
        mbt = MbtInterface()
        mbt.connect_to_svc(LBS_IP, MBT_PORT)
        mbt.http_login()
        mbt.token_login()
        mbt.http_regist()
        mbt.http_anonymous_login()
        mbt.token_login()
        mbt.http_get_state()
        # mbt.anonymous_login()
        mbt.enter_class(cid=123)
        # mbt.hand_up()
        mbt.close()


if __name__ == '__main__':
    unittest.main()

