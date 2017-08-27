# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Aug  4 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class customerWin
###########################################################################

class customerWin(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u" 编辑客户", pos=wx.DefaultPosition, size=wx.Size(541, 455),
                           style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.Size(450, -1), wx.DefaultSize)

        customerSizer = wx.GridSizer(4, 2, 0, 0)

        self.customerNameLabel = wx.StaticText(self, wx.ID_ANY, u"* 姓名：", wx.DefaultPosition, wx.Size(100, -1), 0)
        self.customerNameLabel.Wrap(-1)
        self.customerNameLabel.SetForegroundColour(wx.Colour(255, 0, 0))

        customerSizer.Add(self.customerNameLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 5)

        self.customerNameInput = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(200, -1), 0)
        self.customerNameInput.SetMinSize(wx.Size(200, -1))

        customerSizer.Add(self.customerNameInput, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.customerGenderLabel = wx.StaticText(self, wx.ID_ANY, u"性别：", wx.DefaultPosition, wx.Size(100, -1), 0)
        self.customerGenderLabel.Wrap(-1)
        customerSizer.Add(self.customerGenderLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 5)

        customerGenderSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.customerGender1 = wx.RadioButton(self, wx.ID_ANY, u"男", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP)
        self.customerGender1.SetValue(True)
        customerGenderSizer.Add(self.customerGender1, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        self.customerGender2 = wx.RadioButton(self, wx.ID_ANY, u"女", wx.DefaultPosition, wx.DefaultSize, 0)
        customerGenderSizer.Add(self.customerGender2, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        customerSizer.Add(customerGenderSizer, 1, wx.ALIGN_CENTER | wx.EXPAND, 5)

        self.customerPhoneLabel = wx.StaticText(self, wx.ID_ANY, u"* 电话：", wx.DefaultPosition, wx.Size(100, -1), 0)
        self.customerPhoneLabel.Wrap(-1)
        self.customerPhoneLabel.SetForegroundColour(wx.Colour(255, 0, 0))

        customerSizer.Add(self.customerPhoneLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 5)

        self.customerPhoneInput = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(200, -1), 0)
        self.customerPhoneInput.SetMinSize(wx.Size(200, -1))

        customerSizer.Add(self.customerPhoneInput, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.customerAddressLabel = wx.StaticText(self, wx.ID_ANY, u"地址：", wx.DefaultPosition, wx.Size(100, -1), 0)
        self.customerAddressLabel.Wrap(-1)
        customerSizer.Add(self.customerAddressLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 5)

        self.customerAddressInput = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(200, -1),
                                                0)
        self.customerAddressInput.SetMinSize(wx.Size(200, -1))

        customerSizer.Add(self.customerAddressInput, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.customerOK = wx.Button(self, wx.ID_ANY, u"保存", wx.DefaultPosition, wx.DefaultSize, 0)
        self.customerOK.SetDefault()
        customerSizer.Add(self.customerOK, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.customerCancel = wx.Button(self, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0)
        customerSizer.Add(self.customerCancel, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SetSizer(customerSizer)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass
