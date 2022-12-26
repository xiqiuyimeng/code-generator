# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QFrame, QGridLayout, QPushButton, QLabel

from constant.constant import RESELECT_TXT, CHOOSE_TEMPLATE_TXT
from view.custom_widget.draggable_widget import DraggableDialog
from view.tree.tree_widget.abstract_tree_widget import DisplayTreeWidget

_author_ = 'luwt'
_date_ = '2022/10/31 11:47'


class AbstractGeneratorDialog(DraggableDialog):

    def __init__(self, screen_rect):
        super().__init__()
        self.main_screen_rect = screen_rect
        self._layout: QVBoxLayout = ...
        self.frame: QFrame = ...
        self.button_layout: QGridLayout = ...
        self.setup_ui()
        self.connect_signal()

    def setup_ui(self):
        # 当前窗口大小根据主窗口大小计算
        self.setFixedSize(self.main_screen_rect.width() * 0.8,
                          self.main_screen_rect.height() * 0.8)
        # 设置布局，应该由两部分构成，主体和底部按钮区域
        self._layout = QVBoxLayout(self)
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.setup_main_frame()
        self._layout.addWidget(self.frame)

        self.button_layout = QGridLayout()
        self.setup_button_layout()
        self._layout.addLayout(self.button_layout)

        # 不透明度
        self.setWindowOpacity(0.95)
        # 隐藏窗口边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置窗口背景透明
        # self.setAttribute(Qt.WA_TranslucentBackground, True)

    def setup_main_frame(self): ...

    def setup_button_layout(self): ...

    def connect_signal(self): ...


class AbstractDisplaySelectedDialog(AbstractGeneratorDialog):

    def __init__(self, *args):
        self.frame_layout = ...
        self.header_label = ...
        self.display_tree_widget = ...
        self.reselect_button: QPushButton = ...
        self.choose_template_button: QPushButton = ...
        self.button_blank: QLabel = ...
        super().__init__(*args)

    def setup_main_frame(self):
        # 主体：标题、展示树结构
        self.frame_layout = QVBoxLayout()

        self.header_label = QLabel()
        header_text = self.get_header_text()
        self.header_label.setText(header_text)
        self.frame_layout.addWidget(self.header_label)

        # 展示树结构
        self.display_tree_widget = DisplayTreeWidget(self.frame)
        self.setup_tree_ui()
        self.display_tree_widget.expandAll()
        self.frame_layout.addWidget(self.display_tree_widget)

        self.frame.setLayout(self.frame_layout)

    def setup_button_layout(self):
        # 按钮区：返回修改、选择模板
        self.reselect_button = QPushButton()
        self.reselect_button.setText(RESELECT_TXT)
        self.reselect_button.setObjectName('reselect_button')
        self.button_layout.addWidget(self.reselect_button, 0, 0, 1, 1)

        self.button_blank = QLabel()
        self.button_layout.addWidget(self.button_blank, 0, 1, 1, 2)

        self.choose_template_button = QPushButton()
        self.choose_template_button.setText(CHOOSE_TEMPLATE_TXT)
        self.choose_template_button.setObjectName('choose_template_button')
        self.button_layout.addWidget(self.choose_template_button, 0, 3, 1, 1)

    def connect_signal(self):
        self.reselect_button.clicked.connect(self.close)

    def get_header_text(self) -> str: ...

    def setup_tree_ui(self): ...
