-- 账户表
CREATE TABLE T_ACCOUNT (
  ID          TEXT NOT NULL PRIMARY KEY,  --主键
  NAME        TEXT NOT NULL,               --姓名
  PASSWORD    TEXT,                         --密码
  DELETED     INTEGER,                      --是否删除，1 是；0 否
  TYPE        TEXT                          --账户类型
);

-- 字典表
CREATE TABLE T_ACCOUNT (
  ID          TEXT NOT NULL PRIMARY KEY,   --主键
  TYPE        INTEGER NOT NULL,            --字典分类
  VALUE       TEXT,                         --密码
  SORT        INTEGER,                      --排序
  DELETED     INTEGER                       --是否删除，1 是；0 否
);

-- 客户表
CREATE TABLE T_CUSTOMER (
  ID          TEXT NOT NULL PRIMARY KEY,  --主键
  NAME        TEXT NOT NULL,               --姓名
  GENDER      INTEGER,                     --性别，1 男；2 女
  ID_NUMBER   TEXT,                         --身份证号
  ADDRESS     TEXT,                         --地址
  PHONE       TEXT NOT NULL,               --电话
  REMARK      TEXT,                         --备注
  MODIFY_TIME TEXT,                         --修改时间
  DELETED     INTEGER,                      --是否删除，1 是；0 否
  MODIFIER    TEXT                          --修改人
);

-- 车辆信息表
CREATE TABLE T_VEHICLE (
  ID                    TEXT NOT NULL PRIMARY KEY,   --主键
  CUSTOMER_ID           TEXT NOT NULL,                --客户ID

  PLATE_NUM             TEXT NOT NULL,                --车牌号
  MODEL                 TEXT NOT NULL,                --车型
  REG_DATE              TEXT NOT NULL,                --车辆登记日期
  MILEAGE               INTEGER,                       --公里数
  TRANSFER_COUNT        INTEGER NOT NULL,             --过户次数

  LOAN_PRODUCT          TEXT NOT NULL,                --贷款产品
  LOAN_PERIOD           TEXT NOT NULL,                --贷款期次
  LOAN_TERM             INTEGER NOT NULL,             --贷款年限
  LOAN_VALUE            NUMERIC,                      --贷款金额
  LOAN_REPORT_DATE      TEXT,                         --贷款提报日期
  LOAN_PASSED_DATE      TEXT,                         --贷款通过日期
  LOAN_DATE             TEXT NOT NULL,                --放款日期

  INSURANCE_COMPANY     TEXT,                         --承保公司
  INSURANCE_TYPE        TEXT,                         --险种
  INSURANCE_START_DATE  TEXT,                         --保险生效日期
  INSURANCE_END_DATE    TEXT,                         --保险到期日期

  REMARK                TEXT,                         --备注
  MODIFY_TIME           DATETIME,                     --修改时间
  DELETED               INTEGER,                      --是否删除，1 是；0 否
  MODIFIER              TEXT                          --修改人
);