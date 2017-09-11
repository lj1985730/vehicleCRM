# coding=utf-8
import wx
import wx.grid as gridlib
from crm import service, vehiclewin, excelutil
import datetime


class VehiclePanel(wx.Panel):
    """
    车辆面板
    """

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.alarm_checker = None
        self.grid = None
        self.edit_win = None
        self.init_layout()

    """
    展现渲染
    """
    def init_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        opt_sizer = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, wx.ID_ANY, u"预警时间：", size=(95, -1), style=wx.ALIGN_RIGHT)
        opt_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.alarm_checker = \
            wx.ComboBox(self, wx.ID_ANY, size=wx.Size(80, -1), choices=[], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.alarm_checker.Append(u"全部", 10000)
        self.alarm_checker.Append(u"30天内", 30)
        self.alarm_checker.Append(u"60天内", 60)
        self.alarm_checker.Append(u"90天内", 90)
        self.alarm_checker.SetValue(u"全部")
        self.Bind(wx.EVT_COMBOBOX, self.on_select_alarm, self.alarm_checker)
        opt_sizer.Add(self.alarm_checker, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        export_btn = wx.Button(self, wx.ID_ANY, u"导出")
        self.Bind(wx.EVT_BUTTON, self.on_export, export_btn)
        opt_sizer.Add(export_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

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

        self.grid = VehicleGrid(self)
        sizer.Add(self.grid, 1, wx.ALL | wx.EXPAND, 0)

        self.SetSizer(sizer)

    """
    过滤预警数据
    """
    def on_select_alarm(self, event):
        self.grid.GetTable().data =\
            service.search_vehicle(self.alarm_checker.GetClientData(self.alarm_checker.GetSelection()))
        self.grid.reset()
        self.grid.add_warn()

    """
    打开新增页
    """
    def open_create(self, event):
        self.edit_win = vehiclewin.VehicleWin(self)
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
        self.grid.GetTable().data =\
            service.search_vehicle(self.alarm_checker.GetClientData(self.alarm_checker.GetSelection()))
        self.grid.reset()
        self.grid.add_warn()

    """
    打开修改页
    """
    def open_modify(self, event):
        rows = self.grid.GetSelectedRows()
        if rows is None or len(rows) == 0:
            wx.MessageBox(u"请选择要修改的数据！", "提示", style=wx.ICON_HAND)
            return
        selected = rows[0]
        select_data = self.grid.GetTable().data[selected]
        self.edit_win = vehiclewin.VehicleWin(self)
        self.edit_win.set_data(select_data)
        self.edit_win.auth_control()    # 权限控制
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
        self.grid.GetTable().data =\
            service.search_vehicle(self.alarm_checker.GetClientData(self.alarm_checker.GetSelection()))
        self.grid.reset()
        self.grid.add_warn()

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

        dlg = wx.MessageDialog(self, u"是否确定删除数据？", "警告", style=wx.YES | wx.NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)
        val = dlg.ShowModal()
        if val == wx.ID_NO:
            return False
        dlg.Destroy()

        service.delete_vehicle(select_data[22])

        self.grid.GetTable().data =\
            service.search_vehicle(self.alarm_checker.GetClientData(self.alarm_checker.GetSelection()))
        self.grid.reset()
        self.grid.add_warn()

    """
    导出excel
    """
    def on_export(self, event):
        file_name = u"车辆信息_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        result = excelutil.ExcelUtil.export_vehicle(
            (file_name, u"车辆信息", self.alarm_checker.GetClientData(self.alarm_checker.GetSelection())))
        if result:
            wx.MessageBox(u"导出完成，请到程序根目录下export文件夹中获取导出的文件“" + file_name + ".xls”！",
                          "提示", style=wx.ICON_INFORMATION)
        else:
            wx.MessageBox(u"未找到数据！", "提示", style=wx.ICON_ERROR)


class VehicleDataTable(gridlib.GridTableBase):
    """
    车辆网格数据
    """
    def __init__(self):
        gridlib.GridTableBase.__init__(self)
        self.colLabels = ['客户姓名', '客户性别', '客户电话',
                          '车牌号', '车辆型号', '车辆登记日期', '公里数', '过户次数',
                          '贷款产品', '贷款期次', '贷款年限', '贷款金额', '贷款提报日期', '贷款通过日期', '放款日期',
                          '承保公司', '险种', '保险生效日期', '保险到期日期',
                          '备注', '修改人', '修改时间']
        self.dataTypes = [
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,

            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_DATETIME,
            gridlib.GRID_VALUE_NUMBER,
            gridlib.GRID_VALUE_NUMBER,

            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_NUMBER,
            gridlib.GRID_VALUE_NUMBER,
            gridlib.GRID_VALUE_DATETIME,
            gridlib.GRID_VALUE_DATETIME,
            gridlib.GRID_VALUE_DATETIME,

            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_DATETIME,
            gridlib.GRID_VALUE_DATETIME,

            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING,
            gridlib.GRID_VALUE_STRING
        ]
        self.data = service.search_vehicle(10000, None)

        self._rows = self.GetNumberRows()
        self._cols = self.GetNumberCols()

    # required methods for the wxPyGridTableBase interface
    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return 22

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


class VehicleGrid(gridlib.Grid):
    """
    车辆网格
    """
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1)

        self.selected = None

        self._table = VehicleDataTable()
        self.SetTable(self._table, True)

        self.AutoSize()
        self.CanDragGridSize()
        self.EnableEditing(False)

        self.SetColLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        self.SetDefaultCellAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

        self.add_warn()

    """
    增加预警
    """
    def add_warn(self):
        # alarm threshold day
        today = datetime.date.today()
        threshold_day_30 = today + datetime.timedelta(days=30)
        threshold_day_60 = today + datetime.timedelta(days=60)
        threshold_day_90 = today + datetime.timedelta(days=90)

        # add alarm row style
        table_data = self._table.data
        for index in range(len(table_data)):
            self.set_row_normal(index)
            if table_data[index][18] <= threshold_day_90.strftime('%Y-%m-%d'):
                self.set_row_yellow(index)
            if table_data[index][18] <= threshold_day_60.strftime('%Y-%m-%d'):
                self.set_row_orange(index)
            if table_data[index][18] <= threshold_day_30.strftime('%Y-%m-%d'):
                self.set_row_red(index)

    """
    重置网格
    """
    def reset(self):
        self._table.reset_view(self)

    def set_row_red(self, row_number):
        attr = gridlib.GridCellAttr()
        attr.SetTextColour(wx.BLACK)
        attr.SetBackgroundColour(wx.RED)
        # attr.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.SetRowAttr(row_number, attr)

    def set_row_orange(self, row_number):
        attr = gridlib.GridCellAttr()
        attr.SetTextColour(wx.BLACK)
        attr.SetBackgroundColour((250, 128, 10))
        # attr.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.SetRowAttr(row_number, attr)

    def set_row_yellow(self, row_number):
        attr = gridlib.GridCellAttr()
        attr.SetTextColour(wx.BLACK)
        attr.SetBackgroundColour(wx.YELLOW)
        # attr.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.SetRowAttr(row_number, attr)

    def set_row_normal(self, row_number):
        attr = gridlib.GridCellAttr()
        attr.SetTextColour(wx.BLACK)
        self.SetRowAttr(row_number, attr)
