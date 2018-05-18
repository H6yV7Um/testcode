#coding:utf-8
"""
@author = yinzhixin
@version = 1.0

"""

from DBUtils.PooledDB import PooledDB
from DBUtils.PooledPg import PooledPg
from DBConfig import MYSQL_CONF, PGDB_CONF


class BaseDB(object):
    """
    @summary:数据库连接基类，包含公用方法，
            不同数据库定义各自的连接类，
            继承自该基类获取操作数据库方法
    @note:该类不可以实例化

    """
    def __init__(self):
        raise RuntimeError("The BaseDB can not be instanced")

    def __dictfetchall(self, cursor):
        """
        @return:[{k:v,k2:v2},{}....]
        """
        coloumns = [row[0] for row in cursor.description]
        result = []
        for row in cursor.fetchall():
            itemrow = []
            for item in row:
                itemrow.append(str(item))
            result.append(itemrow)
        return [dict(zip(coloumns, row)) for row in result]

    def __getInsertId(self):
        """
        获取当前连接最后一次插入操作生成的id,如果没有则为０
        """
        self._cursor.execute("SELECT @@IDENTITY AS id")
        result = self._cursor.fetchall()
        return result[0]['id']

    def __query(self, sql, *param):
        """
        内部共用方法，供增删改查方法调用
        """
        if not param:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql,*param)
        return count


    def query(self, sql, *param):
        """
        @summary:select查询
        @notes:count小于0时默认返回的是None
        """
        count = self.__query(sql, *param)
        if count > 0:
            result = self.__dictfetchall(self._cursor)
            return result

    def insert(self,sql,*param):
        self.__query(sql, *param)
        return self.__getInsertId()

    def update(self,sql,param=None):
        return self.__query(sql,param)

    def delete(self,sql,param=None):
        return self.__query(sql,param)

    def dispose(self,isEnd=1):
        """
        @summary: 释放连接池资源
        """
        self._cursor.close()
        self._conn.close()


class Mysql(BaseDB):
    """mysql连接类"""
    _pool = None

    def __init__(self):
        self._cursor = self._conn.cursor()  

    @property
    def _conn(self):
        if Mysql._pool is None:
            Mysql._pool = PooledDB(**MYSQL_CONF)
            #Mysql._pool = PersistentDB(**MYSQL_CONF)
        return Mysql._pool.connection()


class GPDB(BaseDB):
    """GPDB连接类"""
    _pool = None

    def __init__(self):
        self._cursor = self._conn.cursor()

    @property
    def _conn(self):
        if GPDB._pool is None:
            GPDB._pool = PooledPg(**GPDB_CONF)
        return GPDB._pool.connection()


"""
也许有人会说，连接池类代码类同，为啥不直接写到基类里，通过传参调用这一个基类就足够了
开始我也是这么想的，可细细一想，这样有几点弊端：
1、需要在基类定义多个连接池，继而多种判断使用不同连接池
2、每次实调用需要通过传参确定使用哪种连接，效率不高
3、如果某种数据库改为其他连接方式了，此时就杯具了
所以把个数据库连接单拎出来好处是大大的，正所谓，低耦合，欢乐多，看着美，维护易。

"""

if __name__ == '__main__':
    #forbidden = BaseDB()
    db = Mysql()
    result = db.query("select * from %s limit %s" % ('test_table',2))
    print result
    db.dispose()