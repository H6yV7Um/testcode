#coding: utf-8
'''
author: yinzhixin
'''

import time
import logging
import mysql.connector
import requests

from TestManagement.settings import DATABASES


svc_db = DATABASES['svc_load']
DB_INFO = {
        'user': svc_db['USER'],
        'password': svc_db['PASSWORD'],
        'database': svc_db['NAME'],
        'host': svc_db['HOST']
    }

class Dict(dict):
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


class LastRecord(dict):
    '''save the last record when locust stopped'''
    SUPPORT_KEY = set(['pk_id', 'start_time', 'end_time', 'status', 'user_count', 'total_rps', 'hatch_rate', 'fail_ratio', 'stats', 'exceptions'])
    def __init__(self):
        self.connection = None
        self.table = "load_test_record"
        self.start_time = self.cur_time
        self.end_time = None
        self.status = 1
        self.user_count = 0
        self.total_rps = 0
        self.hatch_rate = 0
        self.fail_ratio = 0
        self.stats = None
        self.exceptions = None
        
    def __setattr__(self, attr, value):
        self[attr] = value
        
    def __getattr__(self, key):
        return self[key]
    
    def cursor(self):
        self.connection = mysql.connector.connect(**DB_INFO)
        return self.connection.cursor()

    def close(self):
        try:
            self.cursor.close()
            self.connection.close()
        except:
            pass
    
    def _select(self, sql, *args):
        sql = sql.replace('?', '%s')
        cursor = None
        try:
            cursor = self.cursor()
            cursor.execute(sql, args)
            if cursor.description:
                names = [x[0] for x in cursor.description]
            return [Dict(names, x) for x in cursor.fetchall()]
        except:
            # logger.error('select error:', exc_info=True)
            raise
        finally:
            self.close()
    
    def _update(self, sql, *args):
        sql = sql.replace('?', '%s')
        cursor = None
        try:
            cursor = self.cursor()
            cursor.execute(sql, args)
            r = cursor.rowcount
            self.connection.commit()
            return r
        except:
            # logger.error('update error:', exc_info=True)
            raise
        finally:
            self.close()
    
    def _insert(self, table, **kw):
        cols, args = zip(*kw.items())
        sql = 'insert into `%s` (%s) values (%s)' % (table, ','.join(['`%s`' % col for col in cols]), ','.join(['?' for _ in range(len(cols))]))
        return self._update(sql, *args)
        
    def update_db(self, **kwargs):
        s = "{}=?"
        l, v = [], []
        for key, value in kwargs.items():
            self[key] = value
            t = s.format(key)
            v.append(value)
            l.append(t)
        set_str = ','.join(l)
        sql = "update {} set {} where id={}".format(self.table, set_str, self.pk_id)
        self._update(sql, *v)

    @property
    def record_data(self):
        data = {key:self[key] for key in self.keys() if key in self.SUPPORT_KEY}
        return data
    
    def insert_db(self):
        try:
            self._insert(self.table, **self.record_data)
            last_id_sql = "SELECT @last_id:=id AS last_id FROM {} ORDER BY id DESC LIMIT 1;".format(self.table).replace('?', '%s')
            last_id = self._select(last_id_sql)[0].last_id
            self.pk_id = last_id
        except:
            # logger.error('error:', exc_info=True)
            self.connection.rollback()
            raise
    
    def start_record(self, user_count, hatch_rate):
        self.user_count = user_count
        self.hatch_rate = hatch_rate
        self.insert_db()

    def stop_record(self, fail_ratio, total_rps):
        try:
            self.end_time = self.cur_time
            self.fail_ratio = fail_ratio
            self.total_rps = total_rps
            self.status = 2
            try:
                self.stats = requests.get("http://localhost:8089/stats/requests").content
                self.exceptions = requests.get("http://localhost:8089/exceptions").content
            except Exception as e:
                self.stats = "{}".format(e.message)
                self.exceptions = "{}".format(e.message)
            self.update_db(
                end_time=self.end_time, 
                fail_ratio=self.fail_ratio,
                total_rps=self.total_rps,
                status=self.status,
                stats = self.stats,
                exceptions = self.exceptions
                )
        finally:
            self.close()
    
    @property
    def cur_time(self, fmt='%Y-%m-%d %H:%M:%S'):
        current_time = time.strftime(fmt, time.localtime())
        return current_time




if __name__ == "__main__":
    r = LastRecord()
    # r.update_db(hatch_rate=100, user_count=10000)
    r.start_record(1000, 100)
    r.stop_record(102, 9878)
    # import requests
    # r = requests.get("http://172.16.16.72:8089/stats/requests")
    # print r.content
    # r = requests.get("http://172.16.16.72:8089/exceptions")
    # print r.content