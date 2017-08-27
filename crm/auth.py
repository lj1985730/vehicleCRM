# coding=utf-8
from crm import sqlite


class Auth:

    logon_user = ''

    @classmethod
    def login(cls, account, password):

        if account is None or password is None or account.strip() == '' or password.strip() == '':
            cls.logon_user = None
            return False

        # 数据库对象
        db = sqlite.Database()
        # 操作语句
        sql = "SELECT ID FROM T_ACCOUNT WHERE NAME = ? AND PASSWORD = ?;"
        # 数据集合
        data = (account, password)
        # 执行数据库操作
        result = db.execute_query(sql, data)

        if result is None or (len(result) == 0):
            cls.logon_user = None
            return False
        else:
            cls.logon_user = result[0][0]
            return True

    @classmethod
    def logout(cls):
        cls.logon_user = None

    @classmethod
    def get_logon_account(cls):
        return cls.logon_user
