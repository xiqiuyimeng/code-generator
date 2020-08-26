# -*- coding: utf-8 -*-
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QMovie, QMoveEvent
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout

_author_ = 'luwt'
_date_ = '2020/8/17 16:26'


class LoadingMask(QWidget):

    def __init__(self, parent, gif):
        super().__init__(parent)
        parent.installEventFilter(self)
        self.set_size()
        self.label = QLabel()

        self.movie = QMovie(gif)
        self.label.setMovie(self.movie)
        self.label.setScaledContents(True)
        self.movie.start()

        layout = QHBoxLayout(self)
        layout.addWidget(self.label)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setWindowOpacity(0.8)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

    def eventFilter(self, widget, event):
        """过滤移动事件，让遮罩层跟随父窗口移动"""
        if widget == self.parent() and type(event) == QMoveEvent:
            self.move_with_parent()
            # 返回true，说明事件已处理，其他控件不会再处理
            return True
        # 交由其他控件处理
        return super().eventFilter(widget, event)

    def move_with_parent(self):
        """跟随父窗口移动，大小跟随父窗口大小"""
        self.move(self.parent().geometry().x(), self.parent().geometry().y())
        self.set_size()

    def set_size(self):
        self.setFixedSize(QSize(self.parent().geometry().width(),
                                self.parent().geometry().height()))



