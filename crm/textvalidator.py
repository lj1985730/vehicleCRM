# coding=utf-8
import wx


class TextValidator(wx.Validator):

    def __init__(self):
        wx.Validator.__init__(self)

    def Clone(self):
        return TextValidator()

    def Validate(self, win):
        text_ctrl = self.GetWindow()
        text = text_ctrl.GetValue()

        if len(text.strip()) == 0:
            wx.MessageBox("请输入必填信息!", "Error")
            text_ctrl.SetBackgroundColour("pink")
            text_ctrl.SetFocus()
            text_ctrl.Refresh()
            return False
        else:
            text_ctrl.SetBackgroundColour(
                wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
            text_ctrl.Refresh()
            return True

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True
