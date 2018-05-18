#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import psycopg2cffi
from psycopg2cffi import compat
compat.register()
import pickle
import json
import os
from collections import deque
import subprocess


def clear(fname):
    subprocess.Popen("rm -fr %s" % fname,shell=True)

def writefile(fname,text):
    with open(fname,'a') as f:
        f.write(text + "\n")

def get_field(fname):
    fields=""
    with open(fname,'rt') as f:
        for line in f:
            vlist=json.loads(line).values()
            fields =','.join([key for key in vlist[0].keys()])
            break 
    return fields

class GpConnection(object):
    """connect to gpdb"""
    def __init__(self, constr):
        super(GpConnection, self).__init__()
        self.cursor = psycopg2cffi.connect(constr).cursor()

    def _dictfetchall(self, cursor):
        columns = [str(col[0]) for col in cursor.description]
        newresult = []
        for row in cursor.fetchall():
            itemrow = []
            for item in row:
                itemrow.append(str(item))
            newresult.append(itemrow)
        return [dict(zip(columns, row)) for row in newresult]

    def query(self,sql):
        self.cursor.execute(sql)
        return self._dictfetchall(self.cursor)


def mkgenerator(fname):
    "创建文件生成器大幅度节省内存，但效率慢"
    with open(fname,'r') as f:
        for line in f:
            smallist=json.loads(line)
            if not isinstance(smallist,dict):
                continue
            smallist=smallist.values()
            for value in smallist:
                yield value

def mklist(fname):
    '''读取文件内容构造以dict为元素的list'''
    biglist = []
    with open(fname,'r') as f:
        for line in f:
            smallist=json.loads(line)
            if not isinstance(smallist,dict):
                continue
            smallist=smallist.values()
            biglist.extend(smallist)
    return biglist

def compare(gpresult, biglist):
    '''比较数据'''
    for index, data in enumerate(gpresult,start=1):
        writefile('gporder_id.log', data['order_id'])
        if index%50 == 0:
            print "已比较%s条数据" % index
        forder_list = deque()
        for fdata in biglist:
            if data['order_id'] == fdata['order_id'] and data['order_day_key'] == fdata['order_day_key']:
                forder_list.appendleft(fdata)
        if len(forder_list) > 0:
            text = "-"*10 + "order_id:%s -- 文件中订单记录数:%s" % (data['order_id'],str(len(forder_list))) + "-"*10
            writefile('same_order_diff.log', text)
            for k,v in data.items():
                #if not v:
                    #continue
                if k == "user_address":
                    text = "order_id:%s;gp_address:%s;f_address:%s" % (data['order_id'],v,forder_list[0][k])
                    writefile('address.log', text)
                    continue
                elif str(data[k]).strip() == str(forder_list[0][k]).strip():
                    continue
                else:
                    text = "gpdata > %s > %s | filedata > %s > %s" % (k,v,k,forder_list[0][k])
                    writefile('same_order_diff.log', text)
        else:
            writefile("not_exists_order.log", data['order_id'])


if __name__ == '__main__':
    constr = "host=10.19.147.136 port=2345 user=gploader password=VXt1znQuwGb6TR dbname=da_common"
    if len(sys.argv) !=3:
        print '''
---------------输入参数错误！----------------------
命令格式: 
    python gpdb_diff.py fname limitnum 
参数:
    fname: 读取的文件名称，默认在当前路径
    limitnum: 从gpdb查询的数据量
例子: 
    python gpdb_diff.py order_data.txt 200'''
    else:
        fname = sys.argv[1]
        num = sys.argv[2]
        if not os.path.exists(fname):
            print "文件%s不存在!" % fname
            sys.exit(0)
        else:
            print "清理上次执行的日志文件..."
            clear('*.log')
            print "开始从文件获取字段..."
            fields = get_field(fname)
            print "开始从gpdb获取%s条随机数据..." % num
            sql = '''select {0} 
                    from waimai.fact_order_1_prt_order_day_key_20170111 
                    order by random() limit {1};'''.format(fields, num)
            gpdb = GpConnection(constr)
            gpresult = gpdb.query(sql)
            print "开始从文件%s构造超级list..." % fname
            biglist = mklist(fname)
            #biglist = mkgenerator(fname)
            print "开始比较数据..."
            compare(gpresult, biglist)
            print "数据处理完成！"
            print '''
Tips: 从数据库查询的order_id会写入 gporder_id.log
      相同订单的某些字段值不同写入 same_order_diff.log
      数据库中取出的订单不存在于文件的写入 not_exists_order.log'''


