# coding=utf-8
import sqlite
import uuid

# 业务层
class CrmService:

    # 新增客户
    def save_customer(self, customer):
        db = sqlite.Database
        sql = "INSERT INTO T_CUSTOMER VALUES (?)" % uuid.uuid1()
