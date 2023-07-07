# -*- coding: utf-8 -*-
"""
自定义滚动区域部件，进入控件区域时显示滚动条，离开时隐藏
"""
import re

from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QAbstractScrollArea, QPlainTextEdit, QAbstractItemView, QScrollArea, QFrame, QTextBrowser

_author_ = 'luwt'
_date_ = '2022/5/7 17:18'


class ScrollableWidget(QAbstractScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)
        if hasattr(self, 'setVerticalScrollMode'):
            # 按像素滚动
            self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
            self.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
            # 如果是按下 shift 键进行鼠标滚轮滚动，执行水平滚动
            scroll_value = 10 if event.angleDelta().y() < 0 else -10
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + scroll_value)
        else:
            super().wheelEvent(event)

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


class ScrollArea(QScrollArea, ScrollableWidget):

    def __init__(self, *args):
        super().__init__(*args)
        # 去除边框
        self.setFrameShape(QFrame.Shape.NoFrame)
        # 设置可以调节控件大小
        self.setWidgetResizable(True)
        # 垂直滚动条策略
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def set_canvas_widget(self, canvas_widget):
        """设置画布部件，滚动区域的原理为：在画布之上进行滚动，像用放大镜看画布一样"""
        self.setWidget(canvas_widget)

    def wheelEvent(self, e: QtGui.QWheelEvent):
        """如果当前按键为 ctrl + 滚轮，那么跳过，否则会导致滚动和缩放一起进行"""
        if e.modifiers() == Qt.KeyboardModifier.ControlModifier:
            ...
        else:
            ScrollableWidget.wheelEvent(self, e)


class ScrollableZoomWidget(ScrollableWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLineWrapMode(self.LineWrapMode.NoWrap)

    def wheelEvent(self, e: QtGui.QWheelEvent):
        """实现ctrl + 滚轮缩放功能"""
        if e.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if e.angleDelta().y() > 0:
                # 放大
                self.zoomIn()
            else:
                self.zoomOut()
        else:
            ScrollableWidget.wheelEvent(self, e)


class ScrollableTextEdit(QPlainTextEdit, ScrollableZoomWidget):
    blank_pattern = r'\s+'

    def keyPressEvent(self, e):
        # 按下tab键，设置四个空格位
        tc = self.textCursor()
        if e.key() == Qt.Key.Key_Tab:
            tc.insertText("    ")
            return
        elif e.key() == Qt.Key.Key_Backspace:
            # 当前行文本
            current_text = tc.block().text()
            # 找到光标位置
            cursor_pos = tc.positionInBlock()
            # 截取光标左侧文本，匹配光标和文本之间空白数量
            cursor_left_text = current_text[: cursor_pos]
            # 如果左边第一个字符就是空白，那么进行下面处理
            if cursor_pos > 0 and not cursor_left_text[cursor_pos - 1].strip():
                left_blank_list = re.findall(self.blank_pattern, cursor_left_text)
                if left_blank_list:
                    nearest_blank = left_blank_list[-1]
                    # 如果空白数是4的倍数，那么一次移除4个空格，否则每次移除一个空格
                    if len(nearest_blank) and len(nearest_blank) % 4 == 0:
                        # 删除4个空白
                        for i in range(4):
                            tc.deletePreviousChar()
                        return
        elif e.modifiers() == Qt.KeyboardModifier.ShiftModifier and e.key() == Qt.Key.Key_Return:
            # 将光标移动到末位
            tc.movePosition(QTextCursor.MoveOperation.EndOfBlock)
            # 新起一行
            tc.insertBlock()
            # 移动光标，需要重新设置光标
            self.setTextCursor(tc)
            return
        super().keyPressEvent(e)
        # 因为拦截了按键事件，所以需要再手动调用滚动部件的按键事件，实现shift 滚轮水平滚动
        ScrollableZoomWidget.keyPressEvent(self, e)


class ScrollableTextBrowser(QTextBrowser, ScrollableZoomWidget):
    ...
