# -*- coding: utf-8 -*-
"""
自定义滚动区域部件，进入控件区域时显示滚动条，离开时隐藏
"""
import re

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QAbstractScrollArea, QPlainTextEdit, QAbstractItemView

_author_ = 'luwt'
_date_ = '2022/5/7 17:18'


class ScrollableWidget(QAbstractScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)
        if hasattr(self, 'setVerticalScrollMode'):
            # 按像素滚动
            self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
            self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
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
        # 当鼠标进入时，抓取键盘输入
        self.grabKeyboard()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """设置滚动条在离开控件区域的时候隐藏"""
        self.verticalScrollBar().setHidden(True)
        self.horizontalScrollBar().setHidden(True)
        # 当鼠标离开时，不再抓取键盘输入
        self.releaseKeyboard()
        super().leaveEvent(event)


class ScrollableTextEdit(QPlainTextEdit, ScrollableWidget):
    blank_pattern = r'\s+'

    def __init__(self, parent):
        super().__init__(parent)
        self.setLineWrapMode(self.NoWrap)

    def keyPressEvent(self, e):
        # 按下tab键，设置四个空格位
        tc = self.textCursor()
        if e.key() == Qt.Key_Tab:
            tc.insertText("    ")
            return
        elif e.key() == Qt.Key_Backspace:
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
                        [tc.deletePreviousChar() for i in range(4)]
                        return
        elif self.press_shift and e.key() == Qt.Key_Return:
            # 将光标移动到末位
            tc.movePosition(QTextCursor.EndOfBlock)
            # 新起一行
            tc.insertBlock()
            # 移动光标，需要重新设置光标
            self.setTextCursor(tc)
            return
        super().keyPressEvent(e)
        # 因为拦截了按键事件，所以需要再手动调用滚动部件的按键事件，实现shift 滚轮水平滚动
        ScrollableWidget.keyPressEvent(self, e)

    def wheelEvent(self, e: QtGui.QWheelEvent):
        """实现ctrl + 滚轮缩放功能"""
        if e.modifiers() == Qt.ControlModifier:
            if e.angleDelta().y() > 0:
                # 放大
                self.zoomIn()
            else:
                self.zoomOut()
        else:
            ScrollableWidget.wheelEvent(self, e)
