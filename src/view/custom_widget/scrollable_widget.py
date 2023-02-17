# -*- coding: utf-8 -*-
"""
自定义滚动区域部件，进入控件区域时显示滚动条，离开时隐藏
"""
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractScrollArea, QPlainTextEdit

_author_ = 'luwt'
_date_ = '2022/5/7 17:18'


class ScrollableWidget(QAbstractScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)
        # 抓取键盘事件
        self.grabKeyboard()
        # 检测是否按下shift键
        self.press_shift = False

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if self.press_shift:
            # 如果是按下 shift 键进行鼠标滚轮滚动，执行水平滚动
            scroll_value = 10 if event.angleDelta().y() < 0 else -10
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + scroll_value)
        else:
            super().wheelEvent(event)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == Qt.Key_Shift:
            self.press_shift = True
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == Qt.Key_Shift:
            self.press_shift = False
        super().keyReleaseEvent(event)

    def enterEvent(self, event):
        """设置滚动条在进入控件区域的时候显示"""
        self.verticalScrollBar().setHidden(False)
        self.horizontalScrollBar().setHidden(False)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """设置滚动条在离开控件区域的时候隐藏"""
        self.verticalScrollBar().setHidden(True)
        self.horizontalScrollBar().setHidden(True)
        super().leaveEvent(event)


class ScrollableTextEdit(QPlainTextEdit, ScrollableWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.setLineWrapMode(self.NoWrap)

    def keyPressEvent(self, e):
        # 按下tab键，设置四个空格位
        if e.key() == Qt.Key_Tab:
            tc = self.textCursor()
            tc.insertText("    ")
            return
        super().keyPressEvent(e)
