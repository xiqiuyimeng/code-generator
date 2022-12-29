# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItemIterator

from view.searcher.search_func.searcher import Searcher

_author_ = 'luwt'
_date_ = '2022/5/9 19:03'


class TreeSearcher(Searcher):

    def __init__(self, target_tree, main_widget):
        super().__init__(target_tree, main_widget)

    def iterate_search(self, text, match_items):
        iterator = QTreeWidgetItemIterator(self.target)
        i = 0
        while iterator.value():
            item = iterator.value()
            item.setData(0, Qt.UserRole + 1, i)
            # 简单搜索，单字符匹配，确定范围
            self.simple_match_text(text, item, match_items)
            iterator = iterator.__iadd__(1)
            i += 1

    def fill_row_index(self):
        iterator = QTreeWidgetItemIterator(self.target)
        i = 0
        while iterator.value():
            item = iterator.value()
            item.setData(0, Qt.UserRole + 1, i)
            iterator = iterator.__iadd__(1)
            i += 1

    def get_item_text(self, item):
        return item.text(0)

    def search_post_processor(self):
        # 展开选中的元素
        self.expand_selected_items()

    def expand_selected_items(self):
        """展开选中的元素，如果当前元素是一个父节点，且其下子节点中存在选中元素，则展开父节点"""
        if self.match_item_records and self.match_item_records[-1]:
            [self.recursive_expanded(item) for item in self.match_item_records[-1]]

    def recursive_expanded(self, item):
        parent = item.parent()
        if parent is not None and not parent.isExpanded():
            parent.setExpanded(True)
            self.recursive_expanded(parent)

    def child_selected(self, item):
        for i in range(item.childCount()):
            if item.child(i) in self.match_item_records[-1]:
                return True

    def get_row_index(self, item) -> int:
        """获取按顺序排列的索引号"""
        user_data = item.data(0, Qt.UserRole + 1)
        if not user_data:
            self.fill_row_index()
            user_data = item.data(0, Qt.UserRole + 1)
        return user_data

    def clear_row_index(self):
        iterator = QTreeWidgetItemIterator(self.target)
        while iterator.value():
            item = iterator.value()
            item.setData(0, Qt.UserRole + 1, None)
            iterator = iterator.__iadd__(1)
