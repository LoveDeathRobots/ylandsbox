from PyQt5.QtCore import QUrl,QByteArray,pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView,QWebEngineProfile
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

class LoginDialog(QWidget):

    LoginRailIDSignel = pyqtSignal(int, str)
    def __init__(self, parnet=None):
        super().__init__()
        self.setup()

    def setup(self):
        self.box = QVBoxLayout(self)  # 创建一个垂直布局来放控件
        self.btn_get = QPushButton('点击获取cookies')  # 创建一个按钮涌来了点击获取cookie
        self.btn_get.clicked.connect(self.get_railid)  # 绑定按钮点击事件
        self.web = WebEngineView()  # 创建浏览器组件对象
        self.web.resize(1200, 600)  # 设置大小
        self.web.load(QUrl("https://ylands.qq.com/workshop/"))  # 打开百度页面来测试
        self.box.addWidget(self.btn_get)  # 将组件放到布局内，先在顶部放一个按钮
        self.box.addWidget(self.web)  # 再放浏览器
        self.web.show()  # 最后让页面显示出来


    def get_railid(self):
        cookie = self.web.get_railid()
        self.LoginRailIDSignel.emit(0, cookie)




# 创建自己的浏览器控件，继承自QWebEngineView
class WebEngineView(QWebEngineView):
    DomainCookies = {}
    PathCookies = {}
    def __init__(self, *args, **kwargs):
        super(WebEngineView, self).__init__(*args, **kwargs)
        # 绑定cookie被添加的信号槽
        QWebEngineProfile.defaultProfile().cookieStore().cookieAdded.connect(self.onCookieAdd)
        self.loadFinished.connect(self.onLoadFinished)
        self.cookies = {}  # 存放cookie字典

    def onCookieAdd(self, cookie):  # 处理cookie添加的事件
        domain = cookie.domain()
        path = cookie.path()
        name = cookie.name().data().decode('utf-8')
        value = cookie.value().data().decode('utf-8')

        if domain in self.DomainCookies:
            _cookie = self.DomainCookies[domain]
            _cookie[name] = value
        else:
            self.DomainCookies[domain] = {name: value}
        domain_path = domain + path

        if domain_path in self.PathCookies:
            _cookie = self.PathCookies[domain_path]
            _cookie[name] = value
        else:
            self.PathCookies[domain_path] = {name: value}

        name = cookie.name().data().decode('utf-8')  # 先获取cookie的名字，再把编码处理一下
        value = cookie.value().data().decode('utf-8')  # 先获取cookie值，再把编码处理一下
        self.cookies[name] = value  # 将cookie保存到字典里

    def getAllDomainCookies(self):

        return self.DomainCookies

    def getDomainCookies(self, domain):

        return self.DomainCookies.get(domain, {})

    def getAllPathCookies(self):

        return self.PathCookies

    def getPathCookies(self, dpath):

        return self.PathCookies.get(dpath, {})
    # 获取cookie
    def get_cookie(self):
        cookie_str = ''
        for key, value in self.cookies.items():  # 遍历字典
            cookie_str += (key + '=' + value + ';')  # 将键值对拿出来拼接一下
        return cookie_str  # 返回拼接好的字符串

    def get_railid(self):
        railid_str = ''
        if self.cookies.get('openid') is not None:
            railid_str = self.cookies['openid']
        return railid_str

    def onLoadFinished(self):
        # print("*****AllDomainCookies:", self.getAllDomainCookies())
        # print("*****AllPathCookies:", self.getAllPathCookies())
        # self.cookieView.append(
        #     "AllDomainCookies: " + self.bytestostr(self.getAllDomainCookies()))
        # self.cookieView.append('')
        # self.cookieView.append(
        #     "AllPathCookies: " + self.bytestostr(self.getAllPathCookies()))
        # self.cookieView.append('')
        print("*****ylands.qq.com cookie:", self.getDomainCookies(".qq.com"))
        # print("*****qq.com / path cookie:",
        #       self.getPathCookies(".qq.com/"))

    def closeEvent(self, event):
        self.cookieView.close()
        super(WebEngineView, self).closeEvent(event)

    def bytestostr(self, data):
        if isinstance(data, str):
            return data
        if isinstance(data, QByteArray):
            data = data.data()
        if isinstance(data, bytes):
            data = data.decode(errors='ignore')
        else:
            data = str(data)
        return data