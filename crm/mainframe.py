# coding=utf-8
import wx
from crm import loginwin, auth


# noinspection PyUnusedLocal
class MainFrame(wx.Frame):
    """
    Main Frame
    """
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        self.make_menu_bar()    # 主菜单
        self.CreateStatusBar()    # 状态栏

    """
    生成主菜单
    """
    def make_menu_bar(self):

        operate_menu = wx.Menu()
        login_item = operate_menu.Append(-1, "登录(&L)", u"登录后方能操作")

        operate_menu.AppendSeparator()

        exit_item = operate_menu.Append(wx.ID_EXIT)

        menu_bar = wx.MenuBar()
        menu_bar.Append(operate_menu, "操作(&O)")

        self.SetMenuBar(menu_bar)

        # 绑定事件
        self.Bind(wx.EVT_MENU, self.on_login, login_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)

    '''
    注销
    '''
    def on_exit(self, event):
        auth.Auth.logout()
        print(auth.Auth.logon_user)
        self.Close(True)

    '''
    账户登录
    '''
    def on_login(self, event):
        win = loginwin.LoginWin(self)
        win.CenterOnScreen()

        val = win.ShowModal()

        if val == wx.ID_OK:
            win.do_login()
            print(auth.Auth.logon_user)

        win.Destroy()
