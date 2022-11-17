# -*- coding: utf-8 -*-
from view.searcher.search_func.searcher import Searcher

_author_ = 'luwt'
_date_ = '2022/11/17 16:11'


class ListSearcher(Searcher):

    def __init__(self, target_list, main_widget):
        super().__init__(target_list, main_widget)

    def iterate_search(self, text, match_items):
        pass
