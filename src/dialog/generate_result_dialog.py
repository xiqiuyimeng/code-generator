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
from src.sys.settings.font import set_font


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
        self.label.setObjectName("title")
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
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.cancel_button = QtWidgets.QPushButton(self.frame)
        self.cancel_button.setObjectName("cancel_button")
        self.gridLayout.addWidget(self.cancel_button, 0, 0, 1, 1)
        self.button_blank = QtWidgets.QLabel(self.frame)
        self.gridLayout.addWidget(self.button_blank, 0, 1, 1, 2)
        self.ok_button = QtWidgets.QPushButton(self.frame)
        self.ok_button.setObjectName("ok_button")
        self.gridLayout.addWidget(self.ok_button, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout_frame.addWidget(self.frame)

        # 不透明度
        self.setWindowOpacity(0.96)
        # 隐藏窗口边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置窗口背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        # 样式
        self.setStyleSheet("#frame,#textBrowser{border-style:solid;border-radius:20px;background-color:qlineargradient("
                           "x1:0, y1:0, x2:1, y2:0, stop:0 lightyellow,stop:1 wheat);}"
                           "QPushButton{font-size:20px;font-family:楷体;font-weight:500px;color:black;"
                           "background-color:qlineargradient(x1:0, y1:0, x2:1, y2:0, "
                           "stop:0 lightgreen,stop:1 SpringGreen);border-radius:8px;border-style:outset;border-width:2px;"
                           "border-color:Thistle;padding-top:1px;padding-left:1px;padding-bottom:3px;padding-right:3px;}"
                           "QPushButton:hover{background-color:LimeGreen;}"
                           "QPushButton:pressed{background-color:green;border-style:inset;padding-top:3px;"
                           "padding-left:3px}"
                           "QLabel,QProgressBar,QTextBrowser{font-size:18px;font-family:楷体;}"
                           "#title{font-size:20px;font-family:楷体;font-weight:500;qproperty-alignment:AlignHCenter;}")

        # 创建并启用子线程
        self.thread_1 = Worker(self.gui, self.output_config_dict, self.selected_data)
        self.thread_1.result.connect(self.progress)
        self.thread_1.start()

        # 按钮事件
        self.cancel_button.clicked.connect(self.close)
        self.ok_button.clicked.connect(self.close_parent)

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
        self.label.setText("完成进度")
        self.cancel_button.setText("返回配置页")
        self.ok_button.setText("确定")


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

