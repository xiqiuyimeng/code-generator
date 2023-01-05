# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QCheckBox

_author_ = 'luwt'
_date_ = '2022/12/29 9:21'


class CheckBox(QCheckBox):
    """点击应该是两态，修改状态时为三态"""

    # 由于点击导致的复选框状态变化
    click_state_changed = pyqtSignal(int)
    # 复选框非点击情况下，复选框状态变化信号，主要用在联动时使用
    not_click_state_changed = pyqtSignal(int)

    def __init__(self, allow_emit_signal=None):
        super().__init__()
        self.allow_emit_signal = allow_emit_signal
        self.clicking = False
        # 连接点击信号
        self.clicked.connect(self.click_change_state)
        # 连接状态变化信号
        self.stateChanged.connect(self.not_click_change_state)

    def mousePressEvent(self, event) -> None:
        self.clicking = True
        super().mousePressEvent(event)

    def click_change_state(self, state):
        """如果点击以后的状态为 true，那么将复选框设置为已选中，否则设置为未选中，
        目的是跳过点击时的部分选中情况"""
        check_state = Qt.Checked if state else Qt.Unchecked
        self.setCheckState(check_state)
        self.click_state_changed.emit(check_state)
        self.clicking = False

    def not_click_change_state(self, state):
        # 如果存在 allow_emit_signal，需要加上 allow_emit_signal 判断结果
        allow_emit_signal = not self.allow_emit_signal or \
                            (self.allow_emit_signal and self.allow_emit_signal())
        if not self.clicking and allow_emit_signal:
            self.not_click_state_changed.emit(state)
