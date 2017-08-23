# coding=utf-8
import wx
from crm import mainframe

if __name__ == '__main__':
    app = wx.App()
    window = mainframe.MainFrame(None, title="登陆", size=(800, 600))
    # panel = wx.Panel(window)
    window.Show()
    app.MainLoop()
