# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from src.constant.list_constant import VALUE_RANGE_TYPE_NAME, EDIT_VALUE_RANGE_BOX_TITLE
from src.view.list_widget.list_widget_abc import DraggableListWidgetABC
from src.view.list_widget.custom_list_widget import CustomListWidget

_author_ = 'luwt'
_date_ = '2023/2/13 15:15'


class ValueRangeListWidget(CustomListWidget, DraggableListWidgetABC):
    # 增加信号，列表项变化时发射
    changed_signal = pyqtSignal()

    def __init__(self, edit_value_range_func, *args):
        self.edit_value_range_func = edit_value_range_func
        super().__init__(VALUE_RANGE_TYPE_NAME, *args)
        # 当列表项文本变化触发
        self.itemChanged.connect(lambda: self.changed_signal.emit())

    def addItem(self, item):
        super().addItem(item)
        self.changed_signal.emit()

    def addItems(self, labels):
        super().addItems(labels)
        self.changed_signal.emit()

    def dropEvent(self, event):
        super().dropEvent(event)
        self.changed_signal.emit()

    def edit_item_func(self, item):
        self.edit_value_range_func(EDIT_VALUE_RANGE_BOX_TITLE, item.text())

    def remove_item_func(self, item):
        super().remove_item_func(item)
        self.changed_signal.emit()

    def clear_items_func(self):
        super().clear_items_func()
        self.changed_signal.emit()
