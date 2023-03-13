# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QPushButton

from src.constant.dialog_constant import OK_BTN_TEXT, QUIT_PROMPT, QUIT_BOX_TITLE
from src.view.box.message_box import pop_question
from src.view.dialog.custom_dialog import CustomDialog

_author_ = 'luwt'
_date_ = '2022/11/22 10:20'


class CustomSaveDialog(CustomDialog):

    def __init__(self, *args, **kwargs):
        self.save_button: QPushButton = ...
        super().__init__(*args, **kwargs)

    def keyPressEvent(self, event: QKeyEvent):
        # 拦截esc按键导致的退出事件
        if event.key() == Qt.Key_Escape:
            # 弹出提示，需要保存数据，确认退出再执行
            if pop_question(QUIT_PROMPT, QUIT_BOX_TITLE, self):
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_button_ui(self):
        super().setup_button_ui()
        self.save_button = QPushButton(self.frame)
        # 保存按钮放在退出按钮的前一个位置
        self.button_layout.addWidget(self.save_button, 0, self.quit_button_row_index - 1, 1, 1)

    def setup_label_text(self):
        self.save_button.setText(OK_BTN_TEXT)
        super().setup_label_text()

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def connect_signal(self):
        # 先执行其他信号槽操作，最后执行保存
        super().connect_signal()
        self.save_button.clicked.connect(self.save_func)

    def save_func(self): ...

    # ------------------------------ 信号槽处理 end ------------------------------ #
