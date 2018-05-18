import time

import mysql.connector

from GlobalSettings import DB_INFO

class RecordObject(dict):
    SUPPORT_KEY = set(['pk_id', 'start_time', 'end_time', 'job_name', 'build_no', 'status', 'total_executed', 'success_count', 'failure_count', 'error_count', 'report_url'])
    def __init__(self, job_name, bn):
        self.connection = mysql.connector.connect(**DB_INFO)
        self.start_time = self.cur_time
        self.end_time = None
        self.job_name = job_name
        self.build_no = bn
        self.status = 1
        self.total_executed = 0
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.report_url = None
        self.insert_db()
        
    def __setattr__(self, attr, value):
        self[attr] = value
        
    def __getattr__(self, key):
        return self[key]
    
    def cursor(self):
        return self.connection.cursor()
    
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
            logger.error('select error:', exc_info=True)
            raise
        finally:
            if cursor:
                cursor.close()
    
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
            logger.error('update error:', exc_info=True)
        finally:
            if cursor:
                cursor.close()
    
    def _insert(self, table, **kw):
        cols, args = zip(*kw.iteritems())
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
        sql = "update auto_test_record set {} where id={}".format(set_str, self.pk_id)
        self._update(sql, *v)

    @property
    def record_data(self):
        data = {key:self[key] for key in self.keys() if key in self.SUPPORT_KEY}
        return data
    
    def insert_db(self):
        try:
            self._insert('auto_test_record', **self.record_data)
            last_id_sql = "SELECT @last_id:=id AS last_id FROM auto_test_record ORDER BY id DESC LIMIT 1;".replace('?', '%s')
            last_id = self._select(last_id_sql)[0].last_id
            self.pk_id = last_id
        except:
            logger.error('error:', exc_info=True)
            self.connection.rollback()
            raise
        
    def stop(self, status):
        try:
            self.end_time = self.cur_time
            self.status = status
            self.update_db(end_time=self.end_time, status=self.status)
        finally:
            if self.connection:
                self.connection.close()
    
    @property
    def cur_time(self, fmt='%Y-%m-%d %H:%M:%S'):
        current_time = time.strftime(fmt, time.localtime())
        return current_time