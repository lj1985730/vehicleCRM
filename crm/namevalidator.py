# coding=utf-8
import wx
from crm import service


class NameValidator(wx.Validator):
    """
    客户名称校验器
    """

    def __init__(self, customer_id):
        self.customer_id = customer_id
        wx.Validator.__init__(self)

    def Clone(self):
        return NameValidator(self.customer_id)

    def Validate(self, win):
        text_ctrl = self.GetWindow()
        text = text_ctrl.GetValue()

        if len(text.strip()) == 0:
            wx.MessageBox("请输入“姓名”！", "提示", style=wx.ICON_HAND)
            text_ctrl.SetBackgroundColour("pink")
            text_ctrl.SetFocus()
            text_ctrl.Refresh()
            return False
        elif service.check_customer_name_exist(text, (None if self.customer_id is None else self.customer_id)):
            wx.MessageBox("此名称已被使用！", "提示", style=wx.ICON_HAND)
            text_ctrl.SetBackgroundColour("pink")
            text_ctrl.SetFocus()
            text_ctrl.Refresh()
            return False
        else:
            text_ctrl.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
            text_ctrl.Refresh()
            return True

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True
