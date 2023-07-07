# -*- coding: utf-8 -*-
"""
消息弹窗
"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox, QLabel, QVBoxLayout, QFrame, QStyle, QHBoxLayout, QPushButton, QDialog

from src.constant.message_box_constant import OK_BUTTON, ACCEPT_BUTTON, REJECT_BUTTON
from src.service.read_qrc.read_config import read_qss
from src.view.custom_widget.draggable_widget import DraggableDialog

_author_ = 'luwt'
_date_ = '2020/6/21 16:08'


class MessageBox(DraggableDialog):
    """自定义消息弹窗对话框"""

    def __init__(self, box_icon, title, message, parent):
        self.box_icon = box_icon
        self.title = title
        self.message = message
        self.dialog_icon: QIcon = parent.windowIcon()

        self._layout: QVBoxLayout = ...
        self.frame: QFrame = ...
        self.frame_layout: QVBoxLayout = ...

        self.title_layout: QHBoxLayout = ...
        self.title_icon: QLabel = ...
        self.title_icon_height = 20
        self.title_label: QLabel = ...

        self.message_layout: QHBoxLayout = ...
        self.message_icon: QLabel = ...
        self.message_label: QLabel = ...

        self.button_layout: QHBoxLayout = ...
        super().__init__()

        self.setup_ui()
        self.setup_text()
        # 设置大小位置
        self.resize(self.sizeHint())

    def keyPressEvent(self, event) -> None:
        # 屏蔽esc键关闭窗口事件
        if event.key() == Qt.Key.Key_Escape:
            ...
        else:
            super().keyPressEvent(event)

    def setup_ui(self):
        self.setWindowIcon(self.dialog_icon)
        # 隐藏窗口边框
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.frame = QFrame(self)
        self._layout.addWidget(self.frame)

        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_layout = QVBoxLayout(self.frame)
        self.frame.setLayout(self.frame_layout)

        # 标题部分
        self.title_layout = QHBoxLayout()
        self.frame_layout.addLayout(self.title_layout)
        self.title_icon = QLabel()
        self.title_icon.setPixmap(self.dialog_icon.pixmap(self.title_icon_height, self.title_icon_height))
        # 固定宽度
        self.title_icon.setFixedWidth(self.title_icon_height)
        self.title_layout.addWidget(self.title_icon)
        self.title_label = QLabel()
        self.title_label.setObjectName('message_box_title')
        self.title_layout.addWidget(self.title_label)

        # 消息内容
        self.frame_layout.addSpacing(20)
        self.message_layout = QHBoxLayout()
        self.frame_layout.addLayout(self.message_layout)
        self.message_icon = QLabel()
        get_message_icon = self.get_message_icon()
        if get_message_icon:
            self.message_icon.setPixmap(get_message_icon.pixmap(50, 50))
        self.message_layout.addWidget(self.message_icon)
        self.message_label = QLabel()
        self.message_layout.addWidget(self.message_label)
        self.frame_layout.addSpacing(20)

    def setup_text(self):
        self.setWindowTitle(self.title)
        self.title_label.setText(self.title)
        self.message_label.setText(self.message)

    def add_button(self, button_text, button_role):
        if self.button_layout is Ellipsis:
            self.button_layout = QHBoxLayout()
            self.frame_layout.addLayout(self.button_layout)
            self.button_layout.addWidget(QLabel())
        button = QPushButton(button_text)
        # 宽度固定
        button.setFixedWidth(button.sizeHint().width())
        self.button_layout.addWidget(button)

        if button_role == QMessageBox.ButtonRole.AcceptRole:
            button.setObjectName('accept_button')
            button.clicked.connect(self.accept_clicked)
        elif button_role == QMessageBox.ButtonRole.RejectRole:
            button.setObjectName('reject_button')
            button.clicked.connect(self.reject_clicked)
        # 加载样式表
        button.setStyleSheet(read_qss())
        
    def accept_clicked(self):
        self.close_animation.finished.connect(self.accept)
        self.start_close_animation()

    def reject_clicked(self):
        self.close_animation.finished.connect(self.reject)
        self.start_close_animation()

    def get_message_icon(self):
        if self.box_icon == QMessageBox.Icon.Information:
            return self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation)
        elif self.box_icon == QMessageBox.Icon.Critical:
            return self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxCritical)
        elif self.box_icon == QMessageBox.Icon.Question:
            return self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxQuestion)


def pop_msg(title, msg, window=None):
    """
    弹出普通信息框
    :param title: 弹窗标题
    :param msg: 弹窗消息
    :param window: 父窗体
    """
    msg_box = MessageBox(QMessageBox.Icon.Information, title, msg, parent=window)
    msg_box.add_button(OK_BUTTON, QMessageBox.ButtonRole.AcceptRole)
    msg_box.exec()


def pop_ok(msg, title, window=None):
    """
    弹出执行成功消息框
    :param msg: 弹窗消息
    :param title: 标题
    :param window: 父窗体
    """
    msg_box = MessageBox(QMessageBox.Icon.NoIcon, title, msg, parent=window)
    msg_box.add_button(OK_BUTTON, QMessageBox.ButtonRole.AcceptRole)
    msg_box.exec()


def pop_fail(msg, title, window=None):
    """
    弹出失败消息框
    :param msg: 弹窗消息
    :param title: 标题
    :param window: 父窗体
    """
    msg_box = MessageBox(QMessageBox.Icon.Critical, title, msg, parent=window)
    msg_box.add_button(OK_BUTTON, QMessageBox.ButtonRole.AcceptRole)
    msg_box.exec()


def pop_question(msg, title, window=None):
    """
    弹出询问消息框
    :param msg: 弹窗消息
    :param title: 弹窗标题
    :param window: 父窗体
    """
    msg_box = MessageBox(QMessageBox.Icon.Question, title, msg, parent=window)
    msg_box.add_button(ACCEPT_BUTTON, QMessageBox.ButtonRole.AcceptRole)
    msg_box.add_button(REJECT_BUTTON, QMessageBox.ButtonRole.RejectRole)
    reply = msg_box.exec()
    return True if reply == QDialog.DialogCode.Accepted else False

