#coding: utf-8

import socket
import traceback
import random
import sys
import time
from hashlib import md5

import gevent
from gevent.pool import Group
from gevent.queue import Queue, Empty, Full
import six
from six.moves import xrange
from tomorrow import threads

from data_runner import events
from data_runner import rpc, Message
from data_runner.Glogger import logger
from utils import DictObj



# 全局单例runner
global_runner = None

#用于汇总数据的全局变量
global_stats = DictObj()

STATE_INIT, STATE_READY, STATE_RUNNING, STATE_DONE, STATE_STOPPED = ["connected", "ready", "running", "done", "stopped"]
SLAVE_REPORT_INTERVAL = 1.0
DISTRIBUTE_INTERVAL = 1.0
DISTRIBUTE_RATE = 10000
# MASTER_HOST = "172.16.16.73"
MASTER_HOST = "127.0.0.1"


class BaseRunner(object):
    '''class doc'''
    def __init__(self):
        '''func doc'''
        self.master_bind_host = '*'
        self.master_bind_port = 6666
        self.master_host = MASTER_HOST
        self.stats = global_stats
        self.queue = None
        self.queue_size = 0
        self.slave_put_rate = DISTRIBUTE_RATE
        self.state = STATE_INIT
        self.greenlet = Group()

        def on_runner_data_refresh(runner_data, is_delete=False):
            '''刷新global_stats中各节点的数据'''
            key = hash(runner_data.id)
            if is_delete:
                global_stats.pop(key)
            else:
                row = global_stats.setdefault(key, runner_data)
                row.update(runner_data)
        events.runner_data_refresh += on_runner_data_refresh

        def on_make_data_done():
            '''主节点生产数据完毕时触发该事件'''
            self.state = STATE_DONE
            if self.init_info.role == 'master':
                logger.warn("master send prepare to slave")
                self.prepare_distribute()
        events.make_data_done += on_make_data_done

    @property
    def current_queue_size(self):
        '''当前队列长度'''
        if self.queue:
            return self.queue.qsize()
        else:
            return 0
    def _make_uid(self, mark=0):
        '''根据mark值生成用户id，0：学生，1：教师'''
        return random.randint(1, 0xffffffffffffff) + (mark << 56)

    def _make_cid_generator(self, class_type, num):
        '''根据class_type生产对应的cid'''
        for _ in xrange(num):
            cid = random.randint(1, 0xffffffffffffff) + (class_type << 56)
            yield cid

    @threads(1)
    def make_data(self, struct):
        '''struct = {"total":100, "detail":{0: (100, 2)}} ->{class_type:(class_count, stu_count)}'''
        if self.state != STATE_RUNNING:
            logger.info("Wrong state, start make data failed!")
            return
        if not struct:
            struct = {"total":50000, "detail":{0: (10000, 2), 5: (2000, 5), 12: (20, 1000)}}
        self.queue_size = struct['total']
        self.queue = Queue(self.queue_size)
        try:
            for class_type, count in six.iteritems(struct['detail']):
                class_count, stu_count = count
                for cid in self._make_cid_generator(class_type, class_count):
                    for i in xrange(stu_count):
                        #每节课只添加一位老师
                        if i == 0:
                            uid = self._make_uid(1)
                            self.queue.put_nowait((uid, cid, 1, class_type))
                        #奇数为有操作的学生
                        elif i%2 != 0:
                            uid = self._make_uid(0)
                            self.queue.put_nowait((uid, cid, 0, class_type))
                        #其他为无操作的学生
                        else:
                            uid = self._make_uid(0)
                            self.queue.put_nowait((uid, cid, 2, class_type))

        except Full:
            #实际数据量大于等于队列长度时，实际数据量为队列长度值
            events.make_data_done.fire()
            logger.info("Master make data done, count: %d" % struct['total'])
        else:
            #实际数据量小于队列长度时，数据量为实际数据量
            events.make_data_done.fire()
            logger.info("Master make data done though not reach queue size! count:%s" % self.current_queue_size)

    def get_data(self):
        '''对外提供数据接口'''
        if not self.queue.empty():
            try:
                data = self.queue.get_nowait()
            except:
                data = None
                logger.error("encounter a error when get data from queue!")
            return data

    @threads(1)
    def queue_monitor(self):
        '''主节点队列监听线程'''
        while self.state != STATE_STOPPED:
            self.init_info.qsize = self.queue_size
            self.init_info.state = self.state
            self.init_info.data_count = self.current_queue_size
            events.runner_data_refresh.fire(self.init_info)
            gevent.sleep(0.1)
        else:
            logger.info("stop queue_monitor")

    def start_hatch(self, struct):
        '''func doc'''
        self.state = STATE_RUNNING
        self.make_data(struct)
        logger.info("Start hatching data!")

    def stop(self):
        '''更改runner状态，间接kill掉所有异步线程'''
        self.state = STATE_STOPPED
        # sys.exit(1)

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

    def destroy(self):
        '''func doc'''
        del self


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
    def __init__(self, id, role="master", state=STATE_INIT):
        '''func doc'''
        self.id = id
        self.role = role
        self.state = state
        self.qsize = 0
        self.data_count = 0

class SlaveNode(DictObj):
    '''class doc'''
    def __init__(self, client_id, state=STATE_INIT):
        '''func doc'''
        self.id = client_id
        self.role = "Slave"
        self.state = state
        self.qsize = 0
        self.data_count = 0


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
        self.clients = SlaveNodesDict()
        super(MasterRunner, self).__init__()
        self.server = rpc.Server(self.master_bind_host, self.master_bind_port)
        self.client_listenner()
        self.slave_queue_size = 0
        self.init_info = MainNode(self.master_host)
        self.queue_monitor()

        def on_slave_be_ready(client_id):
            '''slave节点创建队列成功后触发该事件'''
            if client_id not in self.clients:
                self.clients[client_id] = SlaveNode(client_id)
                logger.info("Discarded report from unrecognized slave %s", client_id)
                # return

            self.clients[client_id].state = STATE_READY
            self.clients[client_id].qsize = self.slave_queue_size
            events.runner_data_refresh.fire(self.clients[client_id])
            logger.info("refresh slave state to ready!")
        events.slave_be_ready += on_slave_be_ready

        def on_slave_report(client_id, data):
            '''接收slave上报的数据'''
            if client_id not in self.clients:
                self.clients[client_id] = SlaveNode(client_id)
                logger.info("Discarded report from unrecognized slave %s", client_id)
                # return

            self.clients[client_id].data_count = data["data_count"]
            self.clients[client_id].state = data["state"]
            events.runner_data_refresh.fire(self.clients[client_id])
        events.slave_report += on_slave_report

    def is_valid_slave(self, client_id):
        '''func doc'''
        if client_id in self.clients:
            return True
        else:
            logger.info("Discarded report from unrecognized slave %s", client_id)

    @threads(1)
    def client_listenner(self):
        '''func doc'''
        while self.state != STATE_STOPPED:
            try:
                msg = self.server.recv()
                client_id = msg.client_id
                if msg.type == 'connected':
                    logger.info("The client %s is connected" % client_id)
                    self.clients[client_id] = SlaveNode(client_id)
                    events.runner_data_refresh.fire(self.clients[client_id])
                elif msg.type == 'ready':
                    logger.info("receive ready from slave!")
                    events.slave_be_ready.fire(client_id)
                elif msg.type == 'client_start':
                    logger.info("The client %s start consuming data!" % client_id)
                    self.clients[client_id].state = STATE_RUNNING
                elif msg.type == 'done':
                    logger.info("The data of %s has been done!" % client_id)
                    self.clients[client_id].state = STATE_DONE
                    if msg.data:
                        logger.info("handle %d data returned by client %s" % (len(msg.data), client_id))
                        self.handle_remain_data(msg.data)
                elif msg.type == 'stopped':
                    if client_id in self.clients:
                        events.runner_data_refresh.fire(self.clients[client_id], is_delete=True)
                        del self.clients[client_id]
                        logger.info("The client %s is stopped" % client_id)
                elif msg.type == 'stats':
                    logger.debug("receive client reporter message!")
                    events.slave_report.fire(client_id, msg.data)
                elif msg.type == 'client_reset':
                    logger.info("client-%s has been reset" % client_id)
                    self.clients[client_id].state = STATE_INIT
            except Exception as e:
                logger.error(traceback.format_exc())
                logger.warn("ignore error:%s,continue!" % e)
        else:
            logger.warn("client listener is stopped!")


    @threads(1)
    def distributer(self):
        '''func doc'''
        retry = 0
        while True:
            if self.state == STATE_RUNNING:
                try:
                    for _ in self.clients.running + self.clients.ready:
                        self.distribute_data()
                except:
                    retry += 1
                    logger.info("The master's queue is empty, retry %d time" % retry)
                    gevent.sleep(2)
                    if retry > 4:
                        logger.info("The master's queue is empty, stop distributer!")
                        self.state = STATE_DONE
                        break
                gevent.sleep(DISTRIBUTE_INTERVAL)
            else:
                logger.info("All data of master have been distributed!")
                break

    def prepare_distribute(self):
        '''通知slave创建对应长度的数据队列，为接收数据做准备'''
        if self.state != STATE_DONE:
            logger.warn("Master data do not ready!")
            return
        num_slaves = len(self.clients.connected)
        if not num_slaves:
            logger.warn("no slave servers connected!")
            return
        self.slave_queue_size = self.queue_size // num_slaves or 1
        for client in six.itervalues(self.clients):
            data = {
                "put_rate":self.slave_put_rate,
                "queue_size":self.slave_queue_size,
                "stop_timeout":None
            }
            self.server.send(Message("prepare", data, None))
            logger.info("send prepare to client:%s" % client.id)

    @threads(1)
    def distribute_data(self):
        '''按照固定长度分批次分发数据'''
        temp_data = []
        try:
            for _ in xrange(self.slave_put_rate):
                data = self.queue.get(timeout=2)
                temp_data.append(data)
        except Empty:
            # self.state = STATE_DONE
            raise
        except Exception, e:
            logger.error("master other distribute error:%s" % e)
        finally:
            logger.info("send data to slaves:{0}".format(temp_data[0]))
            self.server.send(Message('data', temp_data, None))

    def start_distribute(self):
        '''分发数据入口方法，供web接口调用'''
        self.state = STATE_RUNNING
        for _ in self.clients.ready:
            self.server.send(Message('start', None, None))
        self.distributer()

    @threads(1)
    def handle_remain_data(self, data_seq):
        '''将节点返回的多余的数据放到主节点队列供其他节点消费'''
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
        global_stats.clear()
        self._reset_master()
        for _ in self.clients:
            self.server.send(Message("stop", None, None))


class SlaveRunner(BaseRunner):
    '''class doc'''
    def __init__(self):
        '''func doc'''
        logger.info("init slave runner")
        super(SlaveRunner, self).__init__()
        self.client_id = socket.gethostname() + "_" + md5(str(time.time() + random.randint(0,10000)).encode('utf-8')).hexdigest()
        self.client = rpc.Client(self.master_host, self.master_bind_port)
        self.worker()
        self.client.send(Message('connected', None, self.client_id))
        self.reporter()

        def on_report_to_master(client_id, data):
            '''func doc'''
            data["state"] = self.state
            data["data_count"] = self.current_queue_size
        events.report_to_master += on_report_to_master

        def on_make_slave_queue(qsize):
            '''func doc'''
            self.state = STATE_READY
            self.queue_size = qsize
            self.queue = Queue(self.queue_size)
            self.client.send(Message('ready', None, self.client_id))
            logger.info("send ready to master!")
        events.make_slave_queue += on_make_slave_queue

        def on_receive_master_data(data_seq):
            '''func doc'''
            if self.state == STATE_DONE:
                self.client.send(Message('done', data_seq, self.client_id))
            else:
                logger.info("start put data into queue!")
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


    @threads(1)
    def worker(self):
        '''slave消息监听线程'''
        logger.info("client worker start!")
        while self.state != STATE_STOPPED:
            msg = self.client.recv()
            if msg.type == 'prepare':
                logger.info("receive prepare from master!")
                events.make_slave_queue.fire(msg.data['queue_size'])
                logger.info("prepare done!")
            elif msg.type == 'start':
                self.state = STATE_RUNNING
                self.client.send(Message('client_start', None, self.client_id))
                logger.info("receive start from master!")
            elif msg.type == 'data':
                logger.info("receive data from master:{0}".format(msg.data[0]))
                events.receive_master_data.fire(msg.data)
                logger.info("handle receive data done!")
            elif msg.type == 'reset':
                logger.info("receive reset cmd from master!")
                events.reset_slave.fire()
            elif msg.type == 'stop':
                events.slave_stopping.fire()
        else:
            logger.info("slave worker is stopped!")

    @threads(1)
    def reporter(self):
        '''slave数据上报线程'''
        while self.state != STATE_STOPPED:
            data = {}
            events.report_to_master.fire(client_id=self.client_id, data=data)
            try:
                self.client.send(Message("stats", data, self.client_id))
                logger.debug("send reporter data to master: %s" % data)
            except:
                logger.error("Connection lost to master server. Aborting...")
                break
            time.sleep(SLAVE_REPORT_INTERVAL)
        else:
            logger.info("reporter is stopped!")

    @threads(1, timeout=2)
    def put_data(self, data_seq):
        '''获取数据put到salve的队列中'''
        try:
            length = len(data_seq)
            for _ in xrange(length):
                data = data_seq.pop()
                self.queue.put(data, timeout=1)
            if self.queue_size == self.current_queue_size:
                data = None
                raise Full("throw a full exception")
        except Full:
            self.state = STATE_DONE
            if data:
                data_seq.append(data)
            logger.info("client %s queue has been full!" % self.client_id)
            self.client.send(Message('done', data_seq, self.client_id))
        except Exception, e:
            logger.error("slave other error: %s" % e)
            return


if __name__ == '__main__':
    import signal

    logger.error("start init slave")
    global_runner = SlaveRunner()
    # global_runner = MasterRunner()
    logger.info("init success!")
    def handle_sig_term():
        global_runner.state = STATE_STOPPED
        logger.info("stop all threads!")
    signal.signal(signal.SIGTERM, handle_sig_term)
