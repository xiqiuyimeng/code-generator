# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

_author_ = 'luwt'
_date_ = '2020/8/27 10:38'


class DraggableDialog(QDialog):
    """可拖动的对话框，自定义实现鼠标单击拖动窗口效果"""

    def mousePressEvent(self, event):
        # 如果按下了鼠标左键，将标志位设置为true
        if event.button() == Qt.LeftButton:
            self.is_moving = True
            # 记录当前鼠标位置坐标
            self.mouse_start_pos = event.globalPos()
            # 记录当前窗口位置坐标
            self.window_start_pos = self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if hasattr(self, "is_moving") and self.is_moving:
            # 移动距离 = 移动后的鼠标位置坐标 - 初始（类型都是QPoint，是可以直接做运算，窗口处同理）
            move_distance = event.globalPos() - self.mouse_start_pos
            # 将窗口也移动
            self.move(self.window_start_pos + move_distance)

    def mouseReleaseEvent(self, event):
        if hasattr(self, "is_moving"):
            # 鼠标按键松开，恢复标志位
            self.is_moving = False
