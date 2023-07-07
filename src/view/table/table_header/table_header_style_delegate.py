# -*- coding: utf-8 -*-
from PyQt6.QtCore import QModelIndex
from PyQt6.QtGui import QPainter, QColor, QBrush
from PyQt6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem

_author_ = 'luwt'
_date_ = '2023/3/2 18:09'


class TableHeaderStyleDelegate(QStyledItemDelegate):

    def paint(self, painter: QPainter, option: 'QStyleOptionViewItem', index: QModelIndex):
        # 绘制背景
        color = QColor(231, 238, 251)
        painter.setPen(color)
        painter.setBrush(QBrush(color))
        painter.drawRect(option.rect)
        super().paint(painter, option, index)


class ColTypeMappingTableHeaderStyleDelegate(QStyledItemDelegate):

    def paint(self, painter: QPainter, option: 'QStyleOptionViewItem', index: QModelIndex):
        col_idx = index.column()
        # 前两列为单行
        if col_idx <= 1:
            color = QColor(231, 238, 251)
        else:
            # 去除前面两列，后面每三列为一组
            # 组索引为奇偶数时，分开处理颜色
            if ((col_idx - 2) // 3) & 1:
                # 奇数时的颜色
                color = QColor(214, 228, 253)
            else:
                # 偶数时的颜色
                color = QColor(203, 221, 255)
        painter.setPen(color)
        painter.setBrush(QBrush(color))
        painter.drawRect(option.rect)
        super().paint(painter, option, index)
