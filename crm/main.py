# coding=utf-8
import wx
from crm import mainframe

if __name__ == '__main__':
    app = wx.App()
    window = mainframe.MainFrame(None, title=u"车辆客户管理系统", size=(800, 600))
    window.Show()
    app.MainLoop()
