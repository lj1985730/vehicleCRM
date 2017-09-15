# coding=utf-8
import wx
import wx.xrc
from crm import service, textvalidator, idnumbervalidator, auth, vehiclepanel
import datetime
import time
import sched


# Class CustomerWin
class AlarmWin(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"车辆保险到期提醒", pos=wx.DefaultPosition, size=wx.DefaultSize,
                           style=wx.DEFAULT_DIALOG_STYLE)

        self.alarm_time = None

        # 加载预警数据
        self.data = service.search_vehicle(30, None)

        border = wx.BoxSizer(wx.VERTICAL)

        alarm_panel = wx.Panel(self)
        alarm_grid = vehiclepanel.VehicleGrid(alarm_panel)

        # 按钮
        buttons = wx.StdDialogButtonSizer()
        self.close_btn = wx.Button(self, wx.ID_OK, u"关闭")
        self.close_btn.SetDefault()
        self.close_btn.Enable(False)
        buttons.Add(self.close_btn)
        border.Add(buttons, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.SetSizer(border)
        border.Fit(self)

    def start(self):
        schedule = sched.scheduler()
        schedule.enter(5, 0, self.enable_btn,)
        schedule.run()

    def enable_btn(self):
        self.close_btn.Enable(True)

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
