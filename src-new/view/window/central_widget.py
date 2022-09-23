# -*- coding: utf-8 -*-
"""
中心窗体，左右布局，包含两部分，左边数据源目录，树结构，右边表格展示区
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSplitter

_author_ = 'luwt'
_date_ = '2022/9/14 10:10'


class CentralWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName('central_widget')
        self._layout = QHBoxLayout(self)
        self.horizontal_splitter = QSplitter(self)

        # 竖直方向的分割器
        self.horizontal_splitter.setOrientation(Qt.Horizontal)
        self._layout.addWidget(self.horizontal_splitter)

        # 标识当前展示的数据源列表类型
        self.datasource_show_type = ''






