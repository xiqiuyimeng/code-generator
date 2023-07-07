# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QCheckBox

_author_ = 'luwt'
_date_ = '2022/12/29 9:21'


class CheckBox(QCheckBox):
    """点击应该是两态，修改状态时为三态"""

    # 由于点击导致的复选框状态变化
    click_state_changed = pyqtSignal(Qt.CheckState)

    def __init__(self):
        super().__init__()
        # 连接点击信号
        self.clicked.connect(self.click_change_state)

    def click_change_state(self, state):
        """如果点击以后的状态为 true，那么将复选框设置为已选中，否则设置为未选中，
        目的是跳过点击时的部分选中情况"""
        check_state = Qt.CheckState.Checked if state else Qt.CheckState.Unchecked
        self.setCheckState(check_state)
        self.click_state_changed.emit(check_state)
