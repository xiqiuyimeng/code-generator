# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'generate_result.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog

from src.func.do_generate import dispatch_generate
from src.sys.settings.font import set_title_font, set_font


class GenerateResultDialog(QDialog):

    # 定义信号，关闭父窗口
    close_parent_signal = pyqtSignal()

    def __init__(self, gui, output_config_dict, selected_data, screen_rect):
        super().__init__()
        self.gui = gui
        self._translate = QtCore.QCoreApplication.translate
        self.output_config_dict = output_config_dict
        self.selected_data = selected_data
        self.parent_screen_rect = screen_rect
        self.setup_ui()

    def setup_ui(self):
        self.setFont(set_font())
        self.setObjectName("Dialog")
        # 当前窗口大小根据父窗口大小计算
        self.resize(self.parent_screen_rect.width() * 0.6, self.parent_screen_rect.height() * 0.6)
        self.verticalLayout_frame = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_frame.setObjectName("verticalLayout_frame")
        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_blank = QtWidgets.QLabel(self.frame)
        self.label_blank.setText("")
        self.verticalLayout.addWidget(self.label_blank)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.progressBar = QtWidgets.QProgressBar(self.frame)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setValue(0)
        self.verticalLayout.addWidget(self.progressBar)
        self.log_label = QtWidgets.QLabel(self.frame)
        self.log_label.setObjectName("log_label")
        self.verticalLayout.addWidget(self.log_label)
        self.textBrowser = QtWidgets.QTextBrowser(self.frame)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.frame)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout_frame.addWidget(self.frame)

        # 不透明度
        self.setWindowOpacity(0.96)
        # 隐藏窗口边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置窗口背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        # 样式
        self.setStyleSheet("#frame,#textBrowser{border-style:solid;border-radius:20px;background-color:Gainsboro;}")

        # 创建并启用子线程
        self.thread_1 = Worker(self.gui, self.output_config_dict, self.selected_data)
        self.thread_1.result.connect(self.progress)
        self.thread_1.start()

        # 按钮事件
        self.buttonBox.accepted.connect(self.close_parent)
        self.buttonBox.rejected.connect(self.close)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def progress(self, saved_count, file_count, progress_value, msg):
        self.progressBar.setValue(progress_value)
        self.log_label.setText(self._translate("Dialog", f"总文件数：{file_count}个，已生成：{saved_count}个"))
        self.textBrowser.append(msg)

    def close_parent(self):
        self.close()
        self.close_parent_signal.emit()

    def retranslateUi(self):
        self.setWindowTitle(self._translate("Dialog", "Dialog"))
        self.label.setText(self._translate("Dialog", set_title_font("完成进度")))
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText("确定")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setFont(set_font())
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText("返回配置页")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setFont(set_font())


class Worker(QThread):

    # 定义信号，返回已生成文件数，总文件数，当前进度值及文件名
    result = pyqtSignal(int, int, int, str)

    def __init__(self, gui, output_config_dict, selected_data):
        super().__init__()
        self.gui = gui
        self.output_config_dict = output_config_dict
        self.selected_data = selected_data

    def run(self):
        self.produce(self.consume())

    def consume(self):
        count = 1
        while True:
            n = yield
            # 发送信号，第一个参数为已经生成的文件数，第二个参数为文件总数，
            # 第三个为进度条值，第四个为文件名
            self.result.emit(count, n[0], n[1], n[2])
            count += 1

    def produce(self, consumer):
        consumer.__next__()
        dispatch_generate(self.gui, self.output_config_dict, self.selected_data, consumer)
        consumer.close()

