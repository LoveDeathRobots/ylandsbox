import sys
import logging
from PyQt5.QtWidgets import QApplication
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import QCoreApplication, Qt
from MainWin import MainWin

logger = logging.getLogger(__name__)
class App:

    instance = None

    def exec_(self, code):
        """执行 Python 代码"""
        obj = compile(code, '<string>', 'single')
        self._g.update({
            'app': self
        })
        exec(obj, self._g, self._g)

    def show_msg(self, msg, *args, **kwargs):
        logger.info(msg)

    @staticmethod
    def get_resolving():
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        height = screen_rect.height()
        width = screen_rect.width()
        return height, width


if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    ylands = MainWin()
    ylands.show()
    res = app.exec_()
    sys.exit(res)
