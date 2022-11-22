# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QFrame, QLabel, QGridLayout, QPushButton

from constant.constant import OK_BTN_TEXT, CANCEL_BTN_TEXT
from view.custom_widget.draggable_widget import DraggableDialog

_author_ = 'luwt'
_date_ = '2022/11/22 10:20'


class CustomDialog(DraggableDialog):

    def __init__(self, screen_rect, dialog_title):
        super().__init__()
        self.parent_screen_rect = screen_rect
        self.dialog_title = dialog_title
        # 当前对话框主布局
        self.dialog_layout: QVBoxLayout = ...
        # 当前对话框框架，用于放置所有部件
        self.frame: QFrame = ...
        # 框架布局，分三部分，第一部分：标题部分，第二部分：主体内容，第三部分：按钮部分
        self.frame_layout: QVBoxLayout = ...
        self.title: QLabel = ...
        self.placeholder_blank: QLabel = ...
        self.button_layout: QGridLayout = ...
        self.save_button: QPushButton = ...
        self.cancel_button: QPushButton = ...

        self.setup_ui()

    def get_dialog_title(self) -> str: ...

    def setup_ui(self):
        # 计算窗口大小
        self.resize_dialog()
        # 不透明度
        self.setWindowOpacity(0.95)
        # 隐藏窗口边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置窗口背景透明
        # self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.dialog_layout = QVBoxLayout(self)
        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("dialog_frame")
        self.dialog_layout.addWidget(self.frame)
        self.frame_layout = QVBoxLayout(self.frame)

        # 标题
        self.setup_title_ui()
        # 主体部分
        self.setup_content_ui()
        # 按钮
        self.setup_button_ui()
        # 设置文本
        self.setup_label_text()
        # 连接信号
        self.connect_signal()
        # 后置处理
        self.post_process()

    def resize_dialog(self): ...

    def setup_title_ui(self):
        self.title = QLabel(self.frame)
        self.title.setObjectName("dialog_title")
        self.frame_layout.addWidget(self.title)

    def setup_content_ui(self): ...

    def setup_button_ui(self):
        self.button_layout = QGridLayout()

        self.button_layout.addWidget(self.placeholder_blank, 0, 0, 1, 2)
        self.save_button = QPushButton(self.frame)
        self.button_layout.addWidget(self.save_button, 0, 2, 1, 1)
        self.cancel_button = QPushButton(self.frame)
        self.button_layout.addWidget(self.cancel_button, 0, 3, 1, 1)
        self.setup_other_button()

        self.frame_layout.addLayout(self.button_layout)

    def setup_other_button(self): ...

    def setup_label_text(self):
        self.title.setText(self.dialog_title)
        self.save_button.setText(OK_BTN_TEXT)
        self.cancel_button.setText(CANCEL_BTN_TEXT)
        self.setup_other_label_text()

    def setup_other_label_text(self): ...

    def connect_signal(self):
        self.save_button.clicked.connect(self.save_func)
        self.cancel_button.clicked.connect(self.close)
        self.connect_other_signal()

    def save_func(self): ...

    def connect_other_signal(self): ...

    def post_process(self): ...
