# -*- coding: utf-8 -*-
import inspect

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QHBoxLayout, QLabel

from src.view.custom_widget.check_box import CheckBox

_author_ = 'luwt'
_date_ = '2022/5/10 15:27'


class TableWidgetItem(QTableWidgetItem):

    def __init__(self, table):
        """自定义单元格项"""
        self.table = table
        super().__init__()
        self.setTextAlignment(Qt.AlignCenter)

    def setText(self, text):
        if not text:
            return
        if not isinstance(text, str):
            text = str(text)
        super().setText(text)


def make_checkbox_num_widget(label_text, clicked_slot_func):
    check_num_widget = QWidget()
    check_layout = QHBoxLayout(check_num_widget)
    check_box = CheckBox()
    setattr(check_num_widget, 'check_box', check_box)
    check_layout.addWidget(check_box)
    check_layout.setContentsMargins(0, 0, 0, 0)
    check_layout.setAlignment(check_box, Qt.AlignRight)
    check_label = QLabel()
    setattr(check_num_widget, 'check_label', check_label)
    check_label.setText(str(label_text))
    check_layout.addWidget(check_label)
    check_layout.setAlignment(check_label, Qt.AlignCenter)
    # 连接信号槽，获取方法签名，如果形参是一个，传递选中状态，如果是两个，传递选中状态和序号
    if len(inspect.signature(clicked_slot_func).parameters) == 1:
        check_box.click_state_changed.connect(lambda check_state: clicked_slot_func(check_state))
    elif len(inspect.signature(clicked_slot_func).parameters) == 2:
        check_box.click_state_changed.connect(lambda check_state: clicked_slot_func(check_state, check_label.text()))
    else:
        check_box.click_state_changed.connect(lambda: clicked_slot_func())
    return check_num_widget


def make_checkbox_num_widget_with_button(label_text, clicked_slot_func, button):
    checkbox_num_widget = make_checkbox_num_widget(label_text, clicked_slot_func)
    checkbox_num_widget.layout().addWidget(button)
    # 设置三个部件等宽排列
    checkbox_num_widget.layout().setStretch(0, 1)
    checkbox_num_widget.layout().setStretch(1, 1)
    checkbox_num_widget.layout().setStretch(2, 1)
    setattr(checkbox_num_widget, 'button', button)
    return checkbox_num_widget
