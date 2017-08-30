# coding=utf-8
import datetime
import uuid

from crm import auth, sqlite


def get_now():
    """
    :return: 获取当前时间，YYYY-MM-DD HH:mm:ss
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


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
    查询客户
    @return 客户信息元组(名称，性别，地址，电话, 备注)
    '''
    @staticmethod
    def search_customer():
        # 数据库对象
        db = sqlite.Database()
        # # 操作语句
        sql = "SELECT NAME, CASE WHEN GENDER = 1 THEN '男' ELSE '女' END AS GENDER,"\
            " PHONE, ADDRESS, REMARK, ID FROM T_CUSTOMER WHERE DELETED = 0;"
        # # 执行数据库操作
        return db.execute_query(sql, None)

    '''
    新增客户
    @customer 客户信息元组(名称，性别，电话, 地址，备注)
    '''
    @staticmethod
    def save_customer(customer):
        # 数据库对象
        db = sqlite.Database()
        # # 操作语句
        sql = "INSERT INTO T_CUSTOMER(ID, NAME, GENDER, PHONE, ADDRESS, REMARK, MODIFY_TIME, MODIFIER) " \
              "VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?);"
        # # 数据集合
        data = (get_uuid(),) + customer + (get_now(), auth.Auth.logon_user)
        # # 执行数据库操作
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
        sql = "UPDATE T_CUSTOMER SET NAME = ?, GENDER = ?, PHONE = ?, ADDRESS = ?, REMARK = ?," \
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
    查询客户
    @:return 车辆信息元组(名称，性别，地址，电话, 备注)
    '''
    @staticmethod
    def search_vehicle(customer_id):
        # 数据库对象
        db = sqlite.Database()
        # # 操作语句
        sql = "SELECT B.NAME, A.MODEL, A.REG_DATE, A.MILEAGE, A.TRANSFER_COUNT, " \
              "A.LOAN_PRODUCT, A.LOAN_PERIOD, A.LOAN_TERM, A.LOAN_VALUE, A.LOAN_REPORT_DATE, " \
              "A.LOAN_PASSED_DATE, A.LOAN_DATE, " \
              "A.INSURANCE_COMPANY, A.INSURANCE_TYPE, A.INSURANCE_START_DATE, A.INSURANCE_END_DATE, " \
              "A.REMARK, C.NAME, A.MODIFY_TIME, A.ID " \
              "FROM T_VEHICLE A, T_CUSTOMER B, T_ACCOUNT C " \
              "WHERE A.CUSTOMER_ID = B.ID AND A.MODIFIER = C.ID AND A.DELETED = 0 AND B.DELETED = 0;"

        if customer_id is not None:
            sql = sql + " AND CUSTOMER_ID = ?"

        # # 执行数据库操作
        return db.execute_query(sql, customer_id)

    '''
    新增车辆
    @vehicle 车辆信息元组(
        型号，车辆登记日期，里程数，过户次数，
        贷款产品，贷款期次，贷款年限，贷款金额，贷款提报日期，贷款通过日期，放款日期，
        承保公司，险种，保险生效日期，保险到期日期，
        备注)
    @customer_id 客户信息
    '''
    @staticmethod
    def save_vehicle(vehicle, customer_id):
        # 数据库对象
        db = sqlite.Database()
        # 操作语句
        sql = "INSERT INTO T_VEHICLE VALUES (?, ?,  ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,  ?, 0, ?);"
        # 数据集合
        data = (get_uuid(), customer_id) + vehicle + (get_now(), auth.Auth.logon_user)
        # 执行数据库操作
        db.execute_update(sql, data)

    '''
    更新车辆
    @data_id 车辆ID
    @vehicle 车辆信息元组(
        客户ID，型号，车辆登记日期，里程数，过户次数，
        贷款产品，贷款期次，贷款年限，贷款金额，贷款提报日期，贷款通过日期，放款日期，
        承保公司，险种，保险生效日期，保险到期日期，
        备注)
    '''
    @staticmethod
    def update_vehicle(data_id, vehicle):
        # 数据库对象
        db = sqlite.Database()
        # 操作语句
        sql = "UPDATE T_VEHICLE SET DELETED = 0"

        data = []
        if not vehicle[0] is None:
            sql = sql + ",CUSTOMER_ID = ?"
            data.append(vehicle[0])
        if not vehicle[1] is None:
            sql = sql + ",MODEL = ?"
            data.append(vehicle[1])
        if not vehicle[2] is None:
            sql = sql + ",REG_DATE = ?"
            data.append(vehicle[2])
        if not vehicle[3] is None:
            sql = sql + ",MILEAGE = ?"
            data.append(vehicle[3])
        if not vehicle[4] is None:
            sql = sql + ",TRANSFER_COUNT = ?"
            data.append(vehicle[4])
        if not vehicle[5] is None:
            sql = sql + ",LOAN_PRODUCT = ?"
            data.append(vehicle[5])
        if not vehicle[6] is None:
            sql = sql + ",LOAN_PERIOD = ?"
            data.append(vehicle[6])
        if not vehicle[7] is None:
            sql = sql + ",LOAN_TERM = ?"
            data.append(vehicle[7])
        if not vehicle[8] is None:
            sql = sql + ",LOAN_VALUE = ?"
            data.append(vehicle[8])
        if not vehicle[9] is None:
            sql = sql + ",LOAN_REPORT_DATE = ?"
            data.append(vehicle[9])
        if not vehicle[10] is None:
            sql = sql + ",LOAN_PASSED_DATE = ?"
            data.append(vehicle[10])
        if not vehicle[11] is None:
            sql = sql + ",LOAN_DATE = ?"
            data.append(vehicle[11])
        if not vehicle[12] is None:
            sql = sql + ",INSURANCE_COMPANY = ?"
            data.append(vehicle[12])
        if not vehicle[13] is None:
            sql = sql + ",INSURANCE_TYPE = ?"
            data.append(vehicle[13])
        if not vehicle[14] is None:
            sql = sql + ",INSURANCE_START_DATE = ?"
            data.append(vehicle[14])
        if not vehicle[15] is None:
            sql = sql + ",INSURANCE_END_DATE = ?"
            data.append(vehicle[15])
        if not vehicle[16] is None:
            sql = sql + ",REMARK = ?"
            data.append(vehicle[16])

        # 固定内容
        sql = sql + ",MODIFY_TIME = ?, MODIFIER = ? WHERE ID = ?"
        data.append(get_now())
        data.append(auth.Auth.logon_user)
        data.append(data_id)

        # list转tuple
        data_tuple = tuple(data)
        # 执行数据库操作
        db.execute_update(sql, data_tuple)

    '''
    删除车辆
    @data_id 车辆ID
    '''
    @staticmethod
    def delete_vehicle(data_id):
        # 数据库对象
        db = sqlite.Database()
        # 操作语句
        sql = "UPDATE T_VEHICLE SET DELETED = 1, MODIFY_TIME = ?, MODIFIER = ? WHERE ID = ?;"
        # 数据集合
        data = (get_now(), auth.Auth.logon_user, data_id)
        # 执行数据库操作
        db.execute_update(sql, data)

    '''
    获取需要报警的车辆
    @alarm_day_count 提前报警天数
    '''
    @staticmethod
    def search_alarm(alarm_day_count):
        # 数据库对象
        db = sqlite.Database()
        # 操作语句
        sql = "SELECT A.ID, A.CUSTOMER_ID, A.MODEL, A.REG_DATE, A.MILEAGE, A.TRANSFER_COUNT, " \
              "A.LOAN_PRODUCT, A.LOAN_PERIOD, A.LOAN_TERM, A.LOAN_VALUE, A.LOAN_REPORT_DATE, A.LOAN_PASSED_DATE, " \
              "A.LOAN_DATE, A.INSURANCE_COMPANY, A.INSURANCE_TYPE, A.INSURANCE_START_DATE, A.INSURANCE_END_DATE, " \
              "A.REMARK, A.MODIFY_TIME, " \
              "B.NAME AS CUSTOMER_NAME, B.GENDER, B.PHONE, B.ADDRESS" \
              " FROM T_VEHICLE A, T_CUSTOMER B" \
              " WHERE A.DELETED = 0 AND B.DELETED = 0 AND A.CUSTOMER_ID = B.ID" \
              " AND A.INSURANCE_END_DATE <= ?;"

        today = datetime.date.today()
        threshold_day = today + datetime.timedelta(days=alarm_day_count)

        # 数据集合
        data = (threshold_day.strftime('%Y-%m-%d'),)
        # 执行数据库操作
        return db.execute_query(sql, data)
