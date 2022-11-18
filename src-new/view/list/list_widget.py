# -*- coding: utf-8 -*-
from PyQt5.QtCore import QSize

from view.custom_widget.scrollable_widget import ScrollableWidget
from view.searcher.smart_item_view import SmartSearcherListWidget

_author_ = 'luwt'
_date_ = '2022/11/18 9:56'


class ListWidget(SmartSearcherListWidget, ScrollableWidget):

    def __init__(self, parent):
        super().__init__(parent)
        # 统一设置图标大小
        self.setIconSize(QSize(40, 30))
