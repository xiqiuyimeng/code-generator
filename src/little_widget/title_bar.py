# -*- coding: utf-8 -*-
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel, QSizePolicy

_author_ = 'luwt'
_date_ = '2020/8/27 17:15'

# 按钮高度
BUTTON_HEIGHT = 30
# 按钮宽度
BUTTON_WIDTH = 30
# 标题栏高度
TITLE_HEIGHT = 30


class TitleBar(QWidget):
    """自定义标题栏"""

    def __init__(self):
        super().__init__()
        # self.setStyleSheet("background-color:blue")
        titleIcon = QPixmap(":/icon/exec.png")
        Icon = QLabel()
        Icon.setPixmap(titleIcon.scaled(25, 25))
        titleContent = QLabel("标题内容")
        titleContent.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        titleContent.setFixedHeight(TITLE_HEIGHT)
        titleContent.setObjectName("TitleContent")
        self.ButtonMin = QPushButton()
        self.ButtonMin.setFixedSize(QSize(BUTTON_WIDTH, BUTTON_HEIGHT))
        self.ButtonMin.setObjectName("ButtonMin")
        self.ButtonMax = QPushButton()
        self.ButtonMax.setFixedSize(QSize(BUTTON_WIDTH, BUTTON_HEIGHT))
        self.ButtonMax.setObjectName("ButtonMax")
        self.ButtonRestore = QPushButton()
        self.ButtonRestore.setFixedSize(QSize(BUTTON_WIDTH, BUTTON_HEIGHT))
        self.ButtonRestore.setObjectName("ButtonRestore")
        self.ButtonRestore.setVisible(False)
        self.ButtonClose = QPushButton()
        self.ButtonClose.setFixedSize(QSize(BUTTON_WIDTH, BUTTON_HEIGHT))
        self.ButtonClose.setObjectName("ButtonClose")
        mylayout = QHBoxLayout()
        mylayout.setSpacing(0)
        mylayout.setContentsMargins(0, 0, 0, 0)
        mylayout.addWidget(Icon)

        mylayout.addWidget(titleContent)
        mylayout.addWidget(self.ButtonMin)
        mylayout.addWidget(self.ButtonMax)
        mylayout.addWidget(self.ButtonRestore)
        mylayout.addWidget(self.ButtonClose)
        self.setLayout(mylayout)

