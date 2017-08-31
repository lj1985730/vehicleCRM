# coding=utf-8
import wx
import wx.grid as gridlib
from crm import service
import datetime


class VehiclePanel(wx.Panel):
    """
    车辆面板
    """

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        sizer = wx.BoxSizer(wx.VERTICAL)

        opt_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.createBtn = wx.Button(self, wx.ID_ANY, u"新增", wx.DefaultPosition, wx.DefaultSize, 0)
        opt_sizer.Add(self.createBtn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.updateBtn = wx.Button(self, wx.ID_ANY, u"修改", wx.DefaultPosition, wx.DefaultSize, 0)
        opt_sizer.Add(self.updateBtn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.deleteBtn = wx.Button(self, wx.ID_ANY, u"删除", wx.DefaultPosition, wx.DefaultSize, 0)
        opt_sizer.Add(self.deleteBtn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        sizer.Add(opt_sizer, 0, wx.ALIGN_RIGHT, 5)

        self.grid = VehicleGrid(self)
        sizer.Add(self.grid, 1, wx.ALL | wx.EXPAND, 0)

        self.SetSizer(sizer)


class VehicleDataTable(gridlib.GridTableBase):
    """
    车辆网格数据
    """

    def __init__(self):
        gridlib.GridTableBase.__init__(self)
        self.colLabels = ['客户姓名', '车辆型号', '车辆登记日期', '里程数', '过户次数',
                          '贷款产品', '贷款期次', '贷款年限', '贷款金额', '贷款提报日期', '贷款通过日期', '放款日期',
                          '承保公司', '险种', '保险生效日期', '保险到期日期', '备注', '修改时间', '修改人']
        self.dataTypes = [
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING
        ]
        self.data = service.CrmService.search_vehicle(None)

    # required methods for the wxPyGridTableBase interface
    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return 19

    def IsEmptyCell(self, row, col):
        try:
            return not self.data[row][col]
        except IndexError:
            return True

    def GetValue(self, row, col):
        try:
            return self.data[row][col]
        except IndexError:
            return ''

    def SetValue(self, row, col, value):
        pass

    def GetColLabelValue(self, col):
        return self.colLabels[col]


class VehicleGrid(gridlib.Grid):
    """
    车辆网格
    """
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1)

        table = VehicleDataTable()
        self.SetTable(table, True)

        self.AutoSize()
        self.CanDragGridSize()
        self.EnableEditing(False)

        self.SetColLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        self.SetDefaultCellAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

        # alarm threshold day
        today = datetime.date.today()
        threshold_day_30 = today + datetime.timedelta(days=30)
        threshold_day_60 = today + datetime.timedelta(days=60)
        threshold_day_90 = today + datetime.timedelta(days=90)

        # add alarm row style
        table_data = table.data
        for index in range(len(table_data)):
            if table_data[index][15] <= threshold_day_90.strftime('%Y-%m-%d'):
                self.set_row_yellow(index)
            if table_data[index][15] <= threshold_day_60.strftime('%Y-%m-%d'):
                self.set_row_orange(index)
            if table_data[index][15] <= threshold_day_30.strftime('%Y-%m-%d'):
                self.set_row_red(index)

                # simple cell formatting

                # self.SetColSize(3, 200)
                # self.SetRowSize(4, 45)
                # self.SetCellValue(0, 0, "First cell")
                # self.SetCellValue(1, 1, "Another cell")
                # self.SetCellValue(2, 2, "Yet another cell")
                # self.SetCellValue(3, 3, "This cell is read-only")
                # self.SetCellFont(0, 0, wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))
                # self.SetCellTextColour(1, 1, wx.RED)
                # self.SetCellBackgroundColour(2, 2, wx.CYAN)
                # self.SetReadOnly(3, 3, True)
                #
                # self.SetCellEditor(5, 0, gridlib.GridCellNumberEditor(1, 1000))
                # self.SetCellValue(5, 0, "123")
                # self.SetCellEditor(6, 0, gridlib.GridCellFloatEditor())
                # self.SetCellValue(6, 0, "123.34")
                # self.SetCellEditor(7, 0, gridlib.GridCellNumberEditor())
                #
                # self.SetCellValue(6, 3, "You can veto editing this cell")
                #
                # # self.SetRowLabelSize(0)
                # # self.SetColLabelSize(0)
                #
                # # attribute objects let you keep a set of formatting values
                # # in one spot, and reuse them if needed

                #
                # self.SetColLabelValue(0, "Custom")
                # self.SetColLabelValue(1, "column")
                # self.SetColLabelValue(2, "labels")
                #
                # self.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_BOTTOM)
                #
                # self.SetCellSize(11, 1, 3, 3)
                # self.SetCellAlignment(11, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
                # self.SetCellValue(11, 1, "This cell is set to span 3 rows and 3 columns")
                #
                # renderer = gridlib.GridCellAutoWrapStringRenderer()
                # self.SetCellRenderer(15, 0, renderer)
                # self.SetCellValue(15, 0, "The text in this cell will be rendered with word-wrapping")

    def set_row_red(self, row_number):
        attr = gridlib.GridCellAttr()
        attr.SetTextColour(wx.BLACK)
        attr.SetBackgroundColour(wx.RED)
        attr.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.SetRowAttr(row_number, attr)

    def set_row_orange(self, row_number):
        attr = gridlib.GridCellAttr()
        attr.SetTextColour(wx.BLACK)
        attr.SetBackgroundColour((250, 128, 10))
        attr.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.SetRowAttr(row_number, attr)

    def set_row_yellow(self, row_number):
        attr = gridlib.GridCellAttr()
        attr.SetTextColour(wx.BLACK)
        attr.SetBackgroundColour(wx.YELLOW)
        attr.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.SetRowAttr(row_number, attr)
