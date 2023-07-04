# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView, QTreeWidget, QListWidget

from src.view.searcher.search_func.list_searcher import ListSearcher
from src.view.searcher.search_func.tree_searcher import TreeSearcher

_author_ = 'luwt'
_date_ = '2022/5/9 19:07'


class SmartSearcherItemView(QAbstractItemView):

    def __init__(self, parent):
        self.parent_widget = parent
        super().__init__(parent)
        self.searcher = self.get_searcher()

    def get_searcher(self):
        ...

    def keyPressEvent(self, event):
        # ctrl F 触发
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_F:
            self.searcher.show_search()
        else:
            # 其他按键触发
            self.searcher.continue_search()

    def set_selected_focus(self, item):
        # 设置对应节点选中状态
        if not self.hasFocus():
            self.setFocus()
        self.setCurrentItem(item)
        # 选中节点后，将节点滑动到视图中央
        self.scrollToItem(item, QAbstractItemView.PositionAtCenter)
        # 滚动到视图中央后，可能由于水平方向其他项文本过长，导致计算的水平中央并不能展示出当前项，所以在调用一次滚动确保可见
        self.scrollToItem(item, QAbstractItemView.EnsureVisible)


class SmartSearcherTreeWidget(QTreeWidget, SmartSearcherItemView):

    def get_searcher(self):
        return TreeSearcher(self, self.parent_widget)

    def keyPressEvent(self, event) -> None:
        # 按键方法应该传递给智能搜索
        SmartSearcherItemView.keyPressEvent(self, event)


class SmartSearcherListWidget(QListWidget, SmartSearcherItemView):

    def get_searcher(self):
        return ListSearcher(self, self.parent_widget)

    def keyPressEvent(self, event) -> None:
        # 按键方法应该传递给智能搜索
        SmartSearcherItemView.keyPressEvent(self, event)
