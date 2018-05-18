#encoding: utf-8

import time
import datetime
import decimal
import json
from functools import wraps
import logging
import inspect
import itertools
from random import randint

from django.http import HttpResponseForbidden


def only_support_post(func):
    @wraps(func)
    def wrapper(req):
        if req.method != 'POST':
            return HttpResponseForbidden()
        return func(req)
    return wrapper

def curtime(format='%Y-%m-%d %H:%M:%S'):
    """return current_time"""
    current_time = time.strftime(format, time.localtime())
    return current_time

class CJsonEncoder(json.JSONEncoder):  
    """json序列化工具类，针对特殊数据类型转换为string"""
    def default(self, obj):  
        if isinstance(obj, datetime.datetime):  
            return obj.strftime('%Y-%m-%d %H:%M:%S')  
        elif isinstance(obj, datetime.date):  
            return obj.strftime("%Y-%m-%d")  
        elif isinstance(obj, decimal.Decimal):
            return str(obj)
        elif isinstance(obj, bytes):
            return obj.decode()
        else:  
            return json.JSONEncoder.default(self, obj) 

class DictObj(dict):
    '''
    Simple dict but support access as x.y style.

    >>> d1 = Dict()
    >>> d1['x'] = 100
    >>> d1.x
    100
    >>> d1.y = 200
    >>> d1['y']
    200
    >>> d2 = Dict(a=1, b=2, c='3')
    >>> d2.c
    '3'
    >>> d2['empty']
    Traceback (most recent call last):
        ...
    KeyError: 'empty'
    >>> d2.empty
    Traceback (most recent call last):
        ...
    AttributeError: 'Dict' object has no attribute 'empty'
    >>> d3 = Dict(('a', 'b', 'c'), (1, 2, 3))
    >>> d3.a
    1
    >>> d3.b
    2
    >>> d3.c
    3
    '''
    def __init__(self, names=(), values=(), **kw):
        super(DictObj, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            setattr(self, key, None)
            return self[key]
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


def get_func_name(obj):
    '''获取调用者函数名称'''
    func_name = inspect.stack()[1][3]
    #func_obj = getattr(obj, func_name)
    return func_name

def slice_seq(seq, n, fvalue=randint(1,1000)):
    '''按步长n切割一个可迭代对象'''
    # slice_seq([1,2,3,4], 3, '0') --> (1,2,3) (4,0,0)"
    args = [iter(seq)] * n
    return itertools.izip_longest(*args, fillvalue=fvalue)




if __name__ == '__main__':
    l = [1,2,3,4,5,6]
    s = slice_seq(l, 7)
    