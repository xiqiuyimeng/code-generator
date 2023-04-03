# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QPushButton

from src.constant.generator_dialog_constant import RESELECT_TXT, CHOOSE_TEMPLATE_TXT
from src.view.dialog.custom_dialog import CustomDialog
from src.view.tree.tree_widget.tree_widget_abc import DisplayTreeWidget

_author_ = 'luwt'
_date_ = '2022/10/31 11:47'


class DisplaySelectedDialogABC(CustomDialog):

    def __init__(self, *args):
        self.display_tree_widget = ...
        self.reselect_button: QPushButton = ...
        self.choose_template_button: QPushButton = ...
        super().__init__(*args)

    # ------------------------------ 创建ui界面 start ------------------------------ #
    def resize_dialog(self):
        # 当前窗口大小根据主窗口大小计算
        self.setFixedSize(self.parent_screen_rect.width() * 0.8, self.parent_screen_rect.height() * 0.8)

    def setup_content_ui(self):
        # 展示树结构
        self.display_tree_widget = DisplayTreeWidget(self.frame)
        self.setup_tree_ui()
        self.display_tree_widget.expandAll()
        self.frame_layout.addWidget(self.display_tree_widget)

    def setup_tree_ui(self): ...

    def setup_other_button(self):
        # 按钮部分
        self.reselect_button = QPushButton(self.frame)
        self.button_layout.addWidget(self.reselect_button, 0, 0, 1, 1)
        self.choose_template_button = QPushButton(self.frame)
        self.button_layout.addWidget(self.choose_template_button, 0, 1, 1, 1)

    def setup_other_label_text(self):
        self.reselect_button.setText(RESELECT_TXT)
        self.choose_template_button.setText(CHOOSE_TEMPLATE_TXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def connect_other_signal(self):
        self.reselect_button.clicked.connect(self.close)

    # ------------------------------ 信号槽处理 end ------------------------------ #
