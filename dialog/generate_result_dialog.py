# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'generate_result.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog

from func.do_generate import dispatch_generate
from settings.font import set_title_font, set_font


class GenerateResultDialog(QDialog):

    # 定义信号，关闭父窗口
    close_parent_signal = pyqtSignal()

    def __init__(self, gui, output_config_dict, selected_data):
        super().__init__()
        self.gui = gui
        self.output_config_dict = output_config_dict
        self.selected_data = selected_data
        self.setup_ui()

    def setup_ui(self):
        self.setFont(set_font())
        self.setObjectName("Dialog")
        self.setFixedSize(600, 400)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setValue(0)
        self.verticalLayout.addWidget(self.progressBar)
        self.log_label = QtWidgets.QLabel(self)
        self.log_label.setObjectName("log_label")
        self.verticalLayout.addWidget(self.log_label)
        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        # 去掉窗口右上角的问号
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)

        # 创建并启用子线程
        self.thread_1 = Worker(self.gui, self.output_config_dict, self.selected_data)
        self.thread_1.result.connect(self.progress)
        self.thread_1.start()

        # 按钮事件
        self.buttonBox.accepted.connect(self.close_parent)
        self.buttonBox.rejected.connect(self.close)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def progress(self, progress_value, msg):
        self.progressBar.setValue(progress_value)
        self.textBrowser.append(msg)

    def close_parent(self):
        self.close()
        self.close_parent_signal.emit()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", set_title_font("完成进度")))
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText("确定")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText("返回配置页")


class Worker(QThread):

    # 定义信号，返回当前进度值及消息
    result = pyqtSignal(int, str)

    def __init__(self, gui, output_config_dict, selected_data):
        super().__init__()
        self.gui = gui
        self.output_config_dict = output_config_dict
        self.selected_data = selected_data

    def run(self):
        self.produce(self.consume())

    def consume(self):
        while True:
            n = yield
            # 发送信号
            self.result.emit(n[0], n[1])

    def produce(self, consumer):
        consumer.__next__()
        dispatch_generate(self.gui, self.output_config_dict, self.selected_data, consumer)
        consumer.close()

