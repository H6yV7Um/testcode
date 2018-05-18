from acinter import interface
import gevent
from gevent.pool import Group
from gevent.socket import socket
from random import randint
from acinter.SocPack import commandID

g = Group()

def run():
    user = interface.acsim()
    user.connect_italk('172.16.16.41', 6000)
    user.login(Account=str(randint(1,999)))
    user.login_complete()
    user.enter_classroom(CID=666)
    user.enter_class_complete(CID=666)
    user.change_textbook_page(CID=666)
    user.chat_in_classroom(CID=666)
    user.hand_up(CID=666)
    user.hand_down(CID=666)
    user.get_pen_color(CID=666)
    user.change_textbook_page(CID=666)
    user.add_textbook(CID=666)
    user.modify_textbook(CID=666)
    user.delete_textbook(CID=666)
    user.clear_textbook(CID=666)
    user.add_white_board(CID=666)
    user.modify_white_board(CID=666)
    user.delete_white_board(CID=666)
    user.clear_white_board(CID=666)
    user.disconnect_italk()
    
# for i in range(30):
#     g.spawn(run)
# g.join()

run()
