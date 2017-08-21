-- 客户表
CREATE TABLE T_CUSTOMER (
  ID      TEXT NOT NULL PRIMARY KEY,
  NAME    TEXT NOT NULL,
  GENDER  INTEGER,
  ADDRESS TEXT,
  PHONE   TEXT NOT NULL,
  DELETED INTEGER
);

-- 车辆信息表
CREATE TABLE T_VEHICLE (
  ID          TEXT NOT NULL PRIMARY KEY,  --主键
  CUSTOMER_ID TEXT NOT NULL,              --客户ID
  MODEL       TEXT NOT NULL,              --车型
  PRODUCT     TEXT NOT NULL,              --贷款产品
  PERIOD      TEXT NOT NULL,              --期次
  REG_DATE    TEXT NOT NULL,              --车辆登记日期
  REPORT_DATE TEXT,                       --贷款提报日期
  PASSED_DATE TEXT,                       --贷款通过日期
  LOAN_DATE   TEXT NOT NULL,              --放款日期
  TRANSFER_COUNT        INTEGER NOT NULL, --过户次数
  MILEAGE               INTEGER,          --里程数
  INSURANCE_COMPANY     INTEGER,          --承保公司
  INSURANCE_TYPE        TEXT,             --险种
  INSURANCE_START_DATE  TEXT,             --保险生效日期
  INSURANCE_END_DATE    TEXT,             --保险到期日期
  LOAN_TERM   TEXT NOT NULL,              --贷款年限
  LOAN_VALUE  TEXT,                       --贷款金额
  REMARK      TEXT                        --备注
);