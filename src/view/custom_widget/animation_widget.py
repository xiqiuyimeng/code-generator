# -*- coding: utf-8 -*-
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import QWidget

_author_ = 'luwt'
_date_ = '2023/8/14 9:03'


class OpacityAnimationWidget(QWidget):

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
