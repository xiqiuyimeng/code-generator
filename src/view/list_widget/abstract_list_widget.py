# -*- coding: utf-8 -*-
from src.view.item_view_widget.abstract_item_view import AbstractItemView
from src.view.searcher.smart_item_view import SmartSearcherListWidget

_author_ = 'luwt'
_date_ = '2023/2/16 11:24'


class AbstractListWidget(SmartSearcherListWidget, AbstractItemView):

    def __init__(self, *args):
        super().__init__(*args)
        # 设置列表项间距
        self.setSpacing(5)
