# coding=utf-8
import wx
import wx.grid as gridlib
from crm import service


class CustomerPanel(wx.Panel):
    """
    客户面板
    """
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.grid = CustomerGrid(self)


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
            return not self.data[row][col+1]
        except IndexError:
            return True

    def GetValue(self, row, col):
        try:
            return self.data[row][col+1]
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
