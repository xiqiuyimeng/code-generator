# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout

from src.view.custom_widget.draggable_widget import DraggableDialog
from src.view.frame.dialog_frame_abc import DialogFrameABC
from src.view.frame.save_dialog_frame import SaveDialogFrame
from src.view.frame.stacked_dialog_frame import StackedDialogFrame

_author_ = 'luwt'
_date_ = '2023/4/3 15:30'


class CustomDialogABC(DraggableDialog):
    """通用对话框抽象类"""

    def __init__(self, dialog_title, screen_rect):
        super().__init__()
        self.dialog_title = dialog_title
        self.parent_screen_rect = screen_rect
        # 当前对话框主布局
        self.dialog_layout: QVBoxLayout = ...
        # 对话框frame
        self.frame: DialogFrameABC = ...

        # 构建ui
        self.setup_ui()
        # 连接信号槽
        self.connect_signal()

    def setup_ui(self):
        # 计算窗口大小
        self.resize_dialog()
        # 不透明度
        self.setWindowOpacity(0.97)
        # 隐藏窗口边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置窗口背景透明
        # self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.dialog_layout = QVBoxLayout(self)
        self.dialog_layout.setContentsMargins(0, 0, 0, 0)
        self.dialog_layout.setSpacing(0)

        self.frame = self.get_frame()
        self.dialog_layout.addWidget(self.frame)

    def resize_dialog(self): ...

    def get_frame(self) -> DialogFrameABC: ...

    def connect_signal(self): ...


class CustomSaveDialogABC(CustomDialogABC):
    """通用具有保存功能对话框抽象类"""
    save_signal: pyqtSignal = ...
    edit_signal: pyqtSignal = ...

    def __init__(self, *args):
        self.frame: SaveDialogFrame = ...
        super().__init__(*args)

    def connect_signal(self):
        if self.frame.save_signal is not Ellipsis \
                and self.save_signal is not Ellipsis:
            self.frame.save_signal.connect(self.save_signal.emit)
        if self.frame.edit_signal is not Ellipsis \
                and self.edit_signal is not Ellipsis:
            self.frame.edit_signal.connect(self.edit_signal.emit)


class StackedDialogABC(CustomSaveDialogABC):
    """堆栈式窗口对话框抽象类"""

    def get_frame(self) -> StackedDialogFrame: ...
