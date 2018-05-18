import time
import sys
import unittest

from GlobalSettings import *
sys.path.append(RUNNER_DIR)
import svcutils
from svcutils.Glogger import Glogger
from svcutils.db import Dict

logger = Glogger.getLogger()

def key2Path(key):
    '''将命令行参数转化为对应的用例路径'''
    try:
        path = CASE_MAP[key.lower()]
        return path
    except KeyError:
        logger.error("用例路径%s不存在" % key)
        sys.exit(-1)

def _create_test_suite(path):
    test_suites = unittest.defaultTestLoader.discover(
        start_dir = path,    #从开始目录递归搜索子目录，凡是符合pattern的都会被加载
        pattern="test*.py",
        top_level_dir=None
    )
    return test_suites

def _create_test_report(suffix):
    path = os.path.join(BASE_DIR, "test_report")
    name = "test_report%s.html" % suffix
    return file(os.path.join(path, name), "wb"), name

def run(mode, suffix):
    try:
        path = key2Path(mode)
        suite = _create_test_suite(path)
        report_stream, report_name = _create_test_report(suffix)
        report_url = "SVC_Case_{}/test_report/{}".format(mode.upper(), report_name)
        runner = commom.HTMLTestRunner.HTMLTestRunner(
            stream=report_stream,
            title='ItalkIM(SVC)自动化测试报告'
            #description='报告使用python通过svc面向AC的接口进行测试'
        )
        job_name = 'SVC_Case_{}'.format(mode.upper())
        record = RecordObject(job_name, suffix)
        runner.run(suite, record)
        record.update_db(report_url=report_url)
        record.stop(status=2)
    except:
        logger.error("Run test error:", exc_info=True)
        try:
            record.stop(status=0)
        except:
            pass
        raise
    
if __name__ == '__main__':
    print(sys.version_info)
    usage = '''Usage:
样例：python {} p0 20170419
参数：mode-[all,p0,p1,p2], suffix-任意字符串
注意：如果不传参数，mode默认为all，suffix默认为当前时间
    '''.format(sys.argv[0])
    message = '''使用默认参数继续执行?[y|n]: '''
    if len(sys.argv) == 3:
        mode = sys.argv[1]
        suffix = sys.argv[2]
    elif len(sys.argv) == 1:
        print(usage)
        mode = 'all'
        suffix = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
        print(message, end="")
        prompt = input()
        if prompt.lower() != 'y':
            sys.exit(-1)
    else:
        logger.error("参数错误:%s" % sys.argv[1:])
        print(usage)
        sys.exit(-1)
    run(mode, suffix)

