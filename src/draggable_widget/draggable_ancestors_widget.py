# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QToolBar

_author_ = 'luwt'
_date_ = '2020/10/19 11:04'


class DragWindowWidget(QWidget):

    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)

    def mousePressEvent(self, event):
        # 如果按下了鼠标左键，将标志位设置为true
        if event.button() == Qt.LeftButton:
            self.is_moving = True
            # 记录当前鼠标位置坐标
            self.mouse_start_pos = event.globalPos()
            # 记录当前窗口位置坐标
            self.window_start_pos = self.parent.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if hasattr(self, "is_moving") and self.is_moving:
            # 移动距离 = 移动后的鼠标位置坐标 - 初始（类型都是QPoint，是可以直接做运算，窗口处同理）
            move_distance = event.globalPos() - self.mouse_start_pos
            # 将主窗口也移动
            self.parent.move(self.window_start_pos + move_distance)

    def mouseReleaseEvent(self, event):
        if hasattr(self, "is_moving"):
            # 鼠标按键松开，恢复标志位
            self.is_moving = False


class DragWindowToolBar(QToolBar, DragWindowWidget): ...
