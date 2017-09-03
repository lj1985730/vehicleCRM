# -*- coding: utf-8 -*-
import wx
import wx.xrc

from crm import auth


class LoginWin(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"登陆窗体", pos=wx.DefaultPosition, size=wx.DefaultSize,
                           style=wx.CLOSE_BOX | wx.DEFAULT_DIALOG_STYLE)

        sizer = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(self, -1, u"请输入账户密码")
        sizer.Add(title, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        login_name_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.loginNameLabel = wx.StaticText(self, wx.ID_ANY, u"账户：")
        login_name_sizer.Add(self.loginNameLabel, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.loginNameInput = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, size=(80, -1))
        self.loginNameInput.SetMaxLength(20)
        login_name_sizer.Add(self.loginNameInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(login_name_sizer, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        login_pass_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.loginPassLabel = wx.StaticText(self, wx.ID_ANY, u"密码：")
        login_pass_sizer.Add(self.loginPassLabel, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.loginPassInput = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, size=(80, -1), style=wx.TE_PASSWORD)
        self.loginPassInput.SetMaxLength(20)
        login_pass_sizer.Add(self.loginPassInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(login_pass_sizer, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP, 5)

        login_button_sizer = wx.StdDialogButtonSizer()

        self.loginOK = wx.Button(self, wx.ID_OK)
        login_button_sizer.Add(self.loginOK)

        self.loginCancel = wx.Button(self, wx.ID_CANCEL)
        login_button_sizer.Add(self.loginCancel)
        login_button_sizer.Realize()

        sizer.Add(login_button_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def do_login(self):
        login_result = auth.Auth.login(self.loginNameInput.GetValue(), self.loginPassInput.GetValue())
        if not login_result:
            wx.MessageBox(u"用户名或密码错误！", u"错误", style=wx.ICON_ERROR)
