# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel, QSizePolicy

_author_ = 'luwt'
_date_ = '2020/8/27 17:15'


class TitleBar(QWidget):
    """自定义标题栏"""

    def __init__(self, title_height, parent):
        super().__init__()
        self.parent = parent
        self.title_height = title_height
        self.icon = QLabel()
        self.icon.setPixmap(QPixmap(":/icon/exec.png").scaled(self.title_height, self.title_height))
        # 标题栏文字
        self.main_title = QLabel("代码生成器")
        self.main_title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.main_title.setFixedHeight(self.title_height)
        self.main_title.setObjectName("main_title")
        # 最小化按钮
        self.min_button = QPushButton()
        self.min_button.resize(QSize(self.title_height, self.title_height))
        self.min_button.setObjectName("min_button")
        self.min_button.setText("最小化")
        # 最大化按钮
        self.max_button = QPushButton()
        self.max_button.resize(QSize(self.title_height, self.title_height))
        self.max_button.setObjectName("max_button")
        self.max_button.setText("最大化")
        # 还原窗口按钮
        self.restore_button = QPushButton()
        self.restore_button.resize(QSize(self.title_height, self.title_height))
        self.restore_button.setObjectName("restore_button")
        self.restore_button.setText("还原")
        self.restore_button.setVisible(False)
        # 关闭按钮
        self.close_button = QPushButton()
        self.close_button.resize(QSize(self.title_height, self.title_height))
        self.close_button.setIcon(QIcon(":/icon/wrong.png"))
        self.close_button.setObjectName("close_button")
        # 标题栏的布局
        self.title_layout = QHBoxLayout()
        self.title_layout.setSpacing(0)
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        # 将各个控件依次添加到布局中
        self.title_layout.addWidget(self.icon)
        self.title_layout.addWidget(self.main_title)
        self.title_layout.addWidget(self.min_button)
        self.title_layout.addWidget(self.max_button)
        self.title_layout.addWidget(self.restore_button)
        self.title_layout.addWidget(self.close_button)
        self.setLayout(self.title_layout)

        self.min_button.clicked.connect(lambda: self.parent.setWindowState(Qt.WindowMinimized))
        self.max_button.clicked.connect(self.max_window)
        self.restore_button.clicked.connect(self.restore_window)
        self.close_button.clicked.connect(self.parent.close)

    @QtCore.pyqtSlot()
    def max_window(self):
        """窗口最大化"""
        self.parent.setWindowState(Qt.WindowMaximized)
        self.restore_button.setVisible(True)
        self.max_button.setVisible(False)
        self.parent.title_bar.setFixedWidth(self.parent.width())

    @QtCore.pyqtSlot()
    def restore_window(self):
        """窗口还原"""
        self.parent.setWindowState(Qt.WindowNoState)
        self.restore_button.setVisible(False)
        self.max_button.setVisible(True)
        self.parent.title_bar.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event):
        # 如果按下了鼠标左键，将标志位设置为true
        if event.button() == Qt.LeftButton:
            self.is_moving = True
            # 记录当前鼠标位置坐标
            self.mouse_start_pos = event.globalPos()
            # 记录当前窗口位置坐标
            self.window_start_pos = self.parent.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self.is_moving:
            # 移动距离 = 移动后的鼠标位置坐标 - 初始（类型都是QPoint，是可以直接做运算，窗口处同理）
            move_distance = event.globalPos() - self.mouse_start_pos
            # 将主窗口也移动
            self.parent.move(self.window_start_pos + move_distance)

    def mouseReleaseEvent(self, event):
        # 鼠标按键松开，恢复标志位
        self.is_moving = False
