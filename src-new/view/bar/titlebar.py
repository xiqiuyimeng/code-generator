# -*- coding: utf-8 -*-
"""
自定义标题栏，实现扁平化效果，标题栏沉浸效果
"""
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QSizePolicy, QPushButton, QHBoxLayout

from view.custom_widget.draggable_widget import DraggableWidget

_author_ = 'luwt'
_date_ = '2022/5/7 16:37'


class TitleBar(DraggableWidget):

    def __init__(self, title_height, parent, menu_bar):
        super().__init__(parent)
        self.parent = parent
        # 沉浸式标题栏，和菜单栏在同一水平线
        self.menu_bar = menu_bar
        self.title_height = title_height
        self.button_height = title_height * 0.8
        self.setFixedHeight(title_height << 1)
        self.icon = QLabel()
        self.icon.setPixmap(QPixmap(":/icon/exec.png").scaled(self.title_height, self.title_height))
        # 标题栏文字
        self.main_title = QLabel("代码生成器")
        self.main_title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.main_title.setFixedHeight(self.title_height)
        self.main_title.setObjectName("main_title")
        # 最小化按钮
        self.min_button = QPushButton()
        self.min_button.setFixedSize(QSize(self.button_height, self.button_height))
        self.min_button.setObjectName("min_button")
        # 最大化按钮
        self.max_button = QPushButton()
        self.max_button.setFixedSize(QSize(self.button_height, self.button_height))
        self.max_button.setObjectName("max_button")
        # 还原窗口按钮
        self.restore_button = QPushButton()
        self.restore_button.setFixedSize(QSize(self.button_height, self.button_height))
        self.restore_button.setObjectName("restore_button")
        self.restore_button.setVisible(False)
        # 关闭按钮
        self.close_button = QPushButton()
        self.close_button.setFixedSize(QSize(self.button_height, self.button_height))
        self.close_button.setObjectName("close_button")
        # 标题栏的布局
        self.title_layout = QHBoxLayout()
        # 将各个控件依次添加到布局中
        self.title_layout.addWidget(self.icon)
        # 实现沉浸式标题栏，将菜单栏融入到当前布局
        self.title_layout.addWidget(self.menu_bar)
        self.title_layout.addWidget(self.main_title)
        self.title_layout.addWidget(self.min_button)
        self.title_layout.addWidget(self.max_button)
        self.title_layout.addWidget(self.restore_button)
        self.title_layout.addWidget(self.close_button)
        self.setLayout(self.title_layout)
        # 菜单栏宽度根据实际内容来定，不占用过多空白空间
        self.menu_bar.setFixedWidth(self.menu_bar.sizeHint().width())
        self.menu_bar.setFixedHeight(self.menu_bar.sizeHint().height())

        self.min_button.clicked.connect(self.parent.showMinimized)
        self.max_button.clicked.connect(self.max_window)
        self.restore_button.clicked.connect(self.restore_window)
        self.close_button.clicked.connect(self.parent.close)

    def max_window(self):
        """窗口最大化"""
        self.parent.showFullScreen()
        self.restore_button.setVisible(True)
        self.max_button.setVisible(False)
        self.parent.title_bar.setFixedWidth(self.parent.width())

    def restore_window(self):
        """窗口还原"""
        self.parent.setWindowState(Qt.WindowNoState)
        self.restore_button.setVisible(False)
        self.max_button.setVisible(True)
        self.parent.title_bar.setFixedWidth(self.parent.width())
