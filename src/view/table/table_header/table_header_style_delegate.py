# -*- coding: utf-8 -*-
from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QPainter, QColor, QBrush, QLinearGradient
from PyQt5.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem

_author_ = 'luwt'
_date_ = '2023/3/2 18:09'


class TableHeaderStyleDelegate(QStyledItemDelegate):

    def paint(self, painter: QPainter, option: 'QStyleOptionViewItem', index: QModelIndex):
        # 绘制背景
        color = QColor(231, 238, 251)
        painter.setPen(color)
        painter.setBrush(QBrush(color))
        painter.drawRect(option.rect)

        # start_x = option.rect.right()
        # start_y = option.rect.y()
        # end_x = start_x + 2
        # end_y = start_y + option.rect.height()
        #
        # gradient = QLinearGradient(start_x, start_y, end_x, end_y)
        # gradient.setColorAt(0, QColor(164, 188, 240, 0))
        # gradient.setColorAt(0.5, QColor(164, 188, 240, 255))
        # gradient.setColorAt(1, QColor(164, 188, 240, 0))
        # painter.setBrush(gradient)
        # painter.drawRect(option.rect.right(), start_y, 0, option.rect.height())

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
