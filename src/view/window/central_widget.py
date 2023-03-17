# -*- coding: utf-8 -*-
"""
中心窗体，左右布局，包含两部分，左边数据源目录，树结构，右边表格展示区
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSplitter

from src.view.tab.tab_frame.tab_frame import get_tab_frame
from src.view.tree.tree_frame.tree_frame import get_tree_frame

_author_ = 'luwt'
_date_ = '2022/9/14 10:10'


class CentralWidget(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setObjectName('central_widget')
        self._layout = QHBoxLayout(self)
        self.horizontal_splitter = QSplitter(self)

        # 竖直方向的分割器
        self.horizontal_splitter.setOrientation(Qt.Horizontal)
        # 设置拉伸时，不覆盖子控件，也就是不会隐藏控件
        self.horizontal_splitter.setChildrenCollapsible(False)
        self._layout.addWidget(self.horizontal_splitter)

        self.frame_dict = dict()

        self.tree_frame = ...
        self.tab_frame = ...

    def setup_ui(self):
        # 隐藏frame的原因是：如果在切换数据源的时候，也就是frame存在，那么重新获取一个frame，
        # 会导致页面一直增加frame，而非切换的效果，所以需要将之前的frame先隐藏，再展示需要展示的frame
        if self.tree_frame is not Ellipsis:
            self.tree_frame.hide()
        if self.tab_frame is not Ellipsis:
            self.tab_frame.hide()

        # 获取tree frame
        tree_frame_key = f'tree-frame:{self.main_window.current_ds_category.name}'
        self.tree_frame = self.frame_dict.get(tree_frame_key)
        if not self.tree_frame:
            self.tree_frame = get_tree_frame(self.main_window.current_ds_category.name,
                                             self.horizontal_splitter, self.main_window)
            self.frame_dict[tree_frame_key] = self.tree_frame
        self.tree_frame.show()

        # 获取tab frame
        tab_frame_key = f'tab-frame:{self.main_window.current_ds_category.name}'
        self.tab_frame = self.frame_dict.get(tab_frame_key)
        if not self.tab_frame:
            self.tab_frame = get_tab_frame(self.main_window.current_ds_category.name,
                                           self.horizontal_splitter, self.main_window)
            self.frame_dict[tab_frame_key] = self.tab_frame
        self.tab_frame.show()

        # 重新打开树，同时也会将tab页打开
        self.tree_frame.reopen_tree()

        self.horizontal_splitter.setStretchFactor(0, 1)
        self.horizontal_splitter.setStretchFactor(1, 3)

        self.horizontal_splitter.setStretchFactor(2, 1)
        self.horizontal_splitter.setStretchFactor(3, 3)
