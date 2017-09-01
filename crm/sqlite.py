# coding=utf-8
import sqlite3


# noinspection PyUnresolvedReferences,SqlResolve
class Database(object):

    """
    数据库操作对象
    """
    def __init__(self):
        self.conn = None

    '''
    提交
    '''
    def commit(self):
        self.conn.commit()

    '''
    关闭
    '''
    def close(self):
        self.conn.close()

    '''
    连接数据库
    '''
    def connect(self):
        self.conn = sqlite3.connect("..\\data\\vehicleCrm.db")
        return self.conn

    '''
    执行查询语句
    @sql 要执行的脚本
    @data 数据元组
    '''
    def execute_query(self, sql, data):
        cur = self.connect().cursor()
        if data is not None and len(data) > 0:
            res = cur.execute(sql, data)
        else:
            res = cur.execute(sql)
        result = res.fetchall()
        cur.close()
        self.commit()
        self.close()
        return result

    '''
        执行修改语句
        @sql 要执行的脚本
        @data 数据元组
    '''
    def execute_update(self, sql, data):
        cur = self.connect().cursor()
        if data is not None and len(data) > 0:
            cur.execute(sql, data)
        else:
            cur.execute(sql)
        cur.close()
        self.commit()
        self.close()

    '''
        获取表全部数据
        @table_name 表名
    '''
    def load_all(self, table_name):
        sql = "SELECT * FROM %s;" % table_name
        return self.execute_query(sql, ())

    '''
        获取表某条数据
        @table_name 表名
        @data_id 主键值
    '''
    def load_one(self, table_name, data_id):
        sql = "SELECT * FROM %s WHERE ID = ?;" % table_name
        return self.execute_query(sql, (data_id,))[0]
