# coding:utf-8

from vncdotool import api


client = api.connect('192.168.0.124')
client.keyPress("super-d")
api.shutdown()
