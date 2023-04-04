# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QGridLayout, QPushButton

from src.constant.dialog_constant import QUIT_BTN_TEXT

_author_ = 'luwt'
_date_ = '2023/4/3 8:52'


class DialogFrameABC(QFrame):
    """对话框框架抽象类"""

    def __init__(self, parent_dialog, dialog_title, quit_button_row_index=3):
        super().__init__(parent_dialog)
        self.parent_dialog = parent_dialog
        # 标题label
        self.dialog_title = dialog_title
        # 退出按钮行位置，退出按钮在栅格布局最后的位置，默认为3，即表格布局的一行可以容纳四个控件
        self.quit_button_row_index = quit_button_row_index
        # 框架布局，分三部分，第一部分：标题部分，第二部分：主体内容，第三部分：按钮部分
        self.frame_layout: QVBoxLayout = ...
        self.title: QLabel = ...
        self.button_layout: QGridLayout = ...
        self.placeholder_blank: QLabel = ...
        self.dialog_quit_button: QPushButton = ...

        # 构建界面
        self.setup_ui()
        # 连接信号
        self.connect_signal()
        # 后置处理
        self.post_process()

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_ui(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.frame_layout = QVBoxLayout(self)
        # 创建空白label
        self.placeholder_blank = QLabel(self)

        # 标题
        self.setup_title_ui()
        # 主体部分
        self.setup_content_ui()
        # 按钮
        self.setup_button_ui()
        # 设置文本
        self.setup_label_text()

    def setup_title_ui(self):
        self.title = QLabel(self)
        self.title.setObjectName("dialog_title")
        self.frame_layout.addWidget(self.title)

    def setup_content_ui(self): ...

    def setup_button_ui(self):
        self.button_layout = QGridLayout()
        self.frame_layout.addLayout(self.button_layout)

        self.button_layout.addWidget(self.placeholder_blank, 0, 0, 1, self.quit_button_row_index)
        self.dialog_quit_button = QPushButton(self)
        self.button_layout.addWidget(self.dialog_quit_button, 0, self.quit_button_row_index, 1, 1)

        self.setup_other_button()

    def setup_other_button(self): ...

    def setup_label_text(self):
        self.title.setText(self.dialog_title)
        self.dialog_quit_button.setText(QUIT_BTN_TEXT)
        self.setup_other_label_text()

    def setup_other_label_text(self): ...

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def connect_signal(self):
        self.dialog_quit_button.clicked.connect(self.parent_dialog.close)
        self.connect_other_signal()

    def connect_other_signal(self): ...

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self): ...

    # ------------------------------ 后置处理 end ------------------------------ #
