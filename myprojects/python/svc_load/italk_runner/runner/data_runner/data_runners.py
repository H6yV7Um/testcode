#coding: utf-8

import socket
import random
import time
import json
import logging
from hashlib import md5
from subprocess import PIPE

import gevent
from gevent.pool import Group
from gevent.queue import Queue, Empty, Full
import six
from six.moves import xrange
import psutil

from data_runner import events
from data_runner import rpc, Message
from utils import DictObj
from runner_settings import LBS_IP_STR, LBS_PORT, OP_INTERVAL, CLASS_DURATION, DATA_RUNNER_MASTER
from runner_settings import get_logger


# 全局runner
global_runner = None

#用于汇总数据的全局变量
global_stats = DictObj()
push_uid_list = None

#current process
cur_process = psutil.Process()

STATE_INIT, STATE_READY, STATE_RUNNING, STATE_DONE, STATE_STOPPED = ["connected", "ready", "running", "done", "stopped"]
SLAVE_REPORT_INTERVAL = 2.0
QUEUE_MONITOR_INTERVAL = 2.0

#master数据节点的ip与port
MASTER_HOST = DATA_RUNNER_MASTER()
MASTER_BIND_PORT = 6666


class BaseRunner(object):
    '''class doc'''
    def __init__(self):
        '''func doc'''
        self.master_bind_host = '*'
        self.master_bind_port = MASTER_BIND_PORT
        self.master_host = MASTER_HOST
        self.stats = global_stats
        self.queue = None
        self.queue_size = 0
        self.state = STATE_INIT
        self.greenlet = Group()
        self.logger = logging.getLogger('console')

        def on_runner_data_refresh(runner_data, is_delete=False):
            '''刷新global_stats中各节点的数据'''
            key = hash(runner_data.id)
            if is_delete:
                self.stats.pop(key)
            else:
                row = self.stats.setdefault(key, runner_data)
                row.update(runner_data)
        events.runner_data_refresh += on_runner_data_refresh

        def on_make_data_done():
            '''主节点生产数据完毕时触发该事件'''
            self.state = STATE_READY
            if self.init_info.role == 'Master':
                self.logger.info("master send prepare to slave")
                self.prepare_distribute()
        events.make_data_done += on_make_data_done

    @property
    def current_queue_size(self):
        if self.queue:
            return self.queue.qsize()
        else:
            return 0

    @property
    def cpu_info(self):
        cpu_percent = "{:.1f}".format(cur_process.cpu_percent(interval=1.0))
        return cpu_percent
    
    @property
    def mem_info(self):
        mem_percent = "{:.1f}".format(cur_process.memory_percent())
        return mem_percent
    
    @property
    def cur_proc_status(self):
        return cur_process.status()
    
    @property
    def sys_loadavg(self):
        '''system load average in 1 min'''
        try:
            r = psutil.Popen(['cat', '/proc/loadavg'], stdout=PIPE)
            loadavg = r.communicate()[0].split()[0]
        except WindowsError:
            loadavg = None
        return loadavg

    def _make_uid(self, mark=0):
        '''根据mark值生成用户id，0：学生，1：教师'''
        return random.randint(1, 0xffffffffffffff) + (mark << 56)
    
    def _make_random_uid(self, num, iss):
        '''func doc'''
        for i in xrange(num):
            if i == 0:
                uid = self._make_uid(1)
                op_code = 1
            else:
                uid = self._make_uid()
                if not iss or i%2 != 0:
                    op_code = 0
                else:
                    op_code = 2
            yield uid, op_code

    def _make_random_cid(self, class_type, num):
        '''根据class_type生产对应的cid'''
        for _ in xrange(num):
            cid = random.randint(1, 0xffffffffffffff) + (class_type << 56)
            yield cid

    def _make_random_data(self, config_data, test_scene, class_struct, iss):
        '''func doc'''
        for class_type, count in six.iteritems(class_struct):
            class_count, user_count = count
            for cid in self._make_random_cid(class_type, class_count):
                for uid, op_code in self._make_random_uid(user_count, iss):
                    push_uid_list.append(uid)
                    user_data = (uid, cid, op_code, class_type)
                    self.queue.put_nowait((config_data, user_data, test_scene))

    def _make_seq_cid(self, class_type, start, end):
        '''func doc'''
        base_cid = 2 << 56
        for i in xrange(start, end):
            cid = base_cid + i + (class_type << 56)
            yield cid
    
    def _make_seq_uid(self, iss, start, end):
        '''func doc'''
        base_uid = 1<<56
        for i in xrange(start, end):
            if i == start:
                uid = base_uid + i + (1 << 56)
                op_code = 1
            else:
                uid = base_uid + i + (0 << 56)
                if not iss or i%2 != 0:
                    op_code = 0
                else:
                    op_code = 2
            yield uid, op_code

    def _make_seq_data(self, config_data, test_scene, class_struct, iss):
        '''func doc'''
        c_start, c_end = 0, 0
        u_start, u_end = 0, 0
        for class_type, count in six.iteritems(class_struct):
            class_count, user_count = count
            c_end += class_count
            for cid in self._make_seq_cid(class_type, c_start, c_end):
                u_end += user_count
                for uid, op_code in self._make_seq_uid(iss, u_start, u_end):
                    push_uid_list.append(uid)
                    user_data = (uid, cid, op_code, class_type)
                    self.queue.put_nowait((config_data, user_data, test_scene))
                u_start += user_count
            c_start += class_count
            
    def make_data(self, struct):
        '''func doc'''
        global push_uid_list
        push_uid_list = []
        if not struct:
            struct = {"include_static_stu": False, "test_scene": {"student": [1,2]}, "data_struct": {"total":100000, "detail":{0: (50000, 2)}}}
        config_data = (LBS_IP_STR(), LBS_PORT(), CLASS_DURATION(), OP_INTERVAL())
        data_detail = struct["data_struct"]['detail']
        test_scene = struct["test_scene"]
        # insert_data = {"data_struct": json.dumps(data_detail), "scene_struct": json.dumps(test_scene)}
        # insert_test_record(insert_data)
        include_static_student = struct["include_static_stu"]
        is_random = struct["is_random"]
        self.queue_size = struct["data_struct"]['total']
        self.queue = Queue(self.queue_size)
        try:
            if not is_random:
                self._make_seq_data(config_data, test_scene, data_detail, include_static_student)
            else:
                self._make_random_data(config_data, test_scene, data_detail, include_static_student)
        except:
            self.logger.error("Make data failed", exc_info=True)
            return False
        else:
            events.make_data_done.fire()
            self.logger.info("Master make data done! count:%s" % self.current_queue_size)
            return True

    def get_data(self):
        '''对外提供数据接口'''
        try:
            data = self.queue.get_nowait()
        except:
            data = None
            self.logger.error("Get data error:", exc_info=True)
        return data

    def queue_monitor(self):
        '''主节点队列监听线程'''
        while self.state != STATE_STOPPED:
            self.init_info.qsize = self.queue_size
            self.init_info.state = self.state
            self.init_info.data_count = self.current_queue_size
            self.init_info.cpu_percent = self.cpu_info
            self.init_info.mem_percent = self.mem_info
            self.init_info.loadavg = self.sys_loadavg
            events.runner_data_refresh.fire(self.init_info)
            gevent.sleep(QUEUE_MONITOR_INTERVAL)
        else:
            self.logger.info("stop queue_monitor")

    def start_hatch(self, struct):
        '''启动造数据，供web接口调用'''
        self.logger.info("Master start hatching data!")
        self.state = STATE_RUNNING
        if not self.make_data(struct):
            return False
        self.start_distribute()
        return True

    def stop(self):
        '''更改runner状态，间接kill掉所有异步线程'''
        self.state = STATE_STOPPED

    def reset(self):
        '''重置各节点状态'''
        self.state = STATE_INIT
        self.queue = None
        self.queue_size = 0
        if hasattr(self, "clients"):
            self.init_info = MainNode(self.master_host)
            events.runner_data_refresh.fire(self.init_info)
            for client in six.itervalues(self.clients):
                client.qsize = 0
                self.server.send(Message('reset', None, None))
        elif hasattr(self, "client_id"):
            pass
        else:
            self.init_info = MainNode(id=self.id, role="local")
        events.runner_data_refresh.fire(self.init_info)


class LocalRunner(BaseRunner):
    '''class doc'''
    def __init__(self):
        '''func doc'''
        self.id = "Local"
        super(LocalRunner, self).__init__()
        self.init_info = MainNode(id=self.id, role="local")
        events.runner_data_refresh.fire(self.init_info)

class MainNode(DictObj):
    '''class doc'''
    def __init__(self, id, role="Master", state=STATE_INIT):
        '''func doc'''
        self.id = id
        self.role = role
        self.state = state
        self.qsize = 0
        self.data_count = 0
        self.cpu_percent = 0
        self.mem_percent = 0
        self.loadavg = 0

class SlaveNode(DictObj):
    '''class doc'''
    def __init__(self, client_id, state=STATE_INIT):
        '''func doc'''
        self.id = client_id
        self.role = "Slave"
        self.state = state
        self.qsize = 0
        self.data_count = 0
        self.cpu_percent = 0
        self.mem_percent = 0
        self.loadavg = 0


class SlaveNodesDict(dict):
    '''class doc'''
    def get_by_state(self, state):
        '''func doc'''
        return [c for c in six.itervalues(self) if c.state == state]

    @property
    def connected(self):
        '''func doc'''
        return self.get_by_state(STATE_INIT)

    @property
    def ready(self):
        '''func doc'''
        return self.get_by_state(STATE_READY)

    @property
    def running(self):
        '''func doc'''
        return self.get_by_state(STATE_RUNNING)

    @property
    def done(self):
        '''func doc'''
        return self.get_by_state(STATE_DONE)

    @property
    def stopped(self):
        '''func doc'''
        return self.get_by_state(STATE_STOPPED)


class MasterRunner(BaseRunner):
    '''class doc'''
    def __init__(self):
        '''func doc'''
        super(MasterRunner, self).__init__()
        self.logger = logging.getLogger('data_runner.master')
        self.clients = SlaveNodesDict()
        self.server = rpc.Server(self.master_bind_host, self.master_bind_port)
        self.greenlet.spawn(self.client_listenner)
        self.slave_queue_size = 0
        self.init_info = MainNode(self.master_host)
        self.greenlet.spawn(self.queue_monitor)

        def on_slave_be_ready(client_id, qsize):
            '''slave节点创建队列成功后触发该事件'''
            self.clients[client_id].state = STATE_READY
            self.clients[client_id].qsize = qsize
            events.runner_data_refresh.fire(self.clients[client_id])
        events.slave_be_ready += on_slave_be_ready

        def on_slave_report(client_id, data):
            '''接收slave上报的数据'''
            if client_id not in self.clients:
                self.clients[client_id] = SlaveNode(client_id)
                self.logger.info("Receive report from unrecognized slave %s", client_id)
                # return

            self.clients[client_id].data_count = data["data_count"]
            self.clients[client_id].state = data["state"]
            self.clients[client_id].qsize = data["queue_size"]
            self.clients[client_id].cpu_percent = data["cpu_percent"]
            self.clients[client_id].mem_percent = data["mem_percent"]
            self.clients[client_id].loadavg = data["loadavg"]
            events.runner_data_refresh.fire(self.clients[client_id])
        events.slave_report += on_slave_report

    def is_valid_slave(self, client_id):
        '''func doc'''
        if client_id in self.clients:
            return True
        else:
            self.logger.info("Discarded report from unrecognized slave %s", client_id)

    def client_listenner(self):
        '''func doc'''
        while self.state != STATE_STOPPED:
            try:
                msg = self.server.recv()
                client_id = msg.client_id
                if msg.type == 'connected':
                    self.logger.info("The client %s connected" % client_id)
                    self.clients[client_id] = SlaveNode(client_id)
                    events.runner_data_refresh.fire(self.clients[client_id])
                elif msg.type == 'ready':
                    events.slave_be_ready.fire(client_id, msg.data)
                elif msg.type == 'client_start':
                    # self.logger.info("The client %s start consuming data!" % client_id)
                    self.clients[client_id].state = STATE_RUNNING
                elif msg.type == 'done':
                    # self.logger.info("Client %s consuming data done!" % client_id)
                    self.clients[client_id].state = STATE_DONE
                    if msg.data:
                        self.logger.info("return %d remained data by client %s" % (len(msg.data), client_id))
                        self.handle_remain_data(msg.data)
                        self.state = STATE_RUNNING
                elif msg.type == 'stopped':
                    if client_id in self.clients:
                        events.runner_data_refresh.fire(self.clients[client_id], is_delete=True)
                        del self.clients[client_id]
                        self.logger.info("The client %s is stopped" % client_id)
                elif msg.type == 'stats':
                    events.slave_report.fire(client_id, msg.data)
                elif msg.type == 'client_reset':
                    self.clients[client_id].state = STATE_INIT
                    self.logger.info("Client-%s has been reset" % client_id)
            except Exception as e:
                self.logger.error("Client listener Error,ignore and continue!", exc_info=True)
        else:
            self.logger.info("Client listener is stopped!")

    def prepare_distribute(self):
        '''通知slave创建对应长度的数据队列，为接收数据做准备'''
        if self.state != STATE_READY:
            self.logger.warn("Master data is not ready!wait 2 second then continue")
            gevent.sleep(2)
            self.prepare_distribute()

        num_slaves = len(self.clients.connected)
        if not num_slaves:
            self.logger.warn("no slave servers connected!")
            return
        slave_queue_size = self.queue_size // num_slaves or 1
        remaining = self.queue_size % num_slaves
        for client in six.itervalues(self.clients):
            data = {
                "queue_size": slave_queue_size,
                "stop_timeout": None
            }
            if remaining > 0:
                data['queue_size'] += 1
                remaining -=1
            client.qsize = data['queue_size']
            self.logger.info("%s queue size: %s" % (client.id, client.qsize))
            self.server.send(Message("prepare", data, None))

    def distributer(self):
        '''按照各client的qsize分发数据'''
        try:
            for client in six.itervalues(self.clients):
                temp_data = []
                for _ in xrange(client.qsize):
                    data = self.queue.get(timeout=2)
                    temp_data.append(data)
                self.server.send(Message('data', temp_data, None))
                self.logger.info("send data to slaves:{0}".format(temp_data[0]))
        except Empty:
            raise
        except:
            self.logger.error("Distribute error", exc_info=True)
        finally:
            self.state = STATE_DONE
            self.logger.info("All data of master have been distributed!")

    def start_distribute(self):
        '''分发数据入口方法，供web接口调用'''
        self.state = STATE_RUNNING
        for _ in six.itervalues(self.clients):
            self.server.send(Message('start', None, None))
        self.logger.info("Master start distributing data!")
        self.greenlet.spawn(self.distributer).join(timeout=30)
        return True
    
    def handle_remain_data(self, data_seq):
        '''处理子节点退回的数据放回主节点队列，供其他节点消费'''
        for data in data_seq:
            self.queue.put_nowait(data)

    def _reset_master(self):
        '''func doc'''
        self.state = STATE_INIT
        self.queue = None
        self.queue_size = 0
        self.init_info = MainNode(self.master_host)
        events.runner_data_refresh.fire(self.init_info)

    def stop(self):
        '''停掉所有slave并重置master'''
        # self.state = STATE_STOPPED
        self.stats.clear()
        self._reset_master()
        for _ in self.clients:
            self.server.send(Message("stop", None, None))


class SlaveRunner(BaseRunner):
    '''class doc'''
    def __init__(self):
        '''func doc'''
        super(SlaveRunner, self).__init__()
        self.logger = get_logger('data_runner.slave')
        self.client_id = socket.gethostname() + "_" + md5(str(time.time() + random.randint(0,10000)).encode('utf-8')).hexdigest()
        self.client = rpc.Client(self.master_host, self.master_bind_port)
        self.greenlet.spawn(self.worker)
        self.client.send(Message('connected', None, self.client_id))
        self.greenlet.spawn(self.reporter)

        def on_report_to_master(client_id, data):
            '''func doc'''
            data["state"] = self.state
            data["queue_size"] = self.queue_size
            data["data_count"] = self.current_queue_size
            data["cpu_percent"] = self.cpu_info
            data["mem_percent"] = self.mem_info
            data["loadavg"] = self.sys_loadavg
        events.report_to_master += on_report_to_master

        def on_make_slave_queue(qsize):
            '''func doc'''
            self.state = STATE_READY
            self.queue_size = qsize
            self.queue = Queue(self.queue_size)
            self.client.send(Message('ready', qsize, self.client_id))
        events.make_slave_queue += on_make_slave_queue

        def on_receive_master_data(data_seq):
            '''func doc'''
            if self.state == STATE_DONE:
                self.client.send(Message('done', data_seq, self.client_id))
            else:
                self.logger.info("start put data into queue!")
                self.put_data(data_seq)
        events.receive_master_data += on_receive_master_data

        def on_reset_slave():
            '''func doc'''
            self.state = STATE_INIT
            self.queue = None
            self.queue_size = 0
            self.client.send(Message('client_reset', None, self.client_id))
        events.reset_slave += on_reset_slave

        def on_slave_stopping():
            self.client.send(Message('stopped', None, self.client_id))
            self.stop()
        events.slave_stopping += on_slave_stopping

    def worker(self):
        '''slave消息监听线程'''
        self.logger.info("Slave worker start!")
        while self.state != STATE_STOPPED:
            msg = self.client.recv()
            if msg.type == 'prepare':
                events.make_slave_queue.fire(msg.data['queue_size'])
            elif msg.type == 'start':
                self.state = STATE_RUNNING
                self.client.send(Message('client_start', None, self.client_id))
            elif msg.type == 'data':
                self.logger.info("receive data from master:{0}".format(msg.data[0]))
                events.receive_master_data.fire(msg.data)
                self.logger.info("handle receive data done!")
            elif msg.type == 'reset':
                events.reset_slave.fire()
            elif msg.type == 'stop':
                events.slave_stopping.fire()
        else:
            self.logger.info("Slave worker stopped!")

    def reporter(self):
        '''slave数据上报线程'''
        while self.state != STATE_STOPPED:
            data = {}
            events.report_to_master.fire(client_id=self.client_id, data=data)
            try:
                self.client.send(Message("stats", data, self.client_id))
            except:
                self.logger.error("Connection lost to master server. Aborting...", exc_info=True)
                break
            gevent.sleep(SLAVE_REPORT_INTERVAL)
        else:
            self.logger.info("Slave reporter is stopped!")

    def put_data(self, data_seq):
        '''获取数据put到salve的队列中'''
        try:
            for data in data_seq:
                self.queue.put_nowait(data)
            self.client.send(Message('done', None, self.client_id))
            self.state = STATE_DONE
        except Full:
            self.logger.warn("client %s queue has been full!" % self.client_id)
            self.client.send(Message('done', None, self.client_id))
        except Exception as e:
            self.logger.error("Slave put data error", exc_info=True)
            return


if __name__ == '__main__':
    global_runner = SlaveRunner()
    s = MasterRunner()
    s.logger.info(123)
    global_runner.logger.info("real test")