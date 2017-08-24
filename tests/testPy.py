import unittest
import uuid
import datetime


class TestPy(unittest.TestCase):
    # 初始化工作
    def setUp(self):
        pass

    # 退出清理工作
    def tearDown(self):
        pass

    # test date
    def testDate(self):
        now = datetime.date.today()
        print(now)
        threshold = now - datetime.timedelta(days=10)
        print(type(threshold))
        print(threshold)

    # test uuid
    def testUUID(self):
        print(str(uuid.uuid1()).upper())


if __name__ == '__main__':
    TestPy()
