#coding:utf-8
"""
@author = yinzhixin
@version = 1.0
@summary: 基于DB-API2.0的各种数据库连击配置信息
		  需要安装PyGreSQL、MySQLdb模块
@tips: 1、注意charset设置编码时为utf8，没有通常的横杠'-'
	   2、port为int类型，不能字符串
	   3、各配置参数意义请参考DBUtils文档
"""

import pgdb		
import MySQLdb
from MySQLdb.cursors import DictCursor
from pprint import pprint



PGDB_CONF = {
	'creator': 'pgdb',
	'mincached': 0,
	'maxcached': 0,
	'host': '127.0.0.1',
	'port': 5324,
	'user': 'test',
	'passwd': '1234',
	'db': 'test',
	'charset': 'utf8',
}

MYSQL_CONF = {
	'creator':MySQLdb,
	'mincached': 0,
	'maxcached': 0,
	'host': '127.0.0.1',
	'port': 3306,
	'user': 'test',
	'passwd': 'test',
	'db': 'test',
	'charset': 'utf8'
	#'cursorclass': DictCursor
}


if __name__ =='__main__':
	pprint(MYSQL)

