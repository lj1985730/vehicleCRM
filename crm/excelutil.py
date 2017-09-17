# coding=utf-8
from crm import service
import xlwt
import os


class ExcelUtil:

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def export_vehicle(query):
        """
        导出车辆信息
        :param query:（sheetName, title, 预警天数, 车牌号模糊）
        :return: 导出是否成功
        """
        data = service.search_vehicle(query[2], query[3])

        if len(data) == 0:
            return False

        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet(query[0], cell_overwrite_ok=True)

        sheet.set_col_default_width(0x0016)

        sheet.write_merge(0, 0, 0, 19, query[1])

        borders = xlwt.Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1

        title_font = xlwt.Font()
        title_font.bold = True

        title_style = xlwt.XFStyle()
        title_style.borders = borders
        title_style.font = title_font

        sheet.write(1, 0, u"客户姓名", title_style)
        sheet.write(1, 1, u"客户性别", title_style)
        sheet.write(1, 2, u"身份证号", title_style)
        sheet.col(2).width = 256 * 20
        sheet.write(1, 3, u"客户电话", title_style)
        sheet.col(3).width = 256 * 12

        sheet.write(1, 4, u"车牌号", title_style)
        sheet.write(1, 5, u"车辆型号", title_style)
        sheet.write(1, 6, u"车辆登记日期", title_style)
        sheet.col(6).width = 256 * 13
        sheet.write(1, 7, u"公里数", title_style)
        sheet.write(1, 8, u"过户次数", title_style)

        sheet.write(1, 9, u"贷款产品", title_style)
        sheet.write(1, 10, u"贷款期次", title_style)
        sheet.write(1, 11, u"贷款年限", title_style)
        sheet.write(1, 12, u"贷款金额", title_style)
        sheet.write(1, 13, u"贷款提报日期", title_style)
        sheet.col(13).width = 256 * 13
        sheet.write(1, 14, u"贷款通过日期", title_style)
        sheet.col(14).width = 256 * 13
        sheet.write(1, 15, u"放款日期", title_style)
        sheet.col(15).width = 256 * 11

        sheet.write(1, 16, u"承保公司", title_style)
        sheet.col(16).width = 256 * 15
        sheet.write(1, 17, u"险种", title_style)
        sheet.write(1, 18, u"保险生效日期", title_style)
        sheet.col(18).width = 256 * 13
        sheet.write(1, 19, u"保险到期日期", title_style)
        sheet.col(19).width = 256 * 13
        sheet.write(1, 20, u"备注", title_style)

        body_style = xlwt.XFStyle()
        body_style.borders = borders

        for index in range(0, len(data)):
            vehicle = data[index]
            for c in range(0, 21):
                sheet.write(index + 2, c, vehicle[c], body_style)

        export_path = r".\export"
        if not os.path.exists(export_path):
            os.makedirs(export_path)

        workbook.save((export_path + "\%s.xls") % query[0])
        return True
