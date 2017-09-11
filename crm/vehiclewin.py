# coding=utf-8
import wx
import datetime
import wx.adv
import wx.xrc
from wx.lib import intctrl

from crm import service, textvalidator, platenumvalidator, auth


# Class VehicleWin
class VehicleWin(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"编辑车辆信息", pos=wx.DefaultPosition, size=wx.DefaultSize,
                           style=wx.DEFAULT_DIALOG_STYLE)

        self.data = None

        border = wx.BoxSizer(wx.VERTICAL)

        # load customer combo data
        self.customer_data = service.search_customer(None, None)

        # load insurance company combo data
        self.company_data = service.search_dict(1)

        # load authorization
        self.current_user = auth.Auth.logon_user

        # new box -------------------------------------------------------------------------
        box = wx.StaticBox(self, -1, u"客户信息")
        box.SetForegroundColour((119, 136, 153))
        box_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        border.Add(box_sizer, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # new line ########################################################################
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        box_sizer.Add(sizer)

        # 客户姓名
        label = wx.StaticText(self, wx.ID_ANY, u"* 姓名：", size=(60, -1), style=wx.ALIGN_RIGHT)
        label.SetForegroundColour(wx.RED)
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.customerCombobox =\
            wx.ComboBox(self, wx.ID_ANY, size=wx.Size(140, -1), choices=[], style=wx.CB_DROPDOWN)

        for customer in self.customer_data:
            self.customerCombobox.Append(customer[0], customer[5])

        sizer.Add(self.customerCombobox, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.Bind(wx.EVT_COMBOBOX, self.select_customer, self.customerCombobox)
        self.Bind(wx.EVT_TEXT, self.filter_customer, self.customerCombobox)
        self.Bind(wx.EVT_CHAR, self.enable_filter, self.customerCombobox)
        self.ignoreEvtText = False

        # 客户性别
        label = wx.StaticText(self, wx.ID_ANY, u"性别：", size=(60, -1), style=wx.ALIGN_RIGHT)
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.customerGenderPanel =\
            wx.StaticText(self, wx.ID_ANY, size=wx.Size(140, -1))
        sizer.Add(self.customerGenderPanel, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        # 客户电话
        label = wx.StaticText(self, wx.ID_ANY, u"电话：", size=(60, -1), style=wx.ALIGN_RIGHT)
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.customerPhonePanel =\
            wx.StaticText(self, wx.ID_ANY, size=wx.Size(140, -1))
        sizer.Add(self.customerPhonePanel, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        # new box -------------------------------------------------------------------------
        box = wx.StaticBox(self, -1, u"车辆信息")
        box.SetForegroundColour((119, 136, 153))
        box_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        border.Add(box_sizer, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # new line ########################################################################
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        box_sizer.Add(sizer)

        # 车牌号
        label = wx.StaticText(self, wx.ID_ANY, u"* 车牌号：", size=(95, -1), style=wx.ALIGN_RIGHT)
        label.SetForegroundColour(wx.RED)
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.vehiclePlateNumInput =\
            wx.TextCtrl(self, wx.ID_ANY, "", size=wx.Size(200, -1), validator=platenumvalidator.PlateNumValidator(None))
        sizer.Add(self.vehiclePlateNumInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        # 车辆型号
        label = wx.StaticText(self, wx.ID_ANY, u"* 车辆型号：", size=(95, -1), style=wx.ALIGN_RIGHT)
        label.SetForegroundColour(wx.RED)
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.vehicleModelInput =\
            wx.TextCtrl(self, wx.ID_ANY, "", size=wx.Size(200, -1), validator=textvalidator.TextValidator(u"车辆型号"))
        sizer.Add(self.vehicleModelInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        # new line ########################################################################
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        box_sizer.Add(sizer)

        # 车辆登记日期
        label = wx.StaticText(self, wx.ID_ANY, u"* 车辆登记日期：", size=(95, -1), style=wx.ALIGN_RIGHT)
        label.SetForegroundColour(wx.RED)
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.vehicleRegDate =\
            wx.adv.DatePickerCtrl(self, wx.ID_ANY, size=wx.Size(200, -1),
                                  style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        sizer.Add(self.vehicleRegDate, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        # 公里数
        label = wx.StaticText(self, wx.ID_ANY, u"公里数：", size=(95, -1), style=wx.ALIGN_RIGHT)
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.mileageInput =\
            intctrl.IntCtrl(self, wx.ID_ANY, size=wx.Size(200, -1))
        sizer.Add(self.mileageInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        # new line ########################################################################
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        box_sizer.Add(sizer)

        # 过户次数
        label = wx.StaticText(self, wx.ID_ANY, u"* 过户次数：", size=(95, -1), style=wx.ALIGN_RIGHT)
        label.SetForegroundColour(wx.RED)
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.transCountInput =\
            intctrl.IntCtrl(self, wx.ID_ANY, 1, size=wx.Size(200, -1), min=0)
        sizer.Add(self.transCountInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        # new box -------------------------------------------------------------------------
        box = wx.StaticBox(self, -1, u"贷款信息")
        box.SetForegroundColour((119, 136, 153))
        box_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        border.Add(box_sizer, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # new line ########################################################################
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        box_sizer.Add(sizer)

        # 贷款产品、期次
        label = wx.StaticText(self, wx.ID_ANY, u"* 贷款产品：", size=(95, -1), style=wx.ALIGN_RIGHT)
        label.SetForegroundColour(wx.RED)
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.loanProductInput =\
            wx.TextCtrl(self, wx.ID_ANY, "", size=wx.Size(200, -1), validator=textvalidator.TextValidator(u"贷款产品"))
        sizer.Add(self.loanProductInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        label = wx.StaticText(self, wx.ID_ANY, u"* 期次：", size=(95, -1), style=wx.ALIGN_RIGHT)
        label.SetForegroundColour(wx.RED)
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.loanPeriodInput =\
            wx.TextCtrl(self, wx.ID_ANY, "", size=wx.Size(200, -1), validator=textvalidator.TextValidator(u"期次"))
        sizer.Add(self.loanPeriodInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        # new line ########################################################################
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        box_sizer.Add(sizer)

        # 贷款年限
        label = wx.StaticText(self, wx.ID_ANY, u"* 贷款年限：", size=(95, -1), style=wx.ALIGN_RIGHT)
        label.SetForegroundColour(wx.RED)
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.loanTermInput =\
            intctrl.IntCtrl(self, wx.ID_ANY, 1, size=wx.Size(200, -1), min=1)
        sizer.Add(self.loanTermInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        # 贷款金额
        label = wx.StaticText(self, wx.ID_ANY, u"贷款金额：", size=(95, -1), style=wx.ALIGN_RIGHT)
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.loanValueInput =\
            intctrl.IntCtrl(self, wx.ID_ANY, 1, size=wx.Size(200, -1))
        sizer.Add(self.loanValueInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        # new line ########################################################################
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        box_sizer.Add(sizer)

        # 贷款提报日期
        label = wx.StaticText(self, wx.ID_ANY, u"贷款提报日期：", size=(95, -1), style=wx.ALIGN_RIGHT)
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.loanReportDate = \
            wx.adv.DatePickerCtrl(self, wx.ID_ANY, size=wx.Size(200, -1),
                                  style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY | wx.adv.DP_ALLOWNONE)
        sizer.Add(self.loanReportDate, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        # 贷款通过日期
        label = wx.StaticText(self, wx.ID_ANY, u"贷款通过日期：", size=(95, -1), style=wx.ALIGN_RIGHT)
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.loanPassedDate = \
            wx.adv.DatePickerCtrl(self, wx.ID_ANY, size=wx.Size(200, -1),
                                  style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY | wx.adv.DP_ALLOWNONE)
        sizer.Add(self.loanPassedDate, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        # new line ########################################################################
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        box_sizer.Add(sizer)

        # 放款日期
        label = wx.StaticText(self, wx.ID_ANY, u"* 放款日期：", size=(95, -1), style=wx.ALIGN_RIGHT)
        label.SetForegroundColour(wx.RED)
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.loanDate = \
            wx.adv.DatePickerCtrl(self, wx.ID_ANY, size=wx.Size(200, -1),
                                  style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        sizer.Add(self.loanDate, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        # new box -------------------------------------------------------------------------
        box = wx.StaticBox(self, -1, u"投保信息")
        box.SetForegroundColour((119, 136, 153))
        box_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        border.Add(box_sizer, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # new line ########################################################################
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        box_sizer.Add(sizer)

        # 承保公司
        label = wx.StaticText(self, wx.ID_ANY, u"承保公司：", size=(95, -1), style=wx.ALIGN_RIGHT)
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.insuranceCompanyCombobox = \
            wx.ComboBox(self, wx.ID_ANY, size=wx.Size(495, -1), choices=[], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        sizer.Add(self.insuranceCompanyCombobox, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        for company in self.company_data:
            self.insuranceCompanyCombobox.Append(company[1], company[0])

        # self.Bind(wx.EVT_COMBOBOX, self.select_company, self.insuranceCompanyCombobox)

        # new line ########################################################################
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        box_sizer.Add(sizer)

        # 险种
        label = wx.StaticText(self, wx.ID_ANY, u"险种：", size=(95, -1), style=wx.ALIGN_RIGHT)
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.insuranceTypeInput =\
            wx.TextCtrl(self, wx.ID_ANY, "", size=wx.Size(495, -1))
        sizer.Add(self.insuranceTypeInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        # new line ########################################################################
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        box_sizer.Add(sizer)

        # 保险生效日期
        label = wx.StaticText(self, wx.ID_ANY, u"* 保险生效日期：", size=(95, -1), style=wx.ALIGN_RIGHT)
        label.SetForegroundColour(wx.RED)
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.insuranceStartDate = \
            wx.adv.DatePickerCtrl(self, wx.ID_ANY, size=wx.Size(200, -1),
                                  style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        sizer.Add(self.insuranceStartDate, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.get_end, self.insuranceStartDate)

        # 保险到期日期
        label = wx.StaticText(self, wx.ID_ANY, u"* 保险到期日期：", size=(95, -1), style=wx.ALIGN_RIGHT)
        label.SetForegroundColour(wx.RED)
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.insuranceEndDate = \
            wx.adv.DatePickerCtrl(self, wx.ID_ANY, size=wx.Size(200, -1),
                                  style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        sizer.Add(self.insuranceEndDate, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        # new line ########################################################################
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        border.Add(sizer, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # 备注
        label = wx.StaticText(self, wx.ID_ANY, u"备注：", size=(95, -1), style=wx.ALIGN_RIGHT)
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.remarkInput =\
            wx.TextCtrl(self, wx.ID_ANY, "", size=wx.Size(495, -1), style=wx.TE_MULTILINE)
        sizer.Add(self.remarkInput, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=wx.DefaultSize, style=wx.HORIZONTAL)
        border.Add(line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.TOP, 5)

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

    '''
    权限控制
    '''
    def auth_control(self):
        if self.current_user[2] == 2:
            self.customerCombobox.Disable()
            self.vehiclePlateNumInput.Disable()
            self.vehicleModelInput.Disable()
            self.vehicleRegDate.Disable()
            self.transCountInput.Disable()
            self.loanProductInput.Disable()
            self.loanPeriodInput.Disable()
            self.loanTermInput.Disable()
            self.loanDate.Disable()
            self.insuranceStartDate.Disable()
            self.insuranceEndDate.Disable()

    def enable_filter(self, event):
        self.ignoreEvtText = False
        event.Skip()

    '''
    过滤客户触发
    '''
    def filter_customer(self, event):

        if self.ignoreEvtText:
            self.ignoreEvtText = False
            return

        text = event.GetString().strip()
        self.customer_data = service.search_customer(text, None)
        data_count = len(self.customer_data)

        for index in range(0, data_count):
            self.customerCombobox.Insert(self.customer_data[index][0], index, self.customer_data[index][5])

        for i in range(data_count, len(self.customerCombobox.GetItems())):
            self.customerCombobox.Delete(data_count)

        self.ignoreEvtText = False

    '''
    选择客户触发
    '''
    def select_customer(self, event):
        cb = event.GetEventObject()
        data = cb.GetClientData(event.GetSelection())
        customer = self.customer_data[event.GetSelection()]
        self.customerGenderPanel.SetLabelText(customer[1])
        self.customerPhonePanel.SetLabelText(customer[2])
        self.ignoreEvtText = True
        event.Skip()

    """
    表单赋值
    """
    def set_data(self, data):

        self.data = data

        if self.data[0] is not None:
            self.customerCombobox.SetValue(self.data[0])
            self.customerGenderPanel.SetLabelText(self.data[1])
            self.customerPhonePanel.SetLabelText(self.data[2])

        self.vehiclePlateNumInput.SetValue(self.data[3])
        self.vehiclePlateNumInput.SetValidator(platenumvalidator.PlateNumValidator(self.data[22]))

        self.vehicleModelInput.SetValue(self.data[4])
        if self.data[5] is not None and self.data[5] != "":
            self.vehicleRegDate.SetValue(self.parse_date(self.data[5]))
        self.mileageInput.SetValue(self.data[6])
        self.transCountInput.SetValue(self.data[7])

        self.loanProductInput.SetValue(self.data[8])
        self.loanPeriodInput.SetValue(self.data[9])
        self.loanTermInput.SetValue(self.data[10])
        self.loanValueInput.SetValue(self.data[11])
        if self.data[12] is not None and self.data[12] != "":
            self.loanReportDate.SetValue(self.parse_date(self.data[12]))
        if self.data[13] is not None and self.data[13] != "":
            self.loanPassedDate.SetValue(self.parse_date(self.data[13]))
        if self.data[14] is not None and self.data[14] != "":
            self.loanDate.SetValue(self.parse_date(self.data[14]))

        if self.data[15] is not None:
            self.insuranceCompanyCombobox.SetValue(self.data[15])
        self.insuranceTypeInput.SetValue(self.data[16])
        if self.data[16] is not None and self.data[17] != "":
            self.insuranceStartDate.SetValue(self.parse_date(self.data[17]))
        if self.data[17] is not None and self.data[18] != "":
            self.insuranceEndDate.SetValue(self.parse_date(self.data[18]))

        self.remarkInput.SetValue(self.data[19])

    """
    表单取值
    """
    def get_form_values(self):
        form_values = ()
        if self.customerCombobox.GetSelection() == -1:
            wx.MessageBox("请选择客户！", "提示", style=wx.ICON_HAND)
            return False
        form_values = form_values + (self.customerCombobox.GetClientData(self.customerCombobox.GetSelection()),)

        if self.vehiclePlateNumInput.GetValue().strip() == "":
            wx.MessageBox("请输入车牌号！", "提示", style=wx.ICON_HAND)
            return False
        form_values = form_values + (self.vehiclePlateNumInput.GetValue().strip(),)

        if self.vehicleModelInput.GetValue().strip() == "":
            wx.MessageBox("请输入车辆型号！", "提示", style=wx.ICON_HAND)
            return False
        form_values = form_values + (self.vehicleModelInput.GetValue().strip(),)

        if not self.vehicleRegDate.GetValue().IsValid():
            wx.MessageBox("请输入车辆登记日期！", "提示", style=wx.ICON_HAND)
            return False
        form_values = form_values + (self.vehicleRegDate.GetValue().Format(format="%Y-%m-%d"),)

        form_values = form_values + (self.mileageInput.GetValue(), self.transCountInput.GetValue())

        if self.loanProductInput.GetValue().strip() == "":
            wx.MessageBox("请输入贷款产品！", "提示", style=wx.ICON_HAND)
            return False
        form_values = form_values + (self.loanProductInput.GetValue().strip(),)

        if self.loanPeriodInput.GetValue().strip() == "":
            wx.MessageBox("请输入期次！", "提示", style=wx.ICON_HAND)
            return False
        form_values = form_values + (self.loanPeriodInput.GetValue().strip(),)

        form_values = form_values + (self.loanTermInput.GetValue(), self.loanValueInput.GetValue())

        if self.loanReportDate.GetValue().IsValid():
            form_values = form_values + (self.loanReportDate.GetValue().Format(format="%Y-%m-%d"),)
        else:
            form_values = form_values + ("",)

        if self.loanPassedDate.GetValue().IsValid():
            form_values = form_values + (self.loanPassedDate.GetValue().Format(format="%Y-%m-%d"),)
        else:
            form_values = form_values + ("",)

        if not self.loanDate.GetValue().IsValid():
            wx.MessageBox("请输入放款日期！", "提示", style=wx.ICON_HAND)
            return False
        form_values = form_values + (self.loanDate.GetValue().Format(format="%Y-%m-%d"),)

        if not self.insuranceCompanyCombobox.GetSelection() == -1:
            form_values = form_values + \
                          (self.insuranceCompanyCombobox.GetClientData(self.insuranceCompanyCombobox.GetSelection()),)
        else:
            form_values = form_values + ("",)

        form_values = form_values + (self.insuranceTypeInput.GetValue().strip(),)

        if not self.insuranceStartDate.GetValue().IsValid():
            wx.MessageBox("请输入保险生效日期！", "提示", style=wx.ICON_HAND)
            return False
        form_values = form_values + (self.insuranceStartDate.GetValue().Format(format="%Y-%m-%d"),)

        if not self.insuranceEndDate.GetValue().IsValid():
            wx.MessageBox("请输入保险到期日期！", "提示", style=wx.ICON_HAND)
            return False
        form_values = form_values + (self.insuranceEndDate.GetValue().Format(format="%Y-%m-%d"),)

        form_values = form_values + (self.remarkInput.GetValue().strip(),)

        return form_values

    """
    取值
    """
    def get_data(self):
        vehicle = self.get_form_values()
        return vehicle + (self.data[22],)

    """
    保存
    """
    def save(self):
        customer = self.get_form_values()
        service.save_vehicle(customer)

    """
    更新
    """
    def update(self):
        customer = self.get_form_values()
        service.update_vehicle(self.data[22], customer)

    '''
    时间字符串转wx.dateTime
    '''
    @staticmethod
    def parse_date(date_str):
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return wx.pydate2wxdate(dt)

    '''
    计算保险到期日期
    '''
    def get_end(self, event):
        start = event.GetDate()
        span = wx.DateSpan(years=1, days=-1)
        end = start.Add(span)
        self.insuranceEndDate.SetValue(end)
