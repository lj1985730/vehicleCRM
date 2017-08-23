import unittest
import sqlite3
import uuid


class TestDb(unittest.TestCase):
    # 初始化工作
    def setUp(self):
        self.conn = sqlite3.connect(".\\data\\vehicleCrm.db")

    # 退出清理工作
    def tearDown(self):
        self.conn.commit()
        self.conn.close()

    # 具体的测试用例，一定要以test开头
    # test db
    def testInsert(self):
        cur = self.conn.cursor()
        sql = "INSERT INTO T_CUSTOMER VALUES ('" \
              + str(uuid.uuid1()).upper() + "', " \
            "'测试客户1', '1', '大连市中山区', '13900000000', " \
            "datetime('now', 'localtime'), 0, 'admin');"
        print(sql)
        cur.execute(sql)



        # test uuid
        # def testUUID(self):
        #     print(str(uuid.uuid1()).upper())


if __name__ == '__main__':
    TestDb.main()
