import unittest
import sqlite3

from crm import service


class TestService(unittest.TestCase):
    # 初始化工作
    def setUp(self):
        pass

    # 退出清理工作
    def tearDown(self):
        pass

    # 测试写入客户信息
    # def testInsertCustomer(self):
    #     pass
    #     customer = ("客户3", 1, "地址3", "33333333333", "备注3")
    #     service.CrmService().save_customer(customer)

    # 测试更新客户信息
    # def testUpdateCustomer(self):
    #     customer = ("客户2", 1, "地址2", "13922222222", "备注2")
    #     service.CrmService.update_customer("A8FA37C0-87DD-11E7-A29E-A0C5898674EA", customer)

    # # 测试删除客户信息
    # def testDeleteCustomer(self):
    #     service.CrmService.delete_customer("A8FA37C0-87DD-11E7-A29E-A0C5898674EA")

    # 测试写入车辆信息
    # def testSaveVehicle(self):
    #     vehicle = ("本田思域", "2010-03-08", 50000, 0, "产品1", "1期",
    #                10, 153800.5, "2010-03-01", "2010-03-03", "2010-03-05",
    #                1, "车贷险", "2010-03-10", "2011-03-09", "测试数据")
    #     service.CrmService.save_vehicle(vehicle, "A8FA37C0-87DD-11E7-A29E-A0C5898674EA")

        # 测试写入车辆信息
    # def testUpdateVehicle(self):
    #     vehicle = (None, "本田雅阁", None, 70000, None, None, None,
    #                None, None, None, None, None,
    #                None, None, None, None, None)
    #     service.CrmService.update_vehicle("61FD0FBA-87E1-11E7-BAF7-A0C5898674EA", vehicle)

    # 测试删除车辆信息
    # def testDeleteVehicle(self):
    #     service.CrmService.delete_vehicle("6C7AD07A-87E4-11E7-A201-A0C5898674EA")

    # 测试获取报警
    def testSearchAlarm(self):
        result = service.CrmService.search_alarm(30)
        print(len(result))
        for data in result:
            print(data)


if __name__ == '__main__':
    TestService()
