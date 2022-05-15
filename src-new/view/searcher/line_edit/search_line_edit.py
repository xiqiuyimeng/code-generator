# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QLineEdit

_author_ = 'luwt'
_date_ = '2022/5/9 19:00'


class SearcherLineEdit(QLineEdit):

    def __init__(self):
        super().__init__()
        self.right_palette = self.palette()
        self.textChanged.connect(self.set_size)

    def sub_text(self):
        if self.text():
            self.setText(self.text()[:-1])

    def paint_wrong_color(self):
        wrong_palette = QPalette()
        wrong_palette.setColor(QPalette.Text, Qt.red)
        self.setPalette(wrong_palette)

    def paint_right_color(self):
        self.setPalette(self.right_palette)

    def set_size(self):
        self.setFixedSize(self.sizeHint())

    def sizeHint(self):
        return QSize(self.fontMetrics().width(self.text()) + self.fontMetrics().maxWidth(),
                     self.fontMetrics().height() + self.fontMetrics().descent())
