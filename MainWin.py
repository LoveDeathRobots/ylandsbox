from PyQt5.QtWidgets import QMainWindow, QGroupBox, QFileDialog, QFileSystemModel, QMenu, QTreeView, QApplication, QMessageBox
from PyQt5.QtCore import Qt, QMimeData, QUrl, QFile
from PyQt5.QtGui import QCursor, QDragEnterEvent, QDropEvent, QDragMoveEvent
from UI.Main import Ui_MainWindow
from Login import LoginDialog
from ImageRGB import ImageRGB
import os, winreg, shutil


class MainWin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWin,self).__init__()
        self.setupUi(self)
        self.Login.triggered.connect(self.open_login)
        self.RGB.triggered.connect(self.open_image_rgb)
        self.LoginDialog = LoginDialog()
        self.ImageMainWin = ImageRGB()


        # 设置TreeWidgets
        self.trees = [self.YCPGAMETREE, self.YCPCOMPTREE, self.YLANDFILETREE]
        for tree in self.trees:
            tree.setContextMenuPolicy(Qt.CustomContextMenu)
            tree.customContextMenuRequested.connect(self.show_context_menu)
            tree.header().setMinimumSectionSize(120)

        self.model = QFileSystemModel()

        self.RailID = ''
        self.ylands_path = ''
        self.rail_user_data = ''
        self.ycp_game_folder_path = ''
        self.ycp_comp_folder_path = ''
        self.yland_folder_path = ''
        self.key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Rail\YlandsRail")
        _value, type = winreg.QueryValueEx(self.key, "InstallPath")
        if _value:
            self.ylands_path = _value
            self.rail_user_data = os.path.dirname(self.ylands_path) + '\\' + 'rail_user_data\\2000108'
        self.YCPTAB.currentChanged.connect(self.refresh_tab_qlistwidget)
        self.GroupBoxTitleDict = {0: 'YCP游戏目录', 1: 'YCP组件目录', 2: 'YLAND文件目录'}
        self.YCPTAB.setCurrentIndex(0)
        print(self.OpenDirBtn.clicked)

    # 打开workshop 后去RailId
    def open_login(self):
        self.LoginDialog.LoginRailIDSignel.connect(self.slot_emit)
        self.LoginDialog.show()

    def open_image_rgb(self):
        self.ImageMainWin.show()

    def slot_emit(self, flag, str):
        # 获得 rail_id
        self.RailID = str
        self.ycp_game_folder_path = self.rail_user_data + '\\' + self.RailID + '\\cloud_storage\\files\\Share\\Games'
        self.ycp_comp_folder_path = self.rail_user_data + '\\' + self.RailID + '\\cloud_storage\\files\\Share\\Compositions'
        self.yland_folder_path = self.rail_user_data + '\\' + self.RailID + '\\cloud_storage\\files\\Scenarios'
        if not os.path.exists(self.ycp_game_folder_path):
            pass
        if not os.path.exists(self.ycp_comp_folder_path):
            pass
        if not os.path.exists(self.yland_folder_path):
            pass
        self.YCPTAB.setEnabled(True)
        self.YCPTAB.setCurrentIndex(0)
        self.refresh_tab_qlistwidget(0)
        self.setAcceptDrops(True)

    def refresh_tab_qlistwidget(self, index):
        if self.RailID != '':
            self.OpenDirBtn.setEnabled(True)
            if index == 0:
                self.YCPGAMETREE.setEnabled(True)
                self.refresh_path(index, self.ycp_game_folder_path)
                self.model.setRootPath(self.ycp_game_folder_path)
                self.YCPGAMETREE.setModel(self.model)
                self.YCPGAMETREE.setRootIndex(self.model.index(self.ycp_game_folder_path))

            elif index == 1:
                self.YCPCOMPTREE.setEnabled(True)
                self.refresh_path(index, self.ycp_comp_folder_path)
                self.model.setRootPath(self.ycp_comp_folder_path)
                self.YCPCOMPTREE.setModel(self.model)
                self.YCPCOMPTREE.setRootIndex(self.model.index(self.ycp_comp_folder_path))
            else:
                self.YLANDFILETREE.setEnabled(True)
                self.refresh_path(index, self.yland_folder_path)
                self.model.setRootPath(self.yland_folder_path)
                self.YLANDFILETREE.setModel(self.model)
                self.YLANDFILETREE.setRootIndex(self.model.index(self.yland_folder_path))

    def refresh_path(self, index, path):
        self.files_count(path)
        self.frame.findChild(QGroupBox, 'groupBox').setTitle(self.GroupBoxTitleDict[index])
        self.PathTxt.setText(path)
        if MainWin.isconnected(self.OpenDirBtn, 'clicked()'):
            self.OpenDirBtn.disconnect()
        self.OpenDirBtn.clicked.connect(lambda: self.open_dir(path, index))
        #TODO 通过背景颜色，显示文件被使用的状态

    def open_dir(self, path, index):
        # QFileDialog.getExistingDirectory(self,"浏览"+ self.GroupBoxTitleDict[index], path, QFileDialog.ShowDirsOnly)
        QFileDialog.getOpenFileNames(self, "浏览" + self.GroupBoxTitleDict[index], path, "All Files (*);;Text Files (*.txt)")

    def files_count(self, path):
        count = 0
        for root, dirs, files in os.walk(path):
            for each in files:
                file = os.path.splitext(each)
                filename, type = file
                if type != '.txt':
                    count += 1
        self.statusbar.showMessage("文件数：" + str(count))

    @staticmethod
    def isconnected(obj, name):
        """判断信号是否连接
        :param obj:        对象
        :param name:       信号名，如 clicked()
        """
        index = obj.metaObject().indexOfMethod(name)
        if index > -1:
            method = obj.metaObject().method(index)
            if method:
                return obj.isSignalConnected(method)
        return False

    def show_context_menu(self, pos):
        sender: QTreeView = self.sender()
        row_index = sender.indexAt(pos).row()
        menu = QMenu()
        cpy = menu.addAction('复制')
        cpy.triggered.connect(lambda: self.copy_selected(sender.currentIndex()))
        rmfile = menu.addAction('删除')
        rmfile.triggered.connect(lambda: self.remove_selected_file(sender.currentIndex()))
        menu.exec_(QCursor.pos())

    def copy_selected(self, index):
        filename = self.model.fileName(index)
        filepath = self.model.filePath(index)
        data = QMimeData()
        url = QUrl.fromLocalFile(filepath)
        clipboard = QApplication.clipboard()
        data.setUrls([url])
        clipboard.setMimeData(data)

    def remove_selected_file(self, index):
        filename = self.model.fileName(index)
        filepath = self.model.filePath(index)
        if not self.model.fileInfo(index).isDir():
            msgBox = QMessageBox()
            msgBox.setText("确定删除文件：" + filename + "?")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            ret = msgBox.exec_()
            if ret == QMessageBox.Ok:
                self.model.remove(index)
            else:
                return

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls:
            filetempname = event.mimeData().urls()[0].fileName()
            filename, extension = os.path.splitext(filetempname)
            if self.YCPTAB.currentIndex() == 0 or self.YCPTAB.currentIndex() == 1:
                if extension == '.ycp':
                    event.accept()
                    # clipboard = QApplication.clipboard()
                    # clipboard.clear()
                    # clipboard.setMimeData(event.mimeData())
                else:
                    msgBox = QMessageBox()
                    msgBox.setText("只能拖放.ycp后缀文件")
                    ret = msgBox.exec_()
                    event.ignore()
                    return
            elif self.YCPTAB.currentIndex() == 2:
                if extension == '.yland':
                    event.accept()
                    # clipboard = QApplication.clipboard()
                    # clipboard.clear()
                    # clipboard.setMimeData(event.mimeData())
                else:
                    msgBox = QMessageBox()
                    msgBox.setText("只能拖放.yland后缀文件")
                    ret = msgBox.exec_()
                    event.ignore()
                    return

    def dragMoveEvent(self, event: QDragMoveEvent):
        if event.mimeData().hasUrls:
            try:
                event.setDropAction(Qt.CopyAction)
            except Exception as e:
                print(e)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        try:
            if event.mimeData().hasUrls:
                event.setDropAction(Qt.CopyAction)
                event.accept()
                filepath = event.mimeData().urls()[0]
                filename = filepath.fileName()
                if self.YCPTAB.currentIndex() == 0:
                    self.copy_file(filepath.url().replace("file:///", ""), os.path.join(self.ycp_game_folder_path, filename))
                elif self.YCPTAB.currentIndex() == 1:
                    self.copy_file(filepath.url().replace("file:///", ""), os.path.join(self.ycp_comp_folder_path, filename))
                else:
                    self.copy_file(filepath.url().replace("file:///", ""), os.path.join(self.yland_folder_path, filename))
            else:
                event.ignore()
        except Exception as e:
            print(e)

    def copy_file(self,srcfle, dstfile):
        newdstfile = dstfile
        if not os.path.isfile(srcfle):
            print("$%s not exist!" % (srcfle))
        else:
            fpath, ftempname = os.path.split(dstfile)
            if not os.path.exists(fpath):
                os.makedirs(fpath)
            elif os.path.exists(dstfile):
                filename, extension = os.path.splitext(ftempname)
                newdstfile = os.path.join(fpath, filename + "copybyylandsbox" + extension)
            shutil.copyfile(srcfle, newdstfile)

