# coding=utf-8
import wx


class LoginFrame(wx.Frame):
    """
    Log in Frame
    """

    def __init__(self):
        wx.Frame.__init__(self, None, -1, u"登陆", size=(400, 300))

        # 窗体居中
        self.Centre()

        panel = wx.Panel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        # self.SetAutoLayout(True)
        #
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title = wx.StaticText(panel, -1, u"欢迎使用客户车辆管理系统", pos=(25, 25))
        title_sizer.Add(title)

        sizer.Add(title_sizer, proportion=3, flag=wx.ALL | wx.EXPAND, border=5)

        # name_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # name_label = wx.StaticText(panel, -1, u"用户名", pos=(125, 200))
        # name_sizer.Add(name_label)
        # name_input = wx.TextCtrl(panel, 1001, "请输入账号", pos=(150, 100), size=(175, -1))
        # name_sizer.Add(name_input)
        #
        # sizer.Add(name_sizer)
        #
        # pass_sizer = wx.BoxSizer(wx.HORIZONTAL)
        #
        # sizer.Add(pass_sizer)



        # font = title.GetFont()
        # # font.PointSize += 10
        # font = font.Bold()
        # title.SetFont(font)
        # box_sizer.Add(title)

        # self.make_menu_bar()

        # name_input = wx.TextCtrl(self, 1001, "请输入账号", pos=(150, 100), size=(175, -1))
        # box_sizer.Add(name_input)
        #
        # pass_label = wx.StaticText(self, -1, u"密码", pos=(25, 175))
        # box_sizer.Add(pass_label)
        # pass_input = wx.TextCtrl(self, 1002, "请输入密码", pos=(150, 175), size=(175, -1))
        # box_sizer.Add(pass_input)

        panel.SetSizer(sizer)
        # sizer.Fit(self)

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("客户车辆管理系统——登陆")

    def make_menu_bar(self):
        file_menu = wx.Menu()
        exit_item = file_menu.Append(wx.ID_EXIT, "(&Q)退出")

        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "(&O)操作")

        # Give the menu bar to the frame
        self.SetMenuBar(menu_bar)

        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)

    def on_exit(self):
        self.Close(True)

if __name__ == '__main__':
    app = wx.App()
    window = LoginFrame()
    window.Show()
    app.MainLoop()
