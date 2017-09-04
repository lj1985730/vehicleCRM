# coding=utf-8
from crm import sqlite


class Auth:

    logon_user = None

    @classmethod
    def login(cls, account, password):

        if account is None or password is None or account.strip() == '' or password.strip() == '':
            cls.logon_user = None
            return False

        # 数据库对象
        db = sqlite.Database()
        # 操作语句
        sql = "SELECT ID, NAME, TYPE FROM T_ACCOUNT WHERE NAME = ? AND PASSWORD = ? AND DELETED = 0;"
        # 数据集合
        data = (account, password)
        # 执行数据库操作
        result = db.execute_query(sql, data)

        if result is None or (len(result) == 0):
            cls.logon_user = None
            return False
        else:
            cls.logon_user = result[0]
            if cls.logon_user[2] == 0:
                cls.register()
            return True

    @classmethod
    def logout(cls):
        cls.logon_user = None

    @classmethod
    def get_logon_account(cls):
        return cls.logon_user

    '''
    激活
    '''
    @classmethod
    def register(cls):
        # 数据库对象
        db = sqlite.Database()
        sql = "UPDATE T_DICT SET VALUE = 1 WHERE TYPE = 0"
        db.execute_update(sql, None)

    '''
    判断激活
    '''
    @classmethod
    def registered(cls):
        # 数据库对象
        db = sqlite.Database()
        sql = "SELECT 1 FROM T_DICT WHERE TYPE = 0 AND VALUE = 1"
        return db.execute_query(sql, None)
