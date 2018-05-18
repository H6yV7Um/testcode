#coding:utf-8

import sys
import re
import requests
import nose
from config import *
from util import Connection, DictObj, formatTime, taskMonitor

def mktime(daykey, t=None):
    import time
    import datetime


def Start():
    db = Connection(DB)
    try:
        daykey = formatTime()
        core_num = db.query(CORE_DELAY_SQL.format(daykey))
        core_rate = db.query(CORE_DELAY_RATE_SQL.format(daykey))
        full_num = db.query(FULL_DELAY_SQL.format(daykey))
        full_rate = db.query(FULL_DELAY_RATE_SQL.format(daykey))
    except Exception, e:
        print "query error!"
        raise e
    finally:
        db.close()
    for key,value in KeyMap.items():
        data = DictObj()
        data.indexkey = value
        data.indextime = formatTime(0)
        data.indexvalue = eval(key)
        data = reqData(data)
        yield taskMonitor,data


if __name__ == '__main__':
    pat = re.compile(r'\d{8}')
    if sys.argv[1] and pat.match(sys.argv[1]):
        daykey = sys.argv[1]
    nose.run()

    




