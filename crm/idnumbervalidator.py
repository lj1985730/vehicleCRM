# coding=utf-8
import wx
import string
from crm import service


class IdNumberValidator(wx.Validator):
    """
    客户身份证校验器
    """

    def __init__(self, customer_id):
        self.customer_id = customer_id
        wx.Validator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.on_char)

    def Clone(self):
        return IdNumberValidator(self.customer_id)

    def Validate(self, win):
        text_ctrl = self.GetWindow()
        text = text_ctrl.GetValue()

        if len(text.strip()) == 0:
            wx.MessageBox("请输入“身份证号”！", "提示", style=wx.ICON_HAND)
            text_ctrl.SetBackgroundColour("pink")
            text_ctrl.SetFocus()
            text_ctrl.Refresh()
            return False
        elif service.check_id_number_exist(text, (None if self.customer_id is None else self.customer_id)):
            wx.MessageBox("此身份证号已被使用！", "提示", style=wx.ICON_HAND)
            text_ctrl.SetBackgroundColour("pink")
            text_ctrl.SetFocus()
            text_ctrl.Refresh()
            return False
        else:
            text_ctrl.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
            text_ctrl.Refresh()
            return True

    def on_char(self, event):
        key = event.GetKeyCode()

        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return

        if chr(key) in string.digits or chr(key) == 'x' or chr == 'X':
            event.Skip()
            return

        if not wx.Validator.IsSilent():
            wx.Bell()

        # Returning without calling even.Skip eats the event before it
        # gets to the text control
        return

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True
