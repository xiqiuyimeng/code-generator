# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QPushButton

from src.constant.dialog_constant import OK_BTN_TEXT
from src.view.dialog.custom_dialog import CustomDialog

_author_ = 'luwt'
_date_ = '2022/11/22 10:20'


class CustomSaveDialog(CustomDialog):

    def __init__(self, *args, **kwargs):
        self.save_button: QPushButton = ...
        super().__init__(*args, **kwargs)

    def setup_button_ui(self):
        super().setup_button_ui()
        self.save_button = QPushButton(self.frame)
        # 保存按钮放在退出按钮的前一个位置
        self.button_layout.addWidget(self.save_button, 0, self.quit_button_row_index - 1, 1, 1)

    def setup_label_text(self):
        self.save_button.setText(OK_BTN_TEXT)
        super().setup_label_text()

    def connect_signal(self):
        self.save_button.clicked.connect(self.save_func)
        super().connect_signal()

    def save_func(self): ...
