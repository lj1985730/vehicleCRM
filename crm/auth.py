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
        sql = "SELECT ID, NAME, TYPE, PASSWORD, LAST FROM T_ACCOUNT WHERE NAME = ? AND PASSWORD = ? AND DELETED = 0;"
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
    def change_pass(cls, old_pass, new_pass):

        if cls.logon_user is None:
            raise ValueError(u"请先登录！")

        if old_pass is None or new_pass is None or old_pass.strip() == '' or new_pass.strip() == '':
            raise ValueError(u"密码不可为空！")

        if not cls.logon_user[3] == old_pass:
            raise ValueError(u"输入旧密码不正确！")

        # 数据库对象
        db = sqlite.Database()
        # 操作语句
        sql = "UPDATE T_ACCOUNT SET PASSWORD = ? WHERE ID = ?;"
        # 数据集合
        data = (new_pass, cls.logon_user[0])
        # 执行数据库操作
        db.execute_update(sql, data)

    @classmethod
    def update_last_login(cls, date):

        if cls.logon_user is None:
            raise ValueError(u"请先登录！")

        # 数据库对象
        db = sqlite.Database()
        # 操作语句
        sql = "UPDATE T_ACCOUNT SET LAST = ? WHERE ID = ?;"
        # 数据集合
        data = (date, cls.logon_user[0])
        # 执行数据库操作
        db.execute_update(sql, data)

    @classmethod
    def logout(cls):
        cls.logon_user = None

    @classmethod
    def get_logon_account(cls):
        return cls.logon_user

    @classmethod
    def register(cls):
        """
        激活
        """
        # 数据库对象
        db = sqlite.Database()
        sql = "UPDATE T_DICT SET VALUE = 1 WHERE TYPE = 0;"
        db.execute_update(sql, None)

    @classmethod
    def registered(cls):
        """
        判断激活
        """
        # 数据库对象
        db = sqlite.Database()
        sql = "SELECT 1 FROM T_DICT WHERE TYPE = 0 AND VALUE = 1;"
        return db.execute_query(sql, None)
