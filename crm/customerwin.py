# coding=utf-8
import wx
import wx.xrc
from crm import service, textvalidator


# Class CustomerWin
class CustomerWin(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u" 编辑客户", pos=wx.DefaultPosition, size=wx.DefaultSize,
                           style=wx.DEFAULT_DIALOG_STYLE)

        self.data = None

        border = wx.BoxSizer(wx.VERTICAL)

        # 姓名
        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, wx.ID_ANY, u"* 姓名：")
        label.SetForegroundColour(wx.RED)
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        self.customerNameInput = wx.TextCtrl(self, wx.ID_ANY, "", size=wx.Size(200, -1),
                                             validator=textvalidator.TextValidator(u"姓名"))
        box.Add(self.customerNameInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        border.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # 性别
        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, wx.ID_ANY, u"  性别：")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        self.customerGender1 = wx.RadioButton(self, wx.ID_ANY, u"男", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP)
        self.customerGender1.SetValue(True)
        box.Add(self.customerGender1, 1, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)
        self.customerGender2 = wx.RadioButton(self, wx.ID_ANY, u"女", wx.DefaultPosition, wx.DefaultSize, 0)
        box.Add(self.customerGender2, 1, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        border.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # 电话
        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, wx.ID_ANY, u"* 电话：")
        label.SetForegroundColour(wx.Colour(255, 0, 0))
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        self.customerPhoneInput = wx.TextCtrl(self, wx.ID_ANY, "", size=wx.Size(200, -1),
                                              validator=textvalidator.TextValidator(u"电话"))
        box.Add(self.customerPhoneInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        border.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # 地址
        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, wx.ID_ANY, u"  地址：")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        self.customerAddressInput = wx.TextCtrl(self, wx.ID_ANY, "", size=wx.Size(200, -1))
        box.Add(self.customerAddressInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        border.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # 备注
        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, wx.ID_ANY, u"  备注：")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        self.customerRemarkInput = wx.TextCtrl(self, wx.ID_ANY, "", size=wx.Size(200, -1), style=wx.TE_MULTILINE)
        box.Add(self.customerRemarkInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        border.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=wx.DefaultSize, style=wx.HORIZONTAL)
        border.Add(line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP, 5)

        # 按钮
        buttons = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK, u"保存")
        btn.SetDefault()
        buttons.Add(btn)
        btn = wx.Button(self, wx.ID_CANCEL, u"取消")
        buttons.Add(btn)
        buttons.Realize()
        border.Add(buttons, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.SetSizer(border)
        border.Fit(self)

    """
    表单赋值
    """
    def set_data(self, data):
        self.data = data
        self.customerNameInput.SetValue(self.data[0])
        if self.data[1] == '男':
            self.customerGender1.SetValue(True)
        else:
            self.customerGender2.SetValue(True)
        self.customerPhoneInput.SetValue(self.data[2])
        self.customerAddressInput.SetValue(self.data[3])
        self.customerRemarkInput.SetValue(self.data[4])

    """
    表单取值
    """
    def get_form_values(self, transfer):
        if transfer:
            gender = '女'
            if self.customerGender1.GetValue():
                gender = '男'
        else:
            gender = 2
            if self.customerGender1.GetValue():
                gender = 1
        return (
            self.customerNameInput.GetValue().strip(),
            gender,
            self.customerPhoneInput.GetValue().strip(),
            self.customerAddressInput.GetValue().strip(),
            self.customerRemarkInput.GetValue().strip()
        )

    """
    取值
    """
    def get_data(self):
        customer = self.get_form_values(True)
        return customer + (self.data[5],)

    """
    保存
    """
    def save(self):
        customer = self.get_form_values(False)
        return service.save_customer(customer)

    """
    更新
    """
    def update(self):
        customer = self.get_form_values(False)
        return service.update_customer(self.data[5], customer)
