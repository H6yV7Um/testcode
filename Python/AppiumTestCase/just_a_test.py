#coding: utf-8
import unittest

class Hello(unittest.TestCase):
    """docstring for Hello"""
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_hello(self):
        self.assertEqual(10,11)

if  __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Hello)
    unittest.TextTestRunner(verbosity=2).run(suite)