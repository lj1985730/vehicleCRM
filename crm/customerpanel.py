# coding=utf-8
import wx
import wx.grid as gridlib
from crm import service, customerwin, idnumbervalidator


class CustomerPanel(wx.Panel):
    """
    客户面板
    """
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.grid = None
        self.edit_win = None
        self.id_number_search = None
        self.init_layout()

    def init_layout(self):
        """
        展现渲染
        """
        sizer = wx.BoxSizer(wx.VERTICAL)
        opt_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.id_number_search = wx.TextCtrl(self, wx.ID_ANY, "搜索身份证号...", size=wx.Size(200, -1),
                                            validator=idnumbervalidator.IdNumberValidator(None))
        opt_sizer.Add(self.id_number_search, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.id_number_search.Bind(wx.EVT_KEY_UP, self.on_search, self.id_number_search)

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

    def on_search(self, event):
        """
        搜索
        """
        self.grid.GetTable().data = service.search_customer(None, self.id_number_search.GetValue())
        self.grid.reset()

    def open_create(self, event):
        """
        打开新增页
        """
        self.edit_win = customerwin.CustomerWin(self)
        self.edit_win.CenterOnScreen()
        val = self.edit_win.ShowModal()
        if val == wx.ID_OK:
            try:
                self.edit_win.save()
            except ValueError as e:
                wx.MessageBox(str(e), "提示", style=wx.ICON_HAND)
            else:
                wx.MessageBox(u"保存成功！", "提示", style=wx.ICON_INFORMATION)
        self.edit_win.Destroy()
        self.grid.GetTable().data = service.search_customer(None, self.id_number_search.GetValue())
        self.grid.reset()

    def open_modify(self, event):
        """
        打开修改页
        """
        rows = self.grid.GetSelectedRows()
        if rows is None or len(rows) == 0:
            wx.MessageBox(u"请选择要修改的数据！", "提示", style=wx.ICON_HAND)
            return
        selected = rows[0]
        select_data = self.grid.GetTable().data[selected]
        self.edit_win = customerwin.CustomerWin(self)
        self.edit_win.set_data(select_data)
        self.edit_win.CenterOnScreen()
        val = self.edit_win.ShowModal()
        if val == wx.ID_OK:
            try:
                self.edit_win.update()
            except ValueError as e:
                wx.MessageBox(str(e), "提示", style=wx.ICON_HAND)
            else:
                wx.MessageBox(u"修改成功！", "提示", style=wx.ICON_INFORMATION)
        self.edit_win.Destroy()
        self.grid.GetTable().data = service.search_customer(None, self.id_number_search.GetValue())
        self.grid.reset()

    def on_delete(self, event):
        """
        删除
        """
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

        service.delete_customer(select_data[6])

        self.grid.GetTable().data = service.search_customer(None, self.id_number_search.GetValue())
        self.grid.reset()


class CustomerDataTable(gridlib.GridTableBase):
    """
    客户网格数据
    """
    def __init__(self):
        gridlib.GridTableBase.__init__(self)
        self.colLabels = ['姓名', '性别', '身份证号', '电话', '住址', '备注']
        self.dataTypes = [
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING
        ]
        self.data = service.search_customer(None, None)
        self._rows = self.GetNumberRows()
        self._cols = self.GetNumberCols()

    # required methods for the wxPyGridTableBase interface
    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return 6

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

    def reset_view(self, grid):
        """
        视图重置
        """
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

    def reset(self):
        """
        重置网格
        """
        self._table.reset_view(self)
