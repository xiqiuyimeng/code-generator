# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt

from view.searcher.search_func.searcher import Searcher

_author_ = 'luwt'
_date_ = '2022/11/17 16:11'


class ListSearcher(Searcher):

    def __init__(self, target_list, main_widget):
        super().__init__(target_list, main_widget)

    def get_item_text(self, item) -> str:
        return item.text()

    def iterate_search(self, text, match_items):
        for idx in range(self.target.count()):
            item = self.target.item(idx)
            item.setData(Qt.UserRole + 1, idx)
            # 简单搜索
            self.simple_match_text(text, item, match_items)

    def get_row_index(self, item) -> int:
        return self.target.indexFromItem(item).row()