# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QFrame, QLabel, QFormLayout, QGridLayout, QPushButton, QListWidgetItem

from constant.constant import SAVE_STRUCT_TITLE, SAVE_STRUCT_TO, CREATE_NEW_FOLDER, OK_BTN_TEXT, CANCEL_BTN_TEXT
from view.custom_widget.draggable_widget import DraggableDialog
from view.list.list_widget import ListWidget

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
        self.list_widget: ListWidget = ...
        self.button_layout: QGridLayout = ...
        self.create_folder_button: QPushButton = ...
        self.button_blank: QLabel = ...
        self.save_button: QPushButton = ...
        self.cancel_button: QPushButton = ...

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
        # 列表部件
        self.setup_list_widget()
        # 按钮
        self.setup_button_ui()
        # 文本
        self.setup_label_text()
        # 连接信号
        self.connect_signal()
        # 展示列表项
        self.setup_list_item()

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

    def setup_list_widget(self):
        self.list_widget = ListWidget(self.frame)
        self.list_widget.setObjectName('list_widget')
        self.frame_layout.addWidget(self.list_widget)

    def setup_button_ui(self):
        self.button_layout = QGridLayout()

        self.create_folder_button = QPushButton(self.frame)
        self.create_folder_button.setObjectName('create_folder_button')
        self.button_layout.addWidget(self.create_folder_button, 0, 0, 1, 1)
        self.button_blank = QLabel(self.frame)
        self.button_layout.addWidget(self.button_blank, 0, 1, 1, 1)
        self.save_button = QPushButton(self.frame)
        self.save_button.setObjectName('save_button')
        self.button_layout.addWidget(self.save_button, 0, 2, 1, 1)
        self.cancel_button = QPushButton(self.frame)
        self.button_layout.addWidget(self.cancel_button, 0, 3, 1, 1)

        self.frame_layout.addLayout(self.button_layout)

    def setup_label_text(self):
        self.title.setText(SAVE_STRUCT_TITLE)
        self.choose_folder_label.setText(SAVE_STRUCT_TO)
        self.create_folder_button.setText(CREATE_NEW_FOLDER)
        self.save_button.setText(OK_BTN_TEXT)
        self.cancel_button.setText(CANCEL_BTN_TEXT)

    def connect_signal(self):
        self.cancel_button.clicked.connect(self.close)

    def setup_list_item(self):
        item = QListWidgetItem()
        item.setText('test1')
        self.list_widget.addItem(item)

        item1 = QListWidgetItem()
        item1.setText('test2')
        self.list_widget.addItem(item1)

        item2 = QListWidgetItem()
        item2.setText('test3')
        self.list_widget.addItem(item2)
