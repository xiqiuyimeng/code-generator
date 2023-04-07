# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QPushButton, QVBoxLayout

from src.view.frame.dialog_frame_abc import DialogFrameABC

_author_ = 'luwt'
_date_ = '2023/4/4 12:36'


class ChainDialogFrameABC(DialogFrameABC):
    """链式调用对话框框架抽象类"""

    def __init__(self, parent_dialog_layout, *args):
        # 父对话框布局，在布局中添加和移除框架，实现页面切换
        self.parent_dialog_layout: QVBoxLayout = parent_dialog_layout
        # 上一个框架
        self.previous_frame: DialogFrameABC = ...
        # 下一个框架
        self.next_frame: DialogFrameABC = ...
        self.previous_frame_button: QPushButton = ...
        self.next_frame_button: QPushButton = ...
        super().__init__(*args)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_other_button(self):
        # 按钮部分
        self.previous_frame_button = QPushButton(self)
        self.button_layout.addWidget(self.previous_frame_button, 0, 0, 1, 1)
        self.next_frame_button = QPushButton(self)
        self.button_layout.addWidget(self.next_frame_button, 0, 1, 1, 1)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def connect_other_signal(self):
        self.previous_frame_button.clicked.connect(lambda: self.switch_frame(self.previous_frame))
        self.next_frame_button.clicked.connect(lambda: self.switch_frame(self.next_frame))

    def switch_frame(self, frame: DialogFrameABC):
        if frame is not Ellipsis:
            self.parent_dialog_layout.removeWidget(self)
            self.hide()
            self.parent_dialog_layout.addWidget(frame)
            if frame.isHidden():
                frame.show()
        else:
            self.parent_dialog.close()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    def set_previous_frame(self, frame):
        self.previous_frame = frame

    def set_next_frame(self, frame):
        self.next_frame = frame
        # 先隐藏下一个框架
        self.next_frame.hide()
