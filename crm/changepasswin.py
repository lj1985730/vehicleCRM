# -*- coding: utf-8 -*-
import wx
import wx.xrc

from crm import auth, textvalidator, service


class ChangePassWin(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"修改密码", pos=wx.DefaultPosition, size=wx.DefaultSize,
                           style=wx.CLOSE_BOX | wx.DEFAULT_DIALOG_STYLE)

        sizer = wx.BoxSizer(wx.VERTICAL)

        old_pass_sizer = wx.BoxSizer(wx.HORIZONTAL)
        old_pass_label = wx.StaticText(self, wx.ID_ANY, u"* 旧密码：", size=(80, -1), style=wx.ALIGN_RIGHT)
        old_pass_sizer.Add(old_pass_label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.oldPassInput = \
            wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, size=(120, -1), style=wx.TE_PASSWORD,
                        validator=textvalidator.TextValidator(u"旧密码"))
        self.oldPassInput.SetMaxLength(20)
        old_pass_sizer.Add(self.oldPassInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(old_pass_sizer, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        new_pass_sizer = wx.BoxSizer(wx.HORIZONTAL)
        new_pass_label = wx.StaticText(self, wx.ID_ANY, u"* 新密码：", size=(80, -1), style=wx.ALIGN_RIGHT)
        new_pass_sizer.Add(new_pass_label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.newPassInput =\
            wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, size=(120, -1), style=wx.TE_PASSWORD,
                        validator=textvalidator.TextValidator(u"新密码"))
        self.newPassInput.SetMaxLength(20)
        new_pass_sizer.Add(self.newPassInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(new_pass_sizer, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        confirm_pass_sizer = wx.BoxSizer(wx.HORIZONTAL)
        confirm_pass_label = wx.StaticText(self, wx.ID_ANY, u"* 确认新密码：", size=(80, -1), style=wx.ALIGN_RIGHT)
        confirm_pass_sizer.Add(confirm_pass_label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.confirmPassInput =\
            wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, size=(120, -1), style=wx.TE_PASSWORD,
                        validator=textvalidator.TextValidator(u"确认新密码"))
        self.confirmPassInput.SetMaxLength(20)
        confirm_pass_sizer.Add(self.confirmPassInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(confirm_pass_sizer, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP, 5)

        change_pass_button_sizer = wx.StdDialogButtonSizer()

        self.changeOK = wx.Button(self, wx.ID_OK)
        change_pass_button_sizer.Add(self.changeOK)
        self.changeOK.SetDefault()

        self.changeCancel = wx.Button(self, wx.ID_CANCEL)
        change_pass_button_sizer.Add(self.changeCancel)
        change_pass_button_sizer.Realize()

        sizer.Add(change_pass_button_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def change_pass(self):

        new_pass = self.newPassInput.GetValue()
        confirm_pass = self.confirmPassInput.GetValue()

        if not new_pass == confirm_pass:
            raise ValueError("新密码与确认密码不一致！")

        auth.Auth.change_pass(self.oldPassInput.GetValue(), self.newPassInput.GetValue())
