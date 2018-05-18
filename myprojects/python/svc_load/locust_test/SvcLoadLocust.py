#coding:utf-8

import time
import random
from functools import wraps
from traceback import format_exc

import gevent
from locust import events
from locust.core import Locust

from acinter import interface
from myexceptions import *
from config import *


class SvcLocust(Locust):
    """class doc"""
    def __init__(self):
        super(SvcLocust, self).__init__()
        self.client = LoadTestCase()


class LbsLocust(Locust):
    '''class doc'''
    def __init__(self):
        super(LbsLocust, self).__init__()
        self.client = LoadTestLbs()


def stat_user_operation(class_name, role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                start_time = time.time()
                result = func(*args, **kwargs)
                rsp_time = int((time.time()-start_time)*1000)
                rsp_code = result.get('RspCode', None)
                push_msgid_str = result.get('MsgStr', None)
                roles = role if not push_msgid_str else push_msgid_str
                if rsp_code == 0:
                    events.request_success.fire(
                        request_type="%s-%s" % (class_name, roles),
                        name=func.__name__,
                        response_time=rsp_time,
                        response_length=len(result)
                    )
                    return True
                elif rsp_code is None:
                    raise OperateTimeout('%s' % result)
                else:
                    error_msg = 'Response Code: %s' % rsp_code
                    raise ResponseError(error_msg)
            except Exception as e:
                events.request_failure.fire(
                    request_type = "%s-%s" % (class_name, role),
                    name = func.__name__,
                    response_time = time.time(),
                    exception = e
                )
        return wrapper
    return decorator

class LoadTestCase(object):
    """class doc"""
    def __init__(self):
        super(LoadTestCase, self).__init__()
    
    def normal_class_scene(self, data_tup):
        """正常教室内的业务场景"""
        uid, cid, user_flag, class_type = data_tup[1]
        #user_flag: 0-学生, 1-老师, 2-无任何操作的学生
        class_name = CLASS_MAPPING.get(class_type, 'test')
        user, role, test_scene_set = self.check_role(user_flag, data_tup[2])
        login_status = False
        try:
            #用户初始化，连接acc
            user.init(data_tup[0], data_tup[1])
            #stat part
            if LOGIN_OP_CODE in test_scene_set:
                test_scene_set.discard(LOGIN_OP_CODE)
                login_status = stat_user_operation(class_name, role)(user.login)() 
            if login_status:
                user.is_login = True
                user.do_enter = ENTER_OP_CODE in test_scene_set
                if PUSH_OP_CODE in test_scene_set:
                    test_scene_set.discard(PUSH_OP_CODE)
                    user.push_greenlet = gevent.spawn(user.do_receive_pushed_message)
                    if not user.do_enter:
                        gevent.sleep(user.class_time)
                if user.do_enter:
                    test_scene_set.discard(ENTER_OP_CODE)
                    enter_status = stat_user_operation(class_name, role)(user.enter_class)()
                    if enter_status:
                        user.call_custom_operation(class_name, role, test_scene_set)
                        # user.leave_class()
                    # user.logout()
        except Exception as e:
            if isinstance(e, EnvironmentError):
                msg = "args:{0}".format(e.args)
                error = ConnectionError(msg)
            else:
                msg = format_exc()
                error = UnexpectError(msg)
            events.request_failure.fire(
                request_type = "%s-%s" % (class_name, role),
                name = "{}, user will retry!".format(type(error).__name__),
                response_time = time.time(),
                exception = error
                )
            
        finally:
            #断开连接,保证finally是exception safe的，否则会有不可控错误，导致greenlet kill不掉
            try:
                if user.push_greenlet:
                    user.push_greenlet.kill()
                user.is_login = False
                #user.leave_class()    
                #user.logout()
                user.ac.disconnect_italk()
            except:
                pass

    def check_role(self, user_flag, test_scene_dict):
        if user_flag == STUDENT_FLAG:
            user = Student()
            test_scene_list = test_scene_dict['student_scene']
        elif user_flag == STATIC_STUDENT_FLAG:
            user = StaticStudent()
            test_scene_list = [LOGIN_OP_CODE, ENTER_OP_CODE]
        elif user_flag == TEACHER_FLAG:
            user = Teacher()
            test_scene_list = test_scene_dict['teacher_scene']
        else:
            user = User()
            test_scene_list = []
        role = type(user).__name__
        return user, role, set(test_scene_list)

class User(object):
    """common user"""
    def __init__(self):
        """func doc"""
        self.ac = interface.acsim()
        self.is_login = False
        self.do_enter = False
        self.push_greenlet = None
        
    def init(self, config_data, user_data):
        uid, cid, _, _ = user_data
        lbs_ip_str, lbs_port, class_duration, op_interval = config_data
        self.cid = cid
        self.uid = uid
        self.lbs_ip = self.random_lbs_ip(lbs_ip_str)
        self.lbs_port = lbs_port
        self.op_interval = op_interval    #操作间隔时间
        self.class_time = class_duration  #课时长度 单位s
        self.op_num = int(self.class_time/self.op_interval) or 1  #操作次数
        self.ac.connect_italk(lbs_ip=self.lbs_ip, lbs_port=self.lbs_port)
    
    def random_lbs_ip(self, hoststr):
        host_list = hoststr.split(',')
        return random.choice(host_list)
    
    def login(self):
        """func doc"""
        response = self.ac.login(Account=self.uid, timeout=6)
        self.ac.login_complete()
        return response
    
    def enter_class(self):
        """func doc"""
        response = self.ac.enter_classroom(CID=self.cid)
        self.ac.enter_class_complete(CID=self.cid)
        return response
    
    def leave_class(self):
        """func doc"""
        response = self.ac.leave_classroom(SID=self.uid, CID=self.cid)
        return response

    def logout(self):
        """func doc"""
        self.ac.logout(1)
        self.is_login = False
    
    def do_receive_pushed_message(self):
        '''监听push消息'''
        while self.is_login:
            recv_message = self.ac.receive_pushed_message(timeout=self.class_time)
            if self.is_login:
                self.handle_push_message(recv_message)

    @stat_user_operation('Push Test', 'User')
    def handle_push_message(self, push_message):
        '''push消息回调'''
        msg_list = push_message.get('MsgList', None)
        seq_key = 'MsgSeq'
        msgid_key = 'MsgID'
        if msg_list:
            msg_seq = [msg[seq_key] for msg in msg_list if seq_key in msg]
            msg_ids = [str(msg[msgid_key]) for msg in msg_list if msgid_key in msg]
            msg_id_str = '|'.join(msg_ids)
            msg_num = len(msg_seq)
            self.ac.received_ack(MsgNum=msg_num, MsgSeqList=msg_seq)
            return {'RspCode': 0, 'MsgStr': msg_id_str}
        return push_message

    def think_time(self, interval=None):
        '''用户思考时间，即操作间隔时间s'''
        if interval:
            gevent.sleep(interval)
        else:
            gevent.sleep(random.randint(1, 10))

    def _call_all(self, class_name, role):
        class_dict = type(self).__dict__
        for name, function in class_dict.items():
            if name.startswith('do'):
                if name not in ('do_chat_in_classroom', 'do_get_white_board'):
                    stat_user_operation(class_name,role)(getattr(self, name))
                else:
                    function(self)

    def call_all_operation(self, class_name, role):
        for _ in xrange(self.op_num):
            self._call_all(class_name, role)
            self.think_time(self.op_interval)

    def _call_custom_operation(self, class_name, role, test_scene):
        for op_code in test_scene:
            op_name = OPERATION_MAPPING[op_code]
            func = type(self).__dict__[op_name]
            if op_name not in ('do_chat_in_classroom', 'do_get_white_board'):
                stat_user_operation(class_name,role)(getattr(self, op_name))()
            else:
                func(self)

    def call_custom_operation(self, class_name, role, test_scene):
        '''
        静态学生的test_scene为空，不会在教室内操作，只会等待
        '''
        if test_scene or role == 'StaticStudent':
            for _ in range(self.op_num):
                self._call_custom_operation(class_name, role, test_scene)
                self.think_time(self.op_interval)


class Teacher(User):
    '''Teacher'''
    def __init__(self):
        super(Teacher, self).__init__()

    def do_chat_in_classroom(self):
        '''chat has no rspcode'''
        self.ac.chat_in_classroom(CID=self.cid, Text="hi, I'm teacher")
    
    def do_change_textbook_page(self):
        return self.ac.change_textbook_page(CID=self.cid)
    
    def do_add_textbook(self):
        return self.ac.add_textbook(CID=self.cid)
    
    def do_modify_textbook(self):
        return self.ac.modify_textbook(CID=self.cid)
    
    def do_delete_textbook(self):
        return self.ac.delete_textbook(CID=self.cid) 
    
    def do_clear_textbook(self):
        return self.ac.clear_textbook(CID=self.cid)
    
    def do_add_white_board(self):
        return self.ac.add_white_board(CID=self.cid, TextbookID=666)
    
    def do_get_white_board(self):
        '''has no rspcode'''
        self.ac.get_white_board(CID=self.cid, TextbookID=666)

    def do_modify_white_board(self):
        return self.ac.modify_white_board(CID=self.cid, TextbookID=666)
    
    def do_delete_white_board(self):
        return self.ac.delete_white_board(CID=self.cid, TextbookID=666)
    
    def do_clear_white_board(self):
        return self.ac.clear_white_board(CID=self.cid, TextbookID=666)
    
    
class Student(User):
    '''Student'''
    def __init__(self):
        super(Student, self).__init__()
    
    def do_get_pen_color(self):
        return self.ac.get_pen_color(CID=self.cid)
    
    def do_hand_up(self):
        return self.ac.hand_up(CID=self.cid)
    
    def do_hand_down(self):
        return self.ac.hand_down(CID=self.cid)

    def do_chat_in_classroom(self):
        '''无响应码，会调用，但暂时不纳入通过率统计'''
        self.ac.chat_in_classroom(CID=self.cid, Text="hi, I'm student")


class StaticStudent(User):
    '''StaticStudent'''
    def __init__(self):
        super(StaticStudent, self).__init__()
    

if __name__ == '__main__':
    pass
