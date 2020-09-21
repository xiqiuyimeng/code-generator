# -*- coding: utf-8 -*-
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon

from src.constant.constant import TEST_CONN_SUCCESS_PROMPT, TEST_CONN_FAIL_PROMPT
from src.func.connection_function import test_connection
from src.little_widget.message_box import pop_ok, pop_fail

_author_ = 'luwt'
_date_ = '2020/8/19 11:35'


class TestConnWorker(QThread):

    # 定义信号，返回测试结果，第一个参数为是否成功，第二个为提示语
    result = pyqtSignal(bool, str)

    def __init__(self, connection):
        super().__init__()
        self.conn = connection

    def run(self):
        self.test_conn()

    def test_conn(self):
        try:
            test_connection(self.conn)
            self.result.emit(True, TEST_CONN_SUCCESS_PROMPT)
        except Exception as e:
            self.result.emit(False, f'{TEST_CONN_FAIL_PROMPT}：[{self.conn.name}]\t\n {e}')


class AsyncTestConn:

    def __init__(self, conn, title, item):
        self.conn = conn
        self.title = title
        self.item = item
        self._movie = QtGui.QMovie(":/gif/loading_simple.gif")
        self.icon = self.item.icon(0)

    def test_conn(self):
        self._movie.start()
        self._movie.frameChanged.connect(lambda: self.item.setIcon(0, QIcon(self._movie.currentPixmap())))
        # 创建并启用子线程，这里需要注意的是，线程需要处理为类成员变量，
        # 如果是方法内的局部变量，在方法自上而下执行完后将被销毁
        self.test_conn_thread = TestConnWorker(self.conn)
        self.test_conn_thread.result.connect(lambda flag, prompt: self.get_test_result(flag, prompt))
        self.test_conn_thread.start()

    def get_test_result(self, flag, prompt):
        """解析测试连接的结果"""
        self._movie.stop()
        self.item.setIcon(0, self.icon)
        if flag:
            pop_ok(self.title, prompt)
        else:
            pop_fail(self.title, prompt)
