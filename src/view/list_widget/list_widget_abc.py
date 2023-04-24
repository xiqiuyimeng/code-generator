# -*- coding: utf-8 -*-

from src.view.custom_widget.item_view_abc import ItemViewABC, DraggableItemViewABC
from src.view.searcher.smart_item_view import SmartSearcherListWidget

_author_ = 'luwt'
_date_ = '2023/2/16 11:24'


class ListWidgetABC(SmartSearcherListWidget, ItemViewABC):

    def __init__(self, *args):
        super().__init__(*args)
        # 设置列表项间距
        self.setSpacing(5)


class DraggableListWidgetABC(ListWidgetABC, DraggableItemViewABC):

    def dropEvent(self, event) -> None:
        DraggableItemViewABC.dropEvent(self, event)
