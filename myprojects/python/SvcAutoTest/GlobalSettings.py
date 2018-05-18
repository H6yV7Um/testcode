#coding:utf-8
import os


#数据库配置
DB_INFO = {
    'user': 123,
    'password': 123,
    'database': 'test',
    'host': '172.16.16.72',
    'port': 3306
}

#主程序目录
RUNNER_DIR = os.path.dirname(__file__)

#项目根目录
BASE_DIR = os.path.dirname(RUNNER_DIR)

#测试报告目录
REPORT_DIR = os.path.join(BASE_DIR, 'test_report')

#测试用例根目录及根据优先级分类后的子目录
CASE_ROOT_DIR = os.path.join(RUNNER_DIR, 'tests')
P0 = os.path.join(CASE_ROOT_DIR,"P0")
P1 = os.path.join(CASE_ROOT_DIR,"P1")
P2 = os.path.join(CASE_ROOT_DIR,"P2")

CASE_MAP = {
    'all': CASE_ROOT_DIR,
    'p0': P0,
    'p1': P1,
    'p2': P2
    }

LBS_IP = '172.16.16.25'
MBT_PORT = 6010
PB_PORT = 6000