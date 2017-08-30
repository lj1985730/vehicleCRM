# coding=utf-8
import wx
import wx.grid as gridlib
from crm import service, customerwin


class CustomerPanel(wx.Panel):
    """
    客户面板
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
        self.enable_btn()

        self.grid = CustomerGrid(self)
        sizer.Add(self.grid, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(sizer)

    def enable_btn(self):
        self.Bind(wx.EVT_MENU, self.open_create, self.createBtn)
        self.Bind(wx.EVT_MENU, self.on_exit, self.updateBtn)
        self.Bind(wx.EVT_MENU, self.on_show_customer, self.deleteBtn)

    def open_create(self):
        self.edit_win = customerwin.CustomerWin()
        self.edit_win.CenterOnScreen()

        val = self.edit_win.ShowModal()

        if val == wx.ID_OK:
            self.edit_win.do_login()
            self.toggle_menu()

            self.edit_win.Destroy()


class CustomerDataTable(gridlib.GridTableBase):
    """
    客户网格数据
    """
    def __init__(self):
        gridlib.GridTableBase.__init__(self)
        self.colLabels = ['姓名', '性别', '电话', '住址', '备注']
        self.dataTypes = [
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING
        ]
        self.data = service.CrmService.search_customer()

    # required methods for the wxPyGridTableBase interface
    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return 5

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


class CustomerGrid(gridlib.Grid):
    """
    客户网格
    """
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1)

        self.SetTable(CustomerDataTable(), True)

        self.AutoSize()
        self.CanDragGridSize()
        self.EnableEditing(False)

        self.SetColLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        self.SetDefaultCellAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

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
        # attr = gridlib.GridCellAttr()
        # attr.SetTextColour(wx.BLACK)
        # attr.SetBackgroundColour(wx.RED)
        # attr.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        #
        # # you can set cell attributes for the whole row (or column)
        # self.SetRowAttr(5, attr)
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
