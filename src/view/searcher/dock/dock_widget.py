# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDockWidget, QWidget

from view.searcher.line_edit.search_line_edit import SearcherLineEdit

_author_ = 'luwt'
_date_ = '2022/5/9 18:59'


class SearcherDockWidget(QDockWidget):

    def __init__(self, parent):
        super().__init__(parent)
        # 取一个空的widget设置为dock窗口的标题栏，以此来去除标题栏
        blank_widget = QWidget()
        self.setTitleBarWidget(blank_widget)
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        # 输入框，用来展示搜索时输入的内容，不允许输入
        self.line_edit = SearcherLineEdit()
        # 设置只读
        self.line_edit.setReadOnly(True)
        self.setWidget(self.line_edit)
