# coding=utf-8
import wx
import wx.xrc
from crm import service, textvalidator, idnumbervalidator, auth, vehiclepanel, excelutil
import datetime
import time
import threading
from wx.lib.scrolledpanel import ScrolledPanel


# Class CustomerWin
class AlarmWin(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"车辆保险到期提醒", pos=wx.DefaultPosition, size=(800, 530),
                           style=wx.CAPTION | wx.STAY_ON_TOP | wx.RESIZE_BORDER)

        self.alarm_time = None

        border = wx.BoxSizer(wx.VERTICAL)

        # 操作条
        opt_sizer = wx.BoxSizer(wx.HORIZONTAL)

        if not auth.Auth.logon_user[2] == 2:
            export_btn = wx.Button(self, wx.ID_ANY, u"导出")
            self.Bind(wx.EVT_BUTTON, self.on_export, export_btn)
            opt_sizer.Add(export_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        border.Add(opt_sizer, 0, wx.ALIGN_RIGHT, 5)

        # 网格条
        grid_boxer = wx.BoxSizer(wx.HORIZONTAL)
        panel = ScrolledPanel(self, size=(780, 400))
        alarm_grid = vehiclepanel.VehicleGrid(panel)
        # 加载预警数据
        self.data = service.search_vehicle(30, None)
        alarm_grid.set_data(self.data)
        grid_boxer.Add(alarm_grid, 0, wx.ALIGN_TOP, 5)
        panel.SetSizer(grid_boxer)
        panel.Fit()
        panel.SetAutoLayout(1)
        panel.SetupScrolling()
        border.Add(panel, 0, wx.FIXED_MINSIZE, 5)

        # 按钮条
        buttons = wx.BoxSizer()
        self.close_btn = wx.Button(self, wx.ID_OK, u"关闭")
        self.close_btn.SetDefault()
        self.close_btn.Enable(False)
        buttons.Add(self.close_btn)
        border.Add(buttons, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.SetSizer(border)

    def start_delay(self):
        """
        新起线程执行延迟激活按钮
        """
        thread = threading.Thread(target=self.delay_enable_btn, name='alarm_btn_delay')
        # serDeamon(True)后台线程，主线程执行过程中，后台线程也在进行，主线程执行完毕后，后台线程不论成功与否，主线程均停止
        thread.setDaemon(True)
        thread.start()

    def delay_enable_btn(self):
        """
        延迟激活按钮
        """
        time.sleep(20)
        self.close_btn.Enable(True)
        self.close_btn.SetDefault()

    @staticmethod
    def check_alarm():
        """
        判断是否需要提醒
        :return true 需要提醒；false 不需要提醒；
        """
        if auth.Auth.logon_user is None:
            return False
        if not AlarmWin.has_alarm():
            return False
        current_user = auth.Auth.logon_user
        last_login = current_user[4]
        if last_login is None or last_login == '':
            return True
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        return last_login < current_date

    @staticmethod
    def finish_alarm():
        """
        结束预警，保存登陆记录
        """
        auth.Auth.update_last_login(datetime.datetime.now().strftime('%Y-%m-%d'))

    @staticmethod
    def has_alarm():
        """
        判断是否存在提醒数据
        """
        data = service.search_vehicle(30, None)
        return data is not None

    def on_export(self, event):
        """
        导出excel
        """
        file_name = u"车辆保险到期提醒_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        result = excelutil.ExcelUtil.export_vehicle(
            (file_name, u"车辆保险到期提醒", 30, None))
        if result:
            wx.MessageBox(u"导出完成，请到程序根目录下export文件夹中获取导出的文件“" + file_name + ".xls”！",
                          "提示", style=wx.ICON_INFORMATION)
        else:
            wx.MessageBox(u"未找到数据！", "提示", style=wx.ICON_ERROR)

