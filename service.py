# coding=utf-8
import sqlite
import uuid
import datetime
import auth


def get_now():
    """
    :return: 获取当前时间，YYYY-MM-DD HH:mm:ss
    """
    return str(datetime.datetime.now())


def get_uuid():
    """
    :return: 生成新大写UUID
    """
    return str(uuid.uuid1()).upper()


class CrmService:
    """
    业务层
    """
    def __init__(self):
        pass

    '''
    新增客户
    @customer 客户信息元组(名称，性别，地址，电话, 备注)
    '''
    @staticmethod
    def save_customer(customer):
        # 数据库对象
        db = sqlite.Database()
        # 操作语句
        sql = "INSERT INTO T_CUSTOMER VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?);"
        # 数据集合
        data = (get_uuid(),) + customer + (get_now(), auth.Auth.logon_user)
        # 执行数据库操作
        db.execute_update(sql, data)

    '''
    更新客户
    @data_id 客户ID
    @customer 客户信息元组(名称，性别，地址，电话，备注)
    '''
    @staticmethod
    def update_customer(data_id, customer):
        # 数据库对象
        db = sqlite.Database()
        # 操作语句
        sql = "UPDATE T_CUSTOMER SET NAME = ?, GENDER = ?, ADDRESS = ?, PHONE = ?, REMARK = ?," \
              "MODIFY_TIME = ?, DELETED = 0, MODIFIER = ? WHERE ID = ?;"
        # 数据集合
        data = customer + (get_now(), auth.Auth.logon_user, data_id)
        # 执行数据库操作
        db.execute_update(sql, data)

    '''
    删除客户
    @data_id 客户ID
    '''
    @staticmethod
    def delete_customer(data_id):
        # 数据库对象
        db = sqlite.Database()
        # 操作语句
        sql = "UPDATE T_CUSTOMER SET DELETED = 1, MODIFY_TIME = ?, MODIFIER = ? WHERE ID = ?;"
        # 数据集合
        data = (get_now(), auth.Auth.logon_user, data_id)
        # 执行数据库操作
        db.execute_update(sql, data)

    '''
    新增车辆
    @vehicle 车辆信息元组(名称，性别，地址，电话)
    '''
    @staticmethod
    def save_vehicle(vehicle):
        # 数据库对象
        db = sqlite.Database()
        # 操作语句
        sql = "INSERT INTO T_CUSTOMER VALUES (?, ?, ?, ?, ?, ?, 0, ?);"
        # 数据集合
        data = (get_uuid(),) + vehicle + (get_now(), auth.Auth.logon_user)
        # 执行数据库操作
        db.execute_update(sql, data)

    '''
        更新客户
        @data_id 客户ID
        @customer 客户信息元组(名称，性别，地址，电话)
    '''
    @staticmethod
    def update_customer(data_id, customer):
        # 数据库对象
        db = sqlite.Database()
        # 当前时间
        now = str(datetime.datetime.now())
        # 操作语句
        sql = "UPDATE T_CUSTOMER SET NAME = ?, GENDER = ?, ADDRESS = ?, PHONE = ?," \
              "MODIFY_TIME = ?, DELETED = 0, MODIFIER = ? WHERE ID = ?;"
        # 数据集合
        data = customer + (now, auth.Auth.logon_user, data_id)
        # 执行数据库操作
        db.execute_update(sql, data)

    '''
        删除客户
        @data_id 客户ID
        @customer 客户信息元组(名称，性别，地址，电话)
    '''
    @staticmethod
    def delete_customer(data_id):
        # 数据库对象
        db = sqlite.Database()
        # 当前时间
        now = str(datetime.datetime.now())
        # 操作语句
        sql = "UPDATE T_CUSTOMER SET DELETED = 1, MODIFY_TIME = ?, MODIFIER = ? WHERE ID = ?;"
        # 数据集合
        data = (now, auth.Auth.logon_user, data_id)
        # 执行数据库操作
        db.execute_update(sql, data)
