# coding=utf-8
import wx
from crm import service


class PlateNumValidator(wx.Validator):
    """
    车牌号校验器
    """

    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        wx.Validator.__init__(self)

    def Clone(self):
        return PlateNumValidator(self.vehicle_id)

    def Validate(self, win):
        text_ctrl = self.GetWindow()
        text = text_ctrl.GetValue()

        if len(text.strip()) == 0:
            wx.MessageBox("请输入“车牌号”！", "提示", style=wx.ICON_HAND)
            text_ctrl.SetBackgroundColour("pink")
            text_ctrl.SetFocus()
            text_ctrl.Refresh()
            return False
        elif service.check_plate_num_exist(text, (None if self.vehicle_id is None else self.vehicle_id)):
            wx.MessageBox("此车牌号已被使用！", "提示", style=wx.ICON_HAND)
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
