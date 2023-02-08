# -*- coding: utf-8 -*-
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QStyledItemDelegate, QStyle

from src.view.searcher.style_item_delegate.painter_delegate import ItemPainterContext

_author_ = 'luwt'
_date_ = '2022/5/9 19:06'


class SearchStyledItemDelegate(QStyledItemDelegate):

    def __init__(self, parent, search_item_dict, match_item_records, get_item_text_func):
        self.search_item_dict = search_item_dict
        self.match_item_records = match_item_records
        self.get_item_text_func = get_item_text_func

        self.parent = parent
        super().__init__(parent)

    def paint(self, painter, option, index):
        # 取最新的匹配记录
        match_items = self.match_item_records[-1] if self.match_item_records else list()
        # 将当前的painter暂存
        painter.save()
        # item
        item = self.parent.itemFromIndex(index)
        selected_flag = option.state & QStyle.State_Selected
        search_flag = match_items and item in match_items

        # 如果既不是选中元素也不是搜索元素，使用原方式进行渲染
        if not selected_flag and not search_flag:
            super().paint(painter, option, index)
        else:
            # 展示的文本
            idx_str = self.get_item_text_func(item)
            # 重构后的绘制代码
            context = ItemPainterContext(item, self.parent)
            search_item_records = self.search_item_dict.get(id(item))[-1] \
                if self.search_item_dict.get(id(item)) else None
            context.init_item_rect(painter, option, index, idx_str, selected_flag, search_flag, search_item_records)
            # 如果是选中元素，处理背景色
            if selected_flag:
                self.draw_selected_background(option, painter)
            context.paint_item()
        # 弹出刚才保存的painter
        painter.restore()

    @staticmethod
    def draw_selected_background(option, painter):
        # 计算选中框大小
        rect = QRect(0, 0, option.rect.width(), option.rect.height())
        # 背景色设置为青绿色
        painter.fillRect(rect, QBrush(QColor(175, 238, 238)))
