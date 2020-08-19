# -*- coding: utf-8 -*-
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon

from src.func.connection_function import test_connection
from src.little_widget.message_box import pop_ok, pop_fail
from static import image_rc

_author_ = 'luwt'
_date_ = '2020/8/19 11:35'


class TestConnWorker(QThread):

    # 定义信号，返回测试结果，第一个参数为是否成功，第二个为提示语
    result = pyqtSignal(tuple)

    def __init__(self, connection):
        super().__init__()
        self.conn = connection

    def run(self):
        self.test_conn()

    def test_conn(self):
        test_res = test_connection(self.conn)
        self.result.emit(test_res)


class AsyncTestConn:

    def __init__(self, conn, title, item):
        self.conn = conn
        self.title = title
        self.item = item
        self._movie = QtGui.QMovie(":/gif/loading_simple.gif")

    def test_conn(self):
        self._movie.start()
        self._movie.frameChanged.connect(lambda: self.item.setIcon(0, QIcon(self._movie.currentPixmap())))
        # 创建并启用子线程，这里需要注意的是，线程需要处理为类成员变量，
        # 如果是方法内的局部变量，在方法自上而下执行完后将被销毁
        self.test_conn_thread = TestConnWorker(self.conn)
        self.test_conn_thread.result.connect(lambda res: self.get_test_result(res))
        self.test_conn_thread.start()

    def get_test_result(self, test_res):
        """解析测试连接的结果"""
        self._movie.stop()
        self.item.setIcon(0, QIcon())
        if test_res[0]:
            pop_ok(self.title, test_res[1])
        else:
            pop_fail(self.title, test_res[1])
