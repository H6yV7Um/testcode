#coding:utf-8

import sys
import re
import requests
import nose
from config import *
from util import Connection, DictObj, formatTime, taskMonitor




def Start(daykey, indextime):
    db = Connection(DB)
    try:
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
        data.indextime = indextime
        data.indexvalue = eval(key)
        data = reqData(data)
        print data
        taskMonitor(data)


if __name__ == '__main__':
    def mktime(daykey):
        import time
        import datetime
        a = datetime.date(int(daykey[0:4]), int(daykey[4:6]), int(daykey[6:]))
        timestamp = time.mktime(a.timetuple())
        return int(timestamp)
    pat = re.compile(r'\d{8}')
    if len(sys.argv)==2 and pat.match(sys.argv[1]):
        daykey = sys.argv[1]
        indextime = mktime(daykey)
        Start(daykey, indextime)
    else:
        print "invalid arg... eg: python manual.py 20161216"


    




