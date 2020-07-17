# -*- coding: utf-8 -*-
_author_ = 'luwt'
_date_ = '2020/7/15 15:56'
import sys
import time
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class test(QWidget):

    def __init__(self):
        super().__init__()

    def setupUi(self):
        self.setFixedSize(500, 90)
        self.main_widget = QtWidgets.QWidget(self)
        self.progressBar = QtWidgets.QProgressBar(self.main_widget)
        self.progressBar.setGeometry(QtCore.QRect(20, 20, 450, 30))
        # 创建并启用子线程
        self.thread_1 = Worker()
        self.thread_1.progressBarValue.connect(self.copy_file)
        self.thread_1.start()

    def copy_file(self, i):
        self.progressBar.setValue(i)


class Worker(QThread):

    progressBarValue = pyqtSignal(int)  # 更新进度条

    def __init__(self):
        super(Worker, self).__init__()


    def run(self):
        for i in range(101):
            time.sleep(0.1)
            self.progressBarValue.emit(i)  # 发送进度条的值 信号


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    testIns = test()
    testIns.setupUi()
    testIns.show()
    sys.exit(app.exec_())