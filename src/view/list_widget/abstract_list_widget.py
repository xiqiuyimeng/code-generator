# -*- coding: utf-8 -*-
from PyQt5.QtGui import QDropEvent

from src.view.item_view_widget.abstract_item_view import AbstractItemView
from src.view.searcher.smart_item_view import SmartSearcherListWidget

_author_ = 'luwt'
_date_ = '2023/2/16 11:24'


class AbstractListWidget(SmartSearcherListWidget, AbstractItemView):

    def __init__(self, *args):
        super().__init__(*args)
        # 设置列表项间距
        self.setSpacing(5)

    def dropEvent(self, event: QDropEvent):
        # 重写，实现拖拽效果
        # 获取拖入事件的坐标
        pos = event.pos()
        # 获取当前坐标下的item
        current_item = self.itemAt(pos)
        # 获取该item的index
        current_index = self.indexFromItem(current_item)
        # 获取行数
        current_row = current_index.row()

        # 获取拖入item的父组件
        source_widget = event.source()
        # 获取所有拖入item
        source_items = source_widget.selectedItems()
        # 当前允许单选就可以了，这样减少其他地方的复杂度
        for source_item in source_items:
            # 在列表中移除之前的项
            self.takeItem(self.indexFromItem(source_item).row())
            # 插入到当前位置
            self.insertItem(current_row, source_item)
