#!/opt/venv_python2.7.13/bin/python
#coding:utf-8
from locust import TaskSet, task, events

from SvcLoadLocust import SvcLocust
from runner_settings import LBS_IP_STR
from data_runner import data_runners


class ClassTestTask(TaskSet):
    '''class doc'''
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        try:
            self.data_tup = data_runners.global_runner.queue.get_nowait()
        except Exception as e:
            import time
            events.request_failure.fire(
                request_type = "init",
                name = "get data failed",
                response_time = time.time(),
                exception = e,
            )

    @task
    def test_class(self):
        """func doc"""
        self.client.normal_class_scene(self.data_tup)

    def make_tasks(self, scene):
        '''
        @decription:构造实例tasks，覆盖类属性
        @param scene-{1: weight, 2: weight} task类型: 占比
        '''
        task_list = []
        for task_type, weight in scene.items():
            task = self.task_mapping[task_type]
            for _ in xrange(weight):
                task_list.append(task)
        return task_list
    
    @property
    def task_mapping(self):
        task_map = {
            1: self.test_class,
            2: self.test_enter_class
        }
        return task_map


class ClassUser(SvcLocust):
    '''class doc'''
    host = LBS_IP_STR()
    task_set = ClassTestTask
    min_wait = 2000
    max_wait = 5000



