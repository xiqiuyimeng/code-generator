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
from src.little_widget.loading_widget import LoadingMask
from src.little_widget.message_box import pop_fail
from src.scrollable_widget.scrollable_widget import MyTextBrowser


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
        self.resize(self.parent_screen_rect.width() * 0.8, self.parent_screen_rect.height() * 0.8)
        self.verticalLayout_frame = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_frame.setObjectName("verticalLayout_frame")
        self.result_frame = QtWidgets.QFrame(self)
        self.result_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.result_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.result_frame.setObjectName("result_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.result_frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_blank = QtWidgets.QLabel(self.result_frame)
        self.label_blank.setText("")
        self.verticalLayout.addWidget(self.label_blank)
        self.label = QtWidgets.QLabel(self.result_frame)
        self.label.setObjectName("title")
        self.verticalLayout.addWidget(self.label)
        self.progressBar = QtWidgets.QProgressBar(self.result_frame)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setValue(0)
        self.verticalLayout.addWidget(self.progressBar)
        self.log_label = QtWidgets.QLabel(self.result_frame)
        self.log_label.setObjectName("log_label")
        self.verticalLayout.addWidget(self.log_label)
        self.textBrowser = MyTextBrowser(self.result_frame)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.cancel_button = QtWidgets.QPushButton(self.result_frame)
        self.cancel_button.setObjectName("cancel_button")
        self.gridLayout.addWidget(self.cancel_button, 0, 0, 1, 1)
        self.button_blank = QtWidgets.QLabel(self.result_frame)
        self.gridLayout.addWidget(self.button_blank, 0, 1, 1, 2)
        self.ok_button = QtWidgets.QPushButton(self.result_frame)
        self.ok_button.setObjectName("ok_button")
        self.gridLayout.addWidget(self.ok_button, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout_frame.addWidget(self.result_frame)

        # 隐藏窗口边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置窗口背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        # 启动遮罩层
        self.set_loading_mask()
        # 创建并启用子线程
        self.generate_thread = GenerateWorker(self.gui, self.output_config_dict, self.selected_data)
        self.generate_thread.result.connect(self.progress)
        self.generate_thread.error.connect(self.handle_error)
        self.generate_thread.start()

        # 按钮事件
        self.cancel_button.clicked.connect(self.close)
        self.ok_button.clicked.connect(self.close_parent)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def set_loading_mask(self):
        """设置遮罩层，以防在刚打开界面时因异常而导致界面没有响应"""
        self.loading_mask = LoadingMask(self, ":/gif/loading.gif")
        self.loading_mask.show()
        self.installEventFilter(self.loading_mask)

    def progress(self, saved_count, file_count, progress_value, msg):
        # 当生成第一个文件的时候，证明数据准备已经没问题，关闭遮罩层
        if saved_count == 1:
            self.loading_mask.close()
        self.progressBar.setValue(progress_value)
        self.log_label.setText(self._translate("Dialog", f"总文件数：{file_count}个，已生成：{saved_count}个"))
        self.textBrowser.append(msg)

    def handle_error(self, e):
        # 当进度条值为0时发生异常，即为数据准备异常
        if self.progressBar.value() == 0:
            self.loading_mask.close()
        pop_fail("生成失败", f'{e.args[0]} - {e.args[1]}')

    def close_parent(self):
        self.close()
        self.close_parent_signal.emit()

    def retranslateUi(self):
        self.label.setText("完成进度")
        self.cancel_button.setText("返回配置页")
        self.ok_button.setText("确定")


class GenerateWorker(QThread):

    # 定义信号，返回已生成文件数，总文件数，当前进度值及文件名
    result = pyqtSignal(int, int, int, str)
    error = pyqtSignal(Exception)

    def __init__(self, gui, output_config_dict, selected_data):
        super().__init__()
        self.gui = gui
        self.output_config_dict = output_config_dict
        self.selected_data = selected_data

    def run(self):
        try:
            self.produce(self.consume())
        except Exception as e:
            self.error.emit(e)

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

