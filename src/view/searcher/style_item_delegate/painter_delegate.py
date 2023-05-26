# -*- coding: utf-8 -*-
from abc import ABC

from PyQt5.QtCore import QRect, Qt, QRectF
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QStyle, QTreeWidgetItem, QListWidgetItem, QStyleOptionButton

_author_ = 'luwt'
_date_ = '2022/5/9 19:05'

# 默认空的rect
none_rect = QRect(0, 0, 0, 0)


class ItemPainterContext:

    def __init__(self, item, parent):
        self.item = item
        self.parent = parent
        self.margin_h = ...
        self.painters = ...

    def init_item_rect(self, painter, option, index, item_text,
                       selected_flag, search_flag, search_item_records):
        style = option.widget.style()
        # 获取当前item rect
        visual_rect = self.parent.visualRect(index)
        # 平移坐标系到item rect的位置
        painter.translate(visual_rect.x(), visual_rect.y())
        # 小部件的水平方向margin，一个小部件会存在左右两个边距
        self.margin_h = style.pixelMetric(QStyle.PM_FocusFrameHMargin) + 1
        self.painters = (CheckBoxItemPainter(self.item, self.margin_h, style, painter, visual_rect),
                         IconItemPainter(self.item, self.margin_h, style, painter, visual_rect, self.parent),
                         TextItemPainter(item_text, selected_flag, search_flag, search_item_records,
                                         self.item, self.margin_h, style, painter, visual_rect))

    def paint_item(self):
        left_x = 0
        for painter in self.painters:
            if painter.match_type():
                rect = painter.calculate_paint_rect(left_x)
                painter.paint_rect(rect)
                # 计算下一个rect的x和宽度，不需要考虑高度和y，因为高度和y一定是相同的
                left_x = rect.x() + rect.width()


def get_item_checkbox(item):
    if isinstance(item, QTreeWidgetItem):
        return item.data(0, Qt.CheckStateRole)
    elif isinstance(item, QListWidgetItem):
        return item.data(Qt.CheckStateRole)


def get_item_icon(item):
    if isinstance(item, QTreeWidgetItem):
        return item.icon(0)
    elif isinstance(item, QListWidgetItem):
        return item.icon()


class ItemPainterABC(ABC):

    def __init__(self, item, margin_h, style, painter, visual_rect, *args):
        self.item = item
        self.margin_h = margin_h
        self.style = style
        self.painter = painter
        self.visual_rect = visual_rect
        self.match = ...

    def match_type(self) -> bool:
        ...

    def calculate_paint_rect(self, left_x):
        ...

    def paint_rect(self, rect):
        ...


class CheckBoxItemPainter(ItemPainterABC):

    def __init__(self, item, margin_h, style, painter, visual_rect):
        super().__init__(item, margin_h, style, painter, visual_rect)
        self.checkbox_width = self.style.pixelMetric(QStyle.PM_IndicatorWidth)
        self.check_state = get_item_checkbox(self.item)

    def match_type(self) -> bool:
        self.match = self.check_state is not None
        return self.match

    def calculate_paint_rect(self, left_x):
        rect = QRect(self.margin_h + left_x, 0, self.checkbox_width, self.visual_rect.height())
        return rect if self.match else none_rect

    def paint_rect(self, rect):
        # 画复选框
        opt = QStyleOptionButton()
        opt.rect = rect
        opt.state = QStyle.State_Enabled | QStyle.State_Active
        if self.check_state == Qt.Unchecked:
            opt.state |= QStyle.State_Off
        elif self.check_state == Qt.PartiallyChecked:
            opt.state |= QStyle.State_NoChange
        elif self.check_state == Qt.Checked:
            opt.state |= QStyle.State_On
        self.style.drawControl(QStyle.CE_CheckBox, opt, self.painter)


class IconItemPainter(ItemPainterABC):

    def __init__(self, item, margin_h, style, painter, visual_rect, parent):
        super().__init__(item, margin_h, style, painter, visual_rect)
        self.parent = parent
        # 如果指定了icon大小，取该值，否则用默认值
        if self.parent.iconSize().isValid():
            self.icon_width = self.parent.iconSize().width()
        else:
            self.icon_width = style.pixelMetric(QStyle.PM_ListViewIconSize)
        self.icon = get_item_icon(item)

    def match_type(self) -> bool:
        self.match = not self.icon.isNull()
        return self.match

    def calculate_paint_rect(self, left_x):
        # 如果在图标部件前有其他部件，左边距有两个，否则计算一个即可
        margin_h = self.margin_h << 1 if left_x else self.margin_h
        return QRect(margin_h + 1 + left_x, 0, self.icon_width, self.visual_rect.height())

    def paint_rect(self, rect):
        self.icon.paint(self.painter, rect, Qt.AlignVCenter | Qt.AlignLeft)


class TextItemPainter(ItemPainterABC):

    def __init__(self, item_text, selected_flag, search_flag, search_item_records, *args):
        super().__init__(*args)
        self.item_text = item_text
        self.selected_flag = selected_flag
        self.search_flag = search_flag
        self.search_item_records = search_item_records

    def match_type(self) -> bool:
        # item必须有文本
        return True

    def get_text_rect_x(self, left_x):
        return self.margin_h + left_x + 1 if left_x else self.margin_h + left_x

    def calculate_paint_rect(self, left_x):
        h = self.painter.fontMetrics().height()
        y = (self.visual_rect.height() - h) / 2
        return QRectF(self.get_text_rect_x(left_x), y,
                      self.visual_rect.width() - left_x, h)

    def paint_rect(self, rect):
        if self.search_flag:
            self.draw_highlight_text(rect)
        else:
            self.draw_normal_text(rect)

    def draw_normal_text(self, rect):
        self.painter.drawText(rect, self.item_text)

    def draw_highlight_text(self, text_rect):
        # 获取当前painter像素
        font_metrics = self.painter.fontMetrics()
        start = 0
        text_rect_x = text_rect.x()
        text_rect_width = 0
        for search_idx in self.search_item_records:
            # 保存当前的painter
            self.painter.save()
            # 找到搜索的文本在原文本中的位置
            char_start_idx, char_end_idx = search_idx

            # 左边的文本
            left_text = self.item_text[start: char_start_idx]
            # 左边像素宽度
            left_text_width = font_metrics.width(left_text)
            # 找到左边字符的rect
            left_rect = QRectF(text_rect_x, text_rect.y(), left_text_width + 1, text_rect.height())

            # 搜索文本
            current_search_text = self.item_text[char_start_idx: char_end_idx + 1] \
                if char_end_idx < len(self.item_text) - 1 else self.item_text[char_start_idx:]
            # 获取搜索文本的像素宽度
            search_text_width = font_metrics.width(current_search_text)
            # 找到当前字符的rect
            search_rect = QRectF(text_rect_x + left_text_width,
                                 text_rect.y(),
                                 search_text_width + 1,
                                 text_rect.height())

            start = char_end_idx + 1
            text_rect_x += left_text_width + search_text_width
            text_rect_width += left_text_width + search_text_width

            # 如果左边有字符
            if left_text:
                self.painter.drawText(left_rect, left_text)
            # 处理当前搜索的字符
            self.painter.setPen(Qt.white)
            # 背景色设置为橙红色
            self.painter.setBackground(QBrush(QColor(255, 69, 0)))
            # 不透明模式OpaqueMode，默认为透明
            self.painter.setBackgroundMode(Qt.OpaqueMode)
            self.painter.drawText(search_rect, current_search_text)
            # 弹出保存的painter
            self.painter.restore()

        # 最后处理最右边的字符，如果匹配到的最后一个不是文本的最后，再进行处理，否则直接结束
        rest_start_idx = self.search_item_records[-1][-1]
        if rest_start_idx < len(self.item_text) - 1:
            # 计算右边的rect
            right_rect = QRectF(text_rect_x, text_rect.y(),
                                text_rect.width() - text_rect_width, text_rect.height())
            self.painter.drawText(right_rect, self.item_text[rest_start_idx + 1:])
