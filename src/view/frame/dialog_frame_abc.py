# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QGridLayout, QPushButton

from src.constant.dialog_constant import QUIT_BTN_TEXT, HELP_BTN_TEXT

_author_ = 'luwt'
_date_ = '2023/4/3 8:52'


class DialogFrameABC(QFrame):
    """对话框框架抽象类"""

    def __init__(self, parent_dialog, dialog_title, placeholder_blank_width=2, need_help_button=True):
        super().__init__(parent_dialog)
        self.parent_dialog = parent_dialog
        # 标题label
        self.dialog_title = dialog_title
        # 空白占位label占栅格布局宽度，用来调节按钮布局美观
        self.placeholder_blank_width = placeholder_blank_width
        # 是否需要帮助按钮
        self.need_help_button = need_help_button
        # 框架布局，分三部分，第一部分：标题部分，第二部分：主体内容，第三部分：按钮部分
        self.frame_layout: QVBoxLayout = ...
        self.title: QLabel = ...
        self.button_layout: QGridLayout = ...
        self.placeholder_blank: QLabel = ...
        self.help_button: QPushButton = ...
        self.dialog_quit_button: QPushButton = ...
        self.help_dialog = ...

        # 构建界面
        self.setup_ui()
        # 连接信号
        self.connect_signal()
        # 后置处理
        self.post_process()

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_ui(self):
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
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

    def setup_content_ui(self):
        ...

    def setup_button_ui(self):
        self.button_layout = QGridLayout()
        self.frame_layout.addLayout(self.button_layout)

        if self.need_help_button:
            self.help_button = QPushButton()
            self.help_button.setObjectName('help_button')
            self.button_layout.addWidget(self.help_button, 0, 0, 1, 1)

        # 空白占位左侧的按钮组
        left_buttons = self.get_blank_left_buttons()
        if left_buttons:
            for idx, left_button in enumerate(left_buttons, start=self.button_layout.count()):
                self.button_layout.addWidget(left_button, 0, idx, 1, 1)

        self.button_layout.addWidget(self.placeholder_blank, 0, self.button_layout.count(),
                                     1, self.placeholder_blank_width)

        # 空白占位右侧的按钮组
        right_buttons = self.get_blank_right_buttons()
        if right_buttons:
            for idx, right_button in enumerate(right_buttons, start=self.get_blank_right_start_col_idx()):
                self.button_layout.addWidget(right_button, 0, idx, 1, 1)

        self.dialog_quit_button = QPushButton(self)
        self.dialog_quit_button.setObjectName('dialog_quit_button')
        self.button_layout.addWidget(self.dialog_quit_button, 0, self.get_blank_right_start_col_idx(), 1, 1)

    def get_blank_left_buttons(self) -> tuple:
        ...

    def get_blank_right_buttons(self) -> tuple:
        ...

    def get_blank_right_start_col_idx(self) -> int:
        return self.button_layout.count() + self.placeholder_blank_width - 1

    def setup_label_text(self):
        self.title.setText(self.dialog_title)
        if self.need_help_button:
            self.help_button.setText(HELP_BTN_TEXT)
        self.dialog_quit_button.setText(QUIT_BTN_TEXT)
        self.setup_other_label_text()

    def setup_other_label_text(self):
        ...

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def connect_signal(self):
        if self.need_help_button:
            self.help_button.clicked.connect(self.open_help_dialog)
        self.dialog_quit_button.clicked.connect(self.parent_dialog.close_dialog)
        self.connect_other_signal()

    def open_help_dialog(self):
        # 为了避免循环依赖问题，在打开对话框时再引用帮助对话框
        from src.view.dialog.help_dialog import HelpDialog
        self.help_dialog = HelpDialog(self.get_help_info_type())
        self.help_dialog.exec()

    def get_help_info_type(self) -> str:
        ...

    def connect_other_signal(self):
        ...

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        ...

    # ------------------------------ 后置处理 end ------------------------------ #

    def showEvent(self, event):
        # 展示的时候，设置对话框标题
        self.parent_dialog.setWindowTitle(self.dialog_title)
        super().showEvent(event)
