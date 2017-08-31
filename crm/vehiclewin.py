# coding=utf-8
import wx
import wx.adv
import wx.xrc
from crm import service, textvalidator
from wx.lib import intctrl


# Class VehicleWin
class VehicleWin(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u" 编辑车辆信息", pos=wx.DefaultPosition, size=wx.DefaultSize,
                           style=wx.DEFAULT_DIALOG_STYLE)

        self.data = None

        border = wx.BoxSizer(wx.VERTICAL)

        # load customer combo data
        customer_data = service.CrmService.search_customer()
        combo_data = []
        for name, gender, phone, address, remark, customer_id in customer_data:
            combo_data.append((customer_id, name))

        # 客户姓名
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, wx.ID_ANY, u"* 客户姓名：")
        label.SetForegroundColour(wx.RED)
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.customerCombobox =\
            wx.ComboBox(self, wx.ID_ANY, "", size=wx.Size(200, -1), choices=combo_data, style=wx.CB_DROPDOWN)
        box.Add(self.customerCombobox, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        border.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # 车辆型号
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, wx.ID_ANY, u"*车辆型号：")
        label.SetForegroundColour(wx.RED)
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.vehicleModelInput =\
            wx.TextCtrl(self, wx.ID_ANY, "", size=wx.Size(200, -1), validator=textvalidator.TextValidator())
        box.Add(self.vehicleModelInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        border.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # 车辆登记日期
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, wx.ID_ANY, u"*车辆登记日期：")
        label.SetForegroundColour(wx.RED)
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.vehicleRegDate =\
            wx.adv.DatePickerCtrl(self, wx.ID_ANY, size=wx.Size(200, -1),
                                  style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY,
                                  validator=textvalidator.TextValidator())
        box.Add(self.vehicleRegDate, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        border.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # 里程数
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, wx.ID_ANY, u"  里程数：")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.mileageInput =\
            intctrl.IntCtrl(self, wx.ID_ANY, size=wx.Size(200, -1), validator=textvalidator.TextValidator())
        box.Add(self.mileageInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        border.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # 过户次数
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, wx.ID_ANY, u"*过户次数：")
        label.SetForegroundColour(wx.RED)
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.transCountInput =\
            intctrl.IntCtrl(self, wx.ID_ANY, 1, size=wx.Size(200, -1), validator=textvalidator.TextValidator())
        box.Add(self.transCountInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        border.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # 贷款产品、期次
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, wx.ID_ANY, u"*贷款产品：")
        label.SetForegroundColour(wx.RED)
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.loanProductInput =\
            wx.TextCtrl(self, wx.ID_ANY, "", size=wx.Size(200, -1), validator=textvalidator.TextValidator())
        box.Add(self.loanProductInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        label = wx.StaticText(self, wx.ID_ANY, u"*期次：")
        label.SetForegroundColour(wx.RED)
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.loanPeriodInput =\
            wx.TextCtrl(self, wx.ID_ANY, "", size=wx.Size(200, -1), validator=textvalidator.TextValidator())
        box.Add(self.loanPeriodInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        border.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # 贷款年限
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, wx.ID_ANY, u"*贷款年限：")
        label.SetForegroundColour(wx.RED)
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.loanTermInput =\
            intctrl.IntCtrl(self, wx.ID_ANY, 1, size=wx.Size(200, -1), validator=textvalidator.TextValidator())
        box.Add(self.loanTermInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        border.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # 贷款金额
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, wx.ID_ANY, u"贷款金额：")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.loanValueInput =\
            intctrl.IntCtrl(self, wx.ID_ANY, 1, size=wx.Size(200, -1))
        box.Add(self.loanValueInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        border.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # 贷款提报日期
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, wx.ID_ANY, u"贷款提报日期：")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.loanReportDate = \
            wx.adv.DatePickerCtrl(self, wx.ID_ANY, size=wx.Size(200, -1),
                                  style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY | wx.adv.DP_ALLOWNONE)
        box.Add(self.loanReportDate, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        border.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # 贷款通过日期
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, wx.ID_ANY, u"贷款通过日期：")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.loanPassedDate = \
            wx.adv.DatePickerCtrl(self, wx.ID_ANY, size=wx.Size(200, -1),
                                  style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY | wx.adv.DP_ALLOWNONE)
        box.Add(self.loanPassedDate, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        border.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # 放款日期
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, wx.ID_ANY, u"* 放款日期：")
        label.SetForegroundColour(wx.RED)
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.loanDate = \
            wx.adv.DatePickerCtrl(self, wx.ID_ANY, size=wx.Size(200, -1),
                                  style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY,
                                  validator=textvalidator.TextValidator())
        box.Add(self.loanDate, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        border.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # 承保公司
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, wx.ID_ANY, u"承保公司：")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.insuranceCompanyInput =\
            wx.TextCtrl(self, wx.ID_ANY, "", size=wx.Size(200, -1))
        box.Add(self.insuranceCompanyInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        border.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # 险种
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, wx.ID_ANY, u"险种：")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.insuranceTypeInput =\
            wx.TextCtrl(self, wx.ID_ANY, "", size=wx.Size(200, -1))
        box.Add(self.insuranceTypeInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        border.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # 保险生效日期
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, wx.ID_ANY, u"*保险生效日期：")
        label.SetForegroundColour(wx.RED)
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.insuranceStartDate = \
            wx.adv.DatePickerCtrl(self, wx.ID_ANY, size=wx.Size(200, -1),
                                  style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY,
                                  validator=textvalidator.TextValidator())
        box.Add(self.insuranceStartDate, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        border.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # 保险到期日期
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, wx.ID_ANY, u"*保险到期日期：")
        label.SetForegroundColour(wx.RED)
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.insuranceEndDate = \
            wx.adv.DatePickerCtrl(self, wx.ID_ANY, size=wx.Size(200, -1),
                                  style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY,
                                  validator=textvalidator.TextValidator())
        box.Add(self.insuranceEndDate, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        border.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # 备注
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, wx.ID_ANY, u"  备注：")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.remarkInput =\
            wx.TextCtrl(self, wx.ID_ANY, "", size=wx.Size(200, -1), style=wx.TE_MULTILINE)
        box.Add(self.remarkInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
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
        vehicle = self.get_form_values(True)
        return vehicle + (self.data[19],)

    """
    保存
    """

    def save(self):
        customer = self.get_form_values(False)
        service.CrmService.save_customer(customer)

    """
    更新
    """

    def update(self):
        customer = self.get_form_values(False)
        service.CrmService.update_customer(self.data[5], customer)
