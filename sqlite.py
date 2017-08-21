# coding=utf-8
import sqlite3
import datetime


# 数据库对象
class Database:

    # 获取数据库游标
    @staticmethod
    def get_cursor():
        conn = sqlite3.connect("data/vehicleCrm.db")
        return conn.cursor()

    # 获取全部数据
    def load_all(self, table_name):
        cur = self.get_cursor()
        res = cur.execute("SELECT * FROM %s" % table_name)
        result = res.fetchall()
        cur.close()
        return result

    # 执行语句
    def execute_sql(self, sql):
        cur = self.get_cursor()
        cur.execute(sql)
        cur.close()
