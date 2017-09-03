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
        self.service = service.CrmService()
        self.grid = None
        self.edit_win = None
        self.init_layout()

    """
    展现渲染
    """
    def init_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        opt_sizer = wx.BoxSizer(wx.HORIZONTAL)

        create_btn = wx.Button(self, wx.ID_ANY, u"新增")
        self.Bind(wx.EVT_BUTTON, self.open_create, create_btn)
        opt_sizer.Add(create_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        update_btn = wx.Button(self, wx.ID_ANY, u"修改")
        self.Bind(wx.EVT_BUTTON, self.open_modify, update_btn)
        opt_sizer.Add(update_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        delete_btn = wx.Button(self, wx.ID_ANY, u"删除")
        self.Bind(wx.EVT_BUTTON, self.on_delete, delete_btn)
        opt_sizer.Add(delete_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        sizer.Add(opt_sizer, 0, wx.ALIGN_RIGHT, 5)

        self.grid = CustomerGrid(self)
        sizer.Add(self.grid, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(sizer)

    """
    打开新增页
    """
    def open_create(self, event):
        self.edit_win = customerwin.CustomerWin(self)
        self.edit_win.CenterOnScreen()
        val = self.edit_win.ShowModal()
        if val == wx.ID_OK:
            self.edit_win.save()
            wx.MessageBox(u"保存成功！", "提示", style=wx.ICON_INFORMATION)
        self.edit_win.Destroy()
        self.grid.GetTable().data = self.service.search_customer()
        self.grid.reset()

    """
    打开修改页
    """
    def open_modify(self, event):
        rows = self.grid.GetSelectedRows()
        if rows is None or len(rows) == 0:
            wx.MessageBox(u"请选择要修改的数据！", "提示", style=wx.ICON_HAND)
            return False
        selected = rows[0]
        select_data = self.grid.GetTable().data[selected]
        self.edit_win = customerwin.CustomerWin(self)
        self.edit_win.set_data(select_data)
        self.edit_win.CenterOnScreen()
        val = self.edit_win.ShowModal()
        if val == wx.ID_OK:
            self.edit_win.update()
            wx.MessageBox(u"修改成功！", "提示", style=wx.ICON_INFORMATION)
        self.edit_win.Destroy()
        self.grid.GetTable().data = self.service.search_customer()
        self.grid.reset()

    """
    删除
    """
    def on_delete(self, event):
        rows = self.grid.GetSelectedRows()
        if rows is None or len(rows) == 0:
            wx.MessageBox(u"请选择要删除的数据！", "提示", style=wx.ICON_HAND)
            return False

        selected = rows[0]
        select_data = self.grid.GetTable().data[selected]

        dlg = wx.MessageDialog(self, u"是否确定删除数据？", "警告", style=wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)
        val = dlg.ShowModal()
        if val == wx.ID_NO:
            return False
        dlg.Destroy()

        self.service.delete_customer(select_data[5])

        self.grid.GetTable().data = self.service.search_customer()
        self.grid.reset()


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
        self._rows = self.GetNumberRows()
        self._cols = self.GetNumberCols()

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

    """
    视图重置
    """
    def reset_view(self, grid):
        grid.BeginBatch()

        for current, new, del_msg, add_msg in [
            (self._rows, self.GetNumberRows(), gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,
             gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED),
            (self._cols, self.GetNumberCols(), gridlib.GRIDTABLE_NOTIFY_COLS_DELETED,
             gridlib.GRIDTABLE_NOTIFY_COLS_APPENDED),
        ]:
            if new < current:
                msg = gridlib.GridTableMessage(self, del_msg, new, current-new)
                grid.ProcessTableMessage(msg)
            elif new > current:
                msg = gridlib.GridTableMessage(self, add_msg, new-current)
                grid.ProcessTableMessage(msg)
                msg = gridlib.GridTableMessage(self, gridlib.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
                grid.ProcessTableMessage(msg)

        grid.EndBatch()

        self._rows = self.GetNumberRows()
        self._cols = self.GetNumberCols()

        grid.AdjustScrollbars()
        grid.ForceRefresh()


class CustomerGrid(gridlib.Grid):
    """
    客户网格
    """
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1)

        self.selected = None

        self._table = CustomerDataTable()
        self.SetTable(self._table, True)

        self.AutoSize()
        self.CanDragGridSize()
        self.EnableEditing(False)

        self.SetColLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        self.SetDefaultCellAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

        # self.Bind(gridlib.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)

    """
    重置网格
    """
    def reset(self):
        self._table.reset_view(self)

    def OnLabelLeftClick(self, evt):
        self.selected = evt.GetRow()

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
