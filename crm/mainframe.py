# coding=utf-8
import wx
import datetime
from crm import loginwin, auth, customerpanel, vehiclepanel
import wx.lib.agw.flatnotebook as fnb


# noinspection PyUnusedLocal
class MainFrame(wx.Frame):
    """
    Main Frame
    """
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        self.customer_item = None
        self.vehicle_item = None
        self.make_menu_bar()    # 主菜单

        self.book = None
        self._rmenu = None

        self.layout_book()

        self.icon = wx.Icon('data\\icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        self.CreateStatusBar()    # 状态栏
        self.Center()

    """
    生成主菜单
    """
    def make_menu_bar(self):

        operate_menu = wx.Menu()

        login_item = operate_menu.Append(-1, "登录(&L)", u"登录后方能操作")

        operate_menu.AppendSeparator()

        exit_item = operate_menu.Append(wx.ID_EXIT)

        view_menu = wx.Menu()
        self.customer_item = view_menu.Append(-1, "客户信息(&C)", u"查看客户信息")
        self.vehicle_item = view_menu.Append(-1, "车辆信息(&V)", u"查看车辆信息")

        menu_bar = wx.MenuBar()
        menu_bar.Append(operate_menu, "操作(&O)")
        menu_bar.Append(view_menu, "查看(&Q)")

        self.SetMenuBar(menu_bar)

        # 绑定事件
        self.Bind(wx.EVT_MENU, self.on_login, login_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        self.Bind(wx.EVT_MENU, self.on_show_customer, self.customer_item)
        self.Bind(wx.EVT_MENU, self.on_show_vehicle, self.vehicle_item)
        self.toggle_menu()

    '''
    切换按钮权限
    '''
    def toggle_menu(self):
        self.customer_item.Enable(auth.Auth.logon_user is not None)
        self.vehicle_item.Enable(auth.Auth.logon_user is not None)

    '''
    创建右键菜单
    '''
    def create_right_click_menu(self):
        self._rmenu = wx.Menu()
        item = wx.MenuItem(self._rmenu, -1, "关闭Tab\tCtrl+F4", "关闭Tab")
        self._rmenu.Append(item)
        # Set right click menu to the notebook
        self.book.SetRightClickMenu(self._rmenu)

    '''
    初始化book
    '''
    def layout_book(self):
        self.book = fnb.FlatNotebook(self, wx.ID_ANY, agwStyle=fnb.FNB_DCLICK_CLOSES_TABS)
        self.book.Bind(wx.EVT_ERASE_BACKGROUND, self.add_bg_img)

    def add_bg_img(self, event):
        dc = event.GetDC()
        bmp = wx.Bitmap("data\\bg.jpg")
        dc.DrawBitmap(bmp, 0, 0)

    '''
    注销
    '''
    def on_exit(self, event):
        auth.Auth.logout()
        self.Close(True)

    '''
    账户登录
    '''
    def on_login(self, event):

        win = loginwin.LoginWin(self)
        win.CenterOnScreen()

        val = win.ShowModal()

        if val == wx.ID_OK:
            login_result = win.do_login()
            if not login_result:
                wx.MessageBox(u"用户名或密码错误！", u"错误", style=wx.ICON_ERROR)
                return

            limit_date = datetime.datetime.strptime("2017-10-31", "%Y-%m-%d")   # 限制使用后门
            if datetime.datetime.now() > limit_date:
                is_registered = auth.Auth.registered()
                if is_registered is None or len(is_registered) == 0:
                    wx.MessageBox(u"请先激活系统！", u"警告", style=wx.ICON_AUTH_NEEDED)
                    return

            self.toggle_menu()

        win.Destroy()

    '''
    显示客户信息
    '''
    def on_show_customer(self, event):
        self.Freeze()
        self.book.AddPage(customerpanel.CustomerPanel(self.book), "客户信息", True)
        self.Thaw()

    '''
    显示客户信息
    '''
    def on_show_vehicle(self, event):
        self.Freeze()
        self.book.AddPage(vehiclepanel.VehiclePanel(self.book), "车辆信息", True)
        self.Thaw()
