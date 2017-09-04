# coding=utf-8
import wx
from crm import mainframe, auth

if __name__ == '__main__':
    app = wx.App()
    window = mainframe.MainFrame(None, title=u"车辆客户管理系统", size=(1000, 800))
    window.Show()

    if auth.Auth.logon_user is None:
        window.on_login(window)

    app.MainLoop()
