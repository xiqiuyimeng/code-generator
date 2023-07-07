# -*- coding: utf-8 -*-
"""
可拖动小部件通用实现，实现部件根随鼠标拖动
"""
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QWidget, QDialog

_author_ = 'luwt'
_date_ = '2022/5/7 15:58'


class DraggableWidgetABC(QWidget):

    def __init__(self, parent=None):
        self.parent = parent
        # 是否移动中标志位
        self.is_moving = False
        # 鼠标开始的坐标
        self.mouse_start_pos = ...
        # 窗口开始的坐标
        self.window_start_pos = ...
        super().__init__(parent)

    def mousePressEvent(self, event: QMouseEvent):
        # 如果按下了鼠标左键，将标志位设置为true
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_moving = True
            # 记录当前鼠标位置坐标
            self.mouse_start_pos = event.globalPosition()
            self.window_start_pos = self.get_window_start_pos()

    def mouseMoveEvent(self, event):
        if hasattr(self, "is_moving") and self.is_moving:
            # 移动距离 = 移动后的鼠标位置坐标 - 初始（类型都是QPointF，是可以直接做运算，窗口处同理）
            move_distance = event.globalPosition() - self.mouse_start_pos
            # 转化为 QPoint
            self.do_move(move_distance.toPoint())

    def mouseReleaseEvent(self, event):
        if hasattr(self, "is_moving"):
            # 鼠标按键松开，恢复标志位
            self.is_moving = False

    def get_window_start_pos(self):
        ...

    def do_move(self, move_distance):
        ...


class DraggableWidget(DraggableWidgetABC):

    def __init__(self, parent):
        super().__init__(parent)

    def get_window_start_pos(self):
        # 记录当前主窗口位置坐标
        return self.parent.frameGeometry().topLeft()

    def do_move(self, move_distance):
        # 将主窗口也移动
        self.parent.move(self.window_start_pos + move_distance)


class DraggableDialog(QDialog, DraggableWidgetABC):

    def __init__(self):
        self.start_animation: QPropertyAnimation = ...
        self.close_animation: QPropertyAnimation = ...
        super().__init__()

        self.set_start_animation()
        self.set_close_animation()

    def set_start_animation(self):
        # 初始设置窗口透明度为0
        self.setWindowOpacity(0)
        # 创建渐入动画
        self.start_animation = QPropertyAnimation(self, b"windowOpacity")
        # 动画持续时间为200毫秒
        self.start_animation.setDuration(200)
        # 动画初始值为0，即完全透明
        self.start_animation.setStartValue(0)
        # 动画结束值为1，即完全不透明
        self.start_animation.setEndValue(1)
        # 使用缓动函数，减速曲线效果
        self.start_animation.setEasingCurve(QEasingCurve.Type.OutQuad)

    def set_close_animation(self):
        # 创建淡出动画
        self.close_animation = QPropertyAnimation(self, b"windowOpacity")
        # 动画持续时间为200毫秒
        self.close_animation.setDuration(200)
        # 动画初始值为1，即完全不透明
        self.close_animation.setStartValue(1)
        # 动画结束值为0，即完全透明
        self.close_animation.setEndValue(0)
        # 使用缓动函数，加速曲线效果
        self.close_animation.setEasingCurve(QEasingCurve.Type.InQuad)

    def start_close_animation(self):
        self.close_animation.start()

    def showEvent(self, event):
        # 启动动画
        self.start_animation.start()

    def get_window_start_pos(self):
        # 记录当前窗口位置坐标
        return self.frameGeometry().topLeft()

    def do_move(self, move_distance):
        # 将窗口移动
        self.move(self.window_start_pos + move_distance)
