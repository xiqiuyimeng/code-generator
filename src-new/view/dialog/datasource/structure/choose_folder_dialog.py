# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QFrame, QLabel, QFormLayout

from view.custom_widget.draggable_widget import DraggableDialog

_author_ = 'luwt'
_date_ = '2022/11/17 10:16'


class ChooseFolderDialog(DraggableDialog):

    def __init__(self, screen_rect):
        super().__init__()
        self.parent_screen_rect = screen_rect
        # 当前对话框主布局
        self.dialog_layout: QVBoxLayout = ...
        # 当前对话框框架，用于放置所有部件
        self.frame: QFrame = ...
        # 框架布局，分四部分，第一部分：标题部分，第二部分：已选文件夹，第三部分：列表框，第四部分：按钮部分
        self.frame_layout: QVBoxLayout = ...
        self.title: QLabel = ...
        self.choose_folder_layout: QFormLayout = ...
        self.choose_folder_label: QLabel = ...
        self.choose_folder_display_label: QLabel = ...

        self.setup_ui()

    def setup_ui(self):
        # 计算窗口大小
        self.resize(self.parent_screen_rect.width() * 0.4, self.parent_screen_rect.height() * 0.5)
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
        self.frame.setObjectName("choose_folder_frame")
        self.dialog_layout.addWidget(self.frame)
        self.frame_layout = QVBoxLayout(self.frame)

        # 标题
        self.setup_title_ui()
        # 已选文件夹展示
        self.setup_choose_folder_form()

    def setup_title_ui(self):
        self.title = QLabel(self.frame)
        self.title.setObjectName("choose_folder_title")
        self.frame_layout.addWidget(self.title)

    def setup_choose_folder_form(self):
        self.choose_folder_layout = QFormLayout()

        self.choose_folder_label = QLabel(self.frame)
        self.choose_folder_label.setObjectName('choose_folder_label')

        self.choose_folder_display_label = QLabel(self.frame)
        self.choose_folder_display_label.setObjectName('choose_folder_display_label')

        self.choose_folder_layout.addRow(self.choose_folder_label, self.choose_folder_display_label)

        self.frame_layout.addLayout(self.choose_folder_layout)
