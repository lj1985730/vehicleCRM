# coding=utf-8
"""
业务层
"""
import datetime
import uuid
import wx

from crm import auth, sqlite


def get_now():
    """
    :return: 当前时间，yyyy-MM-dd HH:mm:ss
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_uuid():
    """
    :return: 生成新大写UUID
    """
    return str(uuid.uuid1()).upper()


def search_customer(name):
    """
    :return: 客户信息元组(名称，性别，地址，电话, 备注)
    """
    # 数据库对象
    db = sqlite.Database()
    # # 操作语句
    sql = "SELECT NAME, CASE WHEN GENDER = 1 THEN '男' ELSE '女' END AS GENDER," \
          " PHONE, ADDRESS, REMARK, ID FROM T_CUSTOMER WHERE DELETED = 0"

    query = None

    # if auth.Auth.logon_user[2] == 2:
    #     sql = sql + " AND MODIFIER = ?"
    #     query = (auth.Auth.logon_user[0],)

    if name is not None and name != '':
        sql = sql + " AND NAME LIKE '%" + name + "%'"

    sql = sql + " ORDER BY NAME ASC"

    # 执行数据库操作
    return db.execute_query(sql, query)


def save_customer(customer):
    """
    新增客户
    @customer 客户
    """

    if check_customer_name_exist(customer[0], None):
        raise ValueError("此姓名已被使用！")

    # 数据库对象
    db = sqlite.Database()
    # 操作语句
    sql = "INSERT INTO T_CUSTOMER(ID, NAME, GENDER, PHONE, ADDRESS, REMARK, DELETED, MODIFY_TIME, MODIFIER) " \
          "VALUES (?, ?, ?, ?, ?, ?, 0, ?, ?);"
    # 数据集合
    data = (get_uuid(),) + customer + (get_now(), auth.Auth.logon_user[0])
    # 执行数据库操作
    db.execute_update(sql, data)
    return True


def update_customer(customer_id, customer):
    """
    更新客户
    @customer_id 客户ID
    @customer 客户信息元组(名称，性别，地址，电话，备注)
    """

    if check_customer_name_exist(customer[0], customer_id):
        raise ValueError("此姓名已被使用！")

    # 数据库对象
    db = sqlite.Database()
    # 操作语句
    sql = "UPDATE T_CUSTOMER SET NAME = ?, GENDER = ?, PHONE = ?, ADDRESS = ?, REMARK = ?," \
          "MODIFY_TIME = ?, DELETED = 0, MODIFIER = ? WHERE ID = ?;"
    # 数据集合
    data = customer + (get_now(), auth.Auth.logon_user[0], customer_id)
    # 执行数据库操作
    db.execute_update(sql, data)
    return True


def check_customer_name_exist(customer_name, customer_id):
    """
    客户名称校验
    @customer_name 客户名称
    @customer_id   客户ID
    """
    # 数据库对象
    db = sqlite.Database()
    # 操作语句
    sql = "SELECT 1 FROM T_CUSTOMER WHERE NAME = ? AND DELETED = 0"
    query = (customer_name,)

    if customer_id is not None:
        sql += " AND ID <> ?"
        query = query + (customer_id,)
    # 执行数据库操作
    return len(db.execute_query(sql, query)) > 0


def delete_customer(data_id):
    """
    删除客户
    @data_id 客户ID
    """
    # 数据库对象
    db = sqlite.Database()
    # 操作语句
    sql = "UPDATE T_CUSTOMER SET DELETED = 1, MODIFY_TIME = ?, MODIFIER = ? WHERE ID = ?;"
    # 数据集合
    data = (get_now(), auth.Auth.logon_user[0], data_id)
    # 执行数据库操作
    db.execute_update(sql, data)


def search_vehicle(alarm_day_count):
    """
    获取需要报警的车辆信息
    @alarm_day_count 提前报警天数
    @:return List[
        客户名称，客户性别，电话，
        车牌号，车辆型号，车辆登记日期，公里数，过户次数
        贷款产品，贷款期次，贷款年限，贷款金额，贷款提报日期，贷款通过日期，放款日期，
        承保公司，险种，保险生效日期，保险到期日期，
        备注，修改人，修改时间，车辆信息ID，客户ID，账户ID，承保公司ID]
    """
    # 数据库对象
    db = sqlite.Database()
    # 操作语句
    sql = "SELECT B.NAME, CASE WHEN GENDER = 1 THEN '男' ELSE '女' END AS GENDER, B.PHONE, " \
          "A.PLATE_NUM, A.MODEL, A.REG_DATE, A.MILEAGE, A.TRANSFER_COUNT, " \
          "A.LOAN_PRODUCT, A.LOAN_PERIOD, A.LOAN_TERM, A.LOAN_VALUE, A.LOAN_REPORT_DATE, " \
          "A.LOAN_PASSED_DATE, A.LOAN_DATE, " \
          "D.VALUE, A.INSURANCE_TYPE, A.INSURANCE_START_DATE, A.INSURANCE_END_DATE, " \
          "A.REMARK, C.NAME, A.MODIFY_TIME, A.ID, B.ID, C.ID, D.ID " \
          "FROM T_VEHICLE A " \
          "LEFT JOIN T_DICT D ON A.INSURANCE_COMPANY = D.ID AND D.TYPE = 1 " \
          "INNER JOIN T_CUSTOMER B ON A.CUSTOMER_ID = B.ID AND B.DELETED = 0 " \
          "INNER JOIN T_ACCOUNT C ON A.MODIFIER = C.ID "

    # if auth.Auth.logon_user[2] == 2:
    #     sql = sql + "AND C.ID = ? "

    sql = sql + "WHERE A.DELETED = 0 AND A.INSURANCE_END_DATE <= ? ORDER BY A.INSURANCE_END_DATE ASC;"

    today = datetime.date.today()
    threshold_day = today + datetime.timedelta(days=alarm_day_count)

    # 数据集合
    # if auth.Auth.logon_user[2] == 2:
    #     data = (auth.Auth.logon_user[0], threshold_day.strftime('%Y-%m-%d'),)
    # else:
    data = (threshold_day.strftime('%Y-%m-%d'),)

    # 执行数据库操作
    return db.execute_query(sql, data)


def save_vehicle(vehicle):
    """
    新增车辆
    @vehicle 车辆信息元组(
        客户ID，车牌号，型号，车辆登记日期，公里数，过户次数，
        贷款产品，贷款期次，贷款年限，贷款金额，贷款提报日期，贷款通过日期，放款日期，
        承保公司ID，险种，保险生效日期，保险到期日期，
        备注)
    """

    if check_plate_num_exist(vehicle[1], None):
        raise ValueError("此车牌号已被使用！")

    # 数据库对象
    db = sqlite.Database()
    # 操作语句
    sql = "INSERT INTO T_VEHICLE VALUES (?,  ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,  ?, 0, ?);"
    # 数据集合
    data = (get_uuid(),) + vehicle + (get_now(), auth.Auth.logon_user[0])
    # 执行数据库操作
    db.execute_update(sql, data)


def update_vehicle(data_id, vehicle):
    """
    更新车辆
    @data_id 车辆ID
    @vehicle 车辆信息元组(
        客户ID，车牌号，型号，车辆登记日期，公里数，过户次数，
        贷款产品，贷款期次，贷款年限，贷款金额，贷款提报日期，贷款通过日期，放款日期，
        承保公司ID，险种，保险生效日期，保险到期日期，
        备注)
    """

    if check_plate_num_exist(vehicle[1], data_id):
        raise ValueError("此车牌号已被使用！")

    # 数据库对象
    db = sqlite.Database()
    # 操作语句
    sql = "UPDATE T_VEHICLE SET DELETED = 0"

    data = []
    if not vehicle[0] is None:
        sql = sql + ", CUSTOMER_ID = ?"
        data.append(vehicle[0])
    if not vehicle[1] is None:
        sql = sql + ", PLATE_NUM = ?"
        data.append(vehicle[1])
    if not vehicle[2] is None:
        sql = sql + ", MODEL = ?"
        data.append(vehicle[2])
    if not vehicle[3] is None:
        sql = sql + ", REG_DATE = ?"
        data.append(vehicle[3])
    if not vehicle[4] is None:
        sql = sql + ", MILEAGE = ?"
        data.append(vehicle[4])
    if not vehicle[5] is None:
        sql = sql + ", TRANSFER_COUNT = ?"
        data.append(vehicle[5])
    if not vehicle[6] is None:
        sql = sql + ", LOAN_PRODUCT = ?"
        data.append(vehicle[6])
    if not vehicle[7] is None:
        sql = sql + ", LOAN_PERIOD = ?"
        data.append(vehicle[7])
    if not vehicle[8] is None:
        sql = sql + ", LOAN_TERM = ?"
        data.append(vehicle[8])
    if not vehicle[9] is None:
        sql = sql + ", LOAN_VALUE = ?"
        data.append(vehicle[9])
    if not vehicle[10] is None:
        sql = sql + ", LOAN_REPORT_DATE = ?"
        data.append(vehicle[10])
    if not vehicle[11] is None:
        sql = sql + ", LOAN_PASSED_DATE = ?"
        data.append(vehicle[11])
    if not vehicle[12] is None:
        sql = sql + ", LOAN_DATE = ?"
        data.append(vehicle[12])
    if not vehicle[13] is None:
        sql = sql + ", INSURANCE_COMPANY = ?"
        data.append(vehicle[13])
    if not vehicle[14] is None:
        sql = sql + ", INSURANCE_TYPE = ?"
        data.append(vehicle[14])
    if not vehicle[15] is None:
        sql = sql + ", INSURANCE_START_DATE = ?"
        data.append(vehicle[15])
    if not vehicle[16] is None:
        sql = sql + ",INSURANCE_END_DATE = ?"
        data.append(vehicle[16])
    if not vehicle[17] is None:
        sql = sql + ",REMARK = ?"
        data.append(vehicle[17])

    # 固定内容
    sql = sql + ",MODIFY_TIME = ?, MODIFIER = ? WHERE ID = ?"
    data.append(get_now())
    data.append(auth.Auth.logon_user[0])
    data.append(data_id)

    # list转tuple
    data_tuple = tuple(data)
    # 执行数据库操作
    db.execute_update(sql, data_tuple)


def check_plate_num_exist(plate_num, vehicle_id):
    """
    车牌照校验
    @plate_num     车牌照
    @vehicle_id     车辆ID
    """
    # 数据库对象
    db = sqlite.Database()
    # 操作语句
    sql = "SELECT 1 FROM T_VEHICLE WHERE PLATE_NUM = ? AND DELETED = 0"
    query = (plate_num,)

    if vehicle_id is not None:
        sql += " AND ID <> ?"
        query = query + (vehicle_id,)
    # 执行数据库操作
    return len(db.execute_query(sql, query)) > 0


def delete_vehicle(data_id):
    """
    删除车辆
    @data_id 车辆ID
    """
    # 数据库对象
    db = sqlite.Database()
    # 操作语句
    sql = "UPDATE T_VEHICLE SET DELETED = 1, MODIFY_TIME = ?, MODIFIER = ? WHERE ID = ?;"
    # 数据集合
    data = (get_now(), auth.Auth.logon_user[0], data_id)
    # 执行数据库操作
    db.execute_update(sql, data)


def search_dict(dic_type):
    """
    获取字典列表
    @dic_type 字典类型
    """
    # 数据库对象
    db = sqlite.Database()
    # 操作语句
    sql = "SELECT ID, VALUE" \
          " FROM T_DICT" \
          " WHERE DELETED = 0 AND TYPE = ?" \
          " ORDER BY SORT ASC;"

    # 执行数据库操作
    return db.execute_query(sql, (dic_type,))
