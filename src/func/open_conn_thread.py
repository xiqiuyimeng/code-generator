# -*- coding: utf-8 -*-
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon

from src.constant.constant import OPEN_CONN_MENU
from src.func.connection_function import open_connection
from src.func.tree_function import make_tree_item
from src.little_widget.message_box import pop_fail
from static import image_rc


_author_ = 'luwt'
_date_ = '2020/8/19 14:20'


class OpenConnWorker(QThread):

    # 定义信号，返回结果，第一个参数为是否成功，第二个：成功为返回的连接对象，失败为返回的异常信息
    result = pyqtSignal(tuple)

    def __init__(self, gui, conn_id, conn_name):
        super().__init__()
        self.gui = gui
        self.conn_id = conn_id
        self.conn_name = conn_name

    def run(self):
        self.open_conn()

    def open_conn(self):
        data = open_connection(self.gui, self.conn_id, self.conn_name)
        self.result.emit(data)


class AsyncOpenConn:

    def __init__(self, gui, conn_id, conn_name, item):
        self.gui = gui
        self.conn_id = conn_id
        self.conn_name = conn_name
        self.item = item
        self._movie = QtGui.QMovie(":/gif/loading_simple.gif")

    def open_conn(self):
        self._movie.start()
        self._movie.frameChanged.connect(lambda: self.item.setIcon(0, QIcon(self._movie.currentPixmap())))
        # 创建并启用子线程
        open_conn_thread = OpenConnWorker(self.gui, self.conn_id, self.conn_name)
        open_conn_thread.result.connect(lambda res: self.get_result(res))
        open_conn_thread.start()

    def get_result(self, data):
        """解析打开连接的结果"""
        self._movie.stop()
        self.item.setIcon(0, QIcon())
        if data[0]:
            dbs = data[1].get_dbs()
            for db in dbs:
                make_tree_item(self.gui, self.item, db)
            self.item.setExpanded(True)
        else:
            pop_fail(OPEN_CONN_MENU, data[1])

