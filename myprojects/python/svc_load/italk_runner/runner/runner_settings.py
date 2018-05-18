#coding:utf-8

'''项目配置文件'''

import os
import logging
import logging.config

from TestManagement.settings import LOGGING, DATABASES
from commom.db import create_engine, select, insert, update, with_transaction


#---------------------Directory Config-------------------------------
#主程序目录
RUNNER_DIR = os.path.dirname(__file__)

#italk_runner根目录
BASE_DIR = os.path.dirname(RUNNER_DIR)

#runner log目录
RUNNER_LOG_PATH = os.path.join(BASE_DIR, 'log')

#整个项目根目录
PROJECT_DIR = os.path.dirname(BASE_DIR)

#-------------------------DB Config-----------------------------------
svc_db = DATABASES['svc_load']
db = {
    72: {
        'user': svc_db['USER'],
        'password': svc_db['PASSWORD'],
        'database': svc_db['NAME'],
        'host': svc_db['HOST']
    }
}

#get config sql
get_config_sql = "select value from common_config where id=?"

#create db engine
try:
    create_engine(**db[72])
except:
    # logger.warning("DB engine already exists!continue..")
    pass

#config value
LBS_IP_STR = lambda: select(get_config_sql,3)[0].value
LBS_PORT = lambda: int(select(get_config_sql, 4)[0].value)
LOCUST_MASTER_IP = lambda: select(get_config_sql,5)[0].value
DATA_RUNNER_MASTER = lambda: select(get_config_sql,2)[0].value 
CLASS_DURATION = lambda: int(select(get_config_sql,6)[0].value)
OP_INTERVAL = lambda: int(select(get_config_sql,7)[0].value)
INFLUXDB_INFO = lambda: select(get_config_sql,8)[0].value.split(':')
SAVE_DATA_INTERVAL = lambda: float(select(get_config_sql,9)[0].value)
HB_INTERVAL = int(select(get_config_sql, 10)[0].value)
SVC_TIMEOUT = int(select(get_config_sql, 11)[0].value)


#------------------Log config------------------------
def get_logger(name):
    logging.config.dictConfig(LOGGING)
    logger = logging.getLogger(name)
    return logger




