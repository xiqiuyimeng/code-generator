# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QAbstractItemView, QTreeWidget, QListWidget

from view.searcher.search_func.tree_searcher import TreeSearcher

_author_ = 'luwt'
_date_ = '2022/5/9 19:07'


class SmartSearcherItemView(QAbstractItemView):

    def __init__(self, parent):
        self.parent_widget = parent
        super().__init__(parent)
        self.searcher = self.get_searcher()

    def get_searcher(self): ...

    def keyPressEvent(self, event):
        self.searcher.handle_search(event.key(), event.text(), super().keyPressEvent, event)

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

    def __init__(self, parent):
        super().__init__(parent)

    def get_searcher(self):
        return TreeSearcher(self, self.parent_widget)


class SmartSearcherListWidget(QListWidget, SmartSearcherItemView):

    def __init__(self, parent):
        super().__init__(parent)

    def get_searcher(self):
        return
