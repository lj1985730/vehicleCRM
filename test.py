import unittest
import sqlite3
import uuid


class Test(unittest.TestCase):
    # 初始化工作
    def setUp(self):
        pass

    # 退出清理工作
    def tearDown(self):
        pass

    # 具体的测试用例，一定要以test开头
    # test db
    # def testGenerateDb(self):
    #     conn = sqlite3.connect(".\\data\\vehicleCrm.db")

    # test uuid
    def testUUID(self):
        print(str(uuid.uuid1()).upper())


if __name__ == '__main__':
    Test.main()
