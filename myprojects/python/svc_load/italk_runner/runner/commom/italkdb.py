#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import commom.db as db


def _calculate_sharding(id):
    '''founction can change id into a part of table name'''
    # 转换为16进制，并去掉后四位
    #windows对于比较长的整形会默认转换为带L后缀的长整形，为了兼容所以还需将L去掉，updated by 尹志鑫 at2017-05-02
    sharding = hex(id).strip('0x').strip('L')[0:-4]
    # 补全12位表名
    sharding = sharding.zfill(12)
    return sharding

def _get_last_tablename(tabls_key, id):
    key_name = '_'.join([tabls_key, _calculate_sharding(id)])
    # 查询将相关表名全部查询出来，并取出最后一个作为最新的数据
    d = db.select('show tables like ?', key_name + '%')
    table = None
    if d:
        for key, value in d.pop().items():
            table = value
    return table


class tableModel(object):
    '''
    Base class for italk table operation
    '''

    @classmethod
    def find_first(cls, id, is_uid=False):
        if is_uid is True:
            key = 'UID'
        else:
            key = 'CID'
        table_name = _get_last_tablename(cls.__name__, id)
        if table_name is None:
            return {}
        d = db.select_one('select * from %s where %s=?' % (table_name, key ), id)
        return d

    @classmethod
    def find_all(cls, id, is_uid=False):
        if is_uid:
            key = 'UID'
        else:
            key = 'CID'
        table_name = _get_last_tablename(cls.__name__, id)
        if table_name is None:
            return {}
        d = db.select('select * from %s where %s=?' % (table_name, key), id)
        return d

    @classmethod
    def delete_all(cls, id, is_uid=False):
        if is_uid:
            key = 'UID'
        else:
            key = 'CID'
        table_name = _get_last_tablename(cls.__name__, id)
        if table_name is None:
            return {}
        d = db.update('delete from %s where %s=?' % (table_name, key), id)
        return d

    @classmethod
    def find_last(cls, **kw):
        return cls.find_all(**kw).pop()

    @classmethod
    def find_tail(cls, count=1, **kw):
        # 取出队列里倒数count个的结果
        return cls.find_all(**kw)[-count:]


class class_dot_data(tableModel):
    '''
    italk database class_dot_data table explorer
    '''
    def __init__(self, **kw):
        super(class_dot_data, self).__init__(**kw)


class class_activity(tableModel):
    '''
    italk database class_dot_data table explorer
    '''
    def __init__(self, **kw):
        super(class_activity, self).__init__(**kw)


class class_av_quality(tableModel):
    '''
    italk database class_av_quality table explorer
    '''
    def __init__(self, **kw):
        super(class_av_quality, self).__init__(**kw)


class class_chat_record(tableModel):
    '''
    italk database class_chat_record table explorer
    '''
    def __init__(self, **kw):
        super(class_chat_record, self).__init__(**kw)


class class_dot_data(tableModel):
    '''
    italk database class_dot_data table explorer
    '''
    def __init__(self, **kw):
        super(class_dot_data, self).__init__(**kw)


class class_info(tableModel):
    '''
    italk database class_info table explorer
    '''
    def __init__(self, **kw):
        super(class_info, self).__init__(**kw)


class class_login_log(tableModel):
    '''
    italk database class_login_log table explorer
    '''
    def __init__(self, **kw):
        super(class_login_log, self).__init__(**kw)


class class_member(tableModel):
    '''
    italk database class_member table explorer
    '''
    def __init__(self, **kw):
        super(class_member, self).__init__(**kw)


class user_activity(tableModel):
    '''
    italk database user_activity table explorer
    '''
    def __init__(self, **kw):
        super(user_activity, self).__init__(**kw)


class user_login_log(tableModel):
    '''
    italk database user_login_log table explorer
    '''
    def __init__(self, **kw):
        super(user_login_log, self).__init__(**kw)
