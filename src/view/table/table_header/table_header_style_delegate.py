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
