# coding=utf-8
from crm import service
import xlwt
import os


class ExcelUtil:

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def export_vehicle(query):

        data = service.search_vehicle(query[2])

        if len(data) == 0:
            return False

        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet(query[0], cell_overwrite_ok=True)

        sheet.set_col_default_width(0x0016)

        sheet.write_merge(0, 0, 0, 19, query[1])

        sheet.write(1, 0, u"客户姓名")
        sheet.write(1, 1, u"客户性别")
        sheet.write(1, 2, u"客户电话")

        sheet.write(1, 3, u"车牌号")
        sheet.write(1, 4, u"车辆型号")
        sheet.write(1, 5, u"车辆登记日期")
        sheet.write(1, 6, u"公里数")
        sheet.write(1, 7, u"过户次数")

        sheet.write(1, 8, u"贷款产品")
        sheet.write(1, 9, u"贷款期次")
        sheet.write(1, 10, u"贷款年限")
        sheet.write(1, 11, u"贷款金额")
        sheet.write(1, 12, u"贷款提报日期")
        sheet.write(1, 13, u"贷款通过日期")
        sheet.write(1, 14, u"放款日期")

        sheet.write(1, 15, u"承保公司")
        sheet.write(1, 16, u"险种")
        sheet.write(1, 17, u"保险生效日期")
        sheet.write(1, 18, u"保险到期日期")
        sheet.write(1, 19, u"备注")

        for index in range(0, len(data)):
            vehicle = data[index]
            for c in range(0, 19):
                sheet.write(index + 2, c, vehicle[c])

        export_path = r".\export"
        if not os.path.exists(export_path):
            os.makedirs(export_path)

        workbook.save((export_path + "\%s.xls") % query[0])
        return True