#coding:utf-8

import sys
import time
import json
import MySQLdb
import requests
from config import *


class Connection(object):
  '''use to make connection to mysqldb'''
  def __init__(self, kwargs):
      self._db_args = kwargs
      try:
          self._db = MySQLdb.connect(**self._db_args)
          self._db.autocommit(True)
          self.cursor = self._db.cursor()
      except MySQLdb.Error,e:
          print e
          sys.exit(2)

  def query(self, sql):
    count = self.cursor.execute(sql)
    if count != 0:
      result = self.cursor.fetchone()
      return result
    else:
      return 0


  def close(self):
    self._db.close()

class DictObj(dict):
    """add property to dict object"""   
    def __setattr__(self, name, value):
        self[name] = value

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError, e:
            raise AttributeError(name)

class DataTranform(object):
    """format cursor data"""
    def __init__(self):
        super(DataTranform, self).__init__()

    @classmethod
    def dictfetchall(cls,cursor):
        '''dict'''
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @classmethod
    def namedtuplefetchall(cls,cursor):
        '''namedtuple'''
        desc = cursor.description 
        nt_result = namedtuple('Result', [col[0] for col in desc])
        return [nt_result(*row) for row in cursor.fetchall()]


def taskMonitor(data, method='POST', url=URL):
    response = requests.request(method, url, json=data)
    if response.status_code == requests.codes.ok:
        content = response.json()
        status = json.loads(content)['status']
        print content
        #assert status
    else:
        print response.json()
        raise AssertionError("Requests the interface failed,please check it manually!")

def formatTime(t=1, seconds=None):
  '''return formated time'''
  tformat = {
      1: '%Y%m%d',
      2: '%Y-%m-%d %H:%M:%S',
      3: '%H:%M:%S'
  }
  if t == 3:
      if isinstance(seconds, int):
          ftime = time.strftime(tformat[t], time.gmtime(seconds))
      else:
          raise TypeError("arg seconds must be integer, default None")
  elif t == 0:
    ftime = int(time.time())
  else:
      try:
          ftime = time.strftime(tformat[t], time.localtime())
      except KeyError, e:
          raise e
  return ftime


  