# -*- coding: utf-8 -*-
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QAbstractItemView, QMenu, QFrame

from src.view.custom_widget.scrollable_widget import ScrollableWidget

_author_ = 'luwt'
_date_ = '2023/2/13 15:38'


class AbstractItemView(QAbstractItemView, ScrollableWidget):

    def __init__(self, parent):
        super().__init__(parent)
        # 设置接受拖入
        self.setAcceptDrops(True)
        # 设置开启拖拽
        self.setDragEnabled(True)
        # 设置无边框
        self.setFrameShape(QFrame.NoFrame)
        # 统一设置图标大小
        self.setIconSize(QSize(40, 30))

        self.connect_signal()

    def keyPressEvent(self, e) -> None:
        # 传递调用
        super().keyPressEvent(e)
        ScrollableWidget.keyPressEvent(self, e)

    def connect_signal(self):
        # 右击事件
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.handle_right_mouse_clicked)

    def handle_right_mouse_clicked(self, pos):
        # 获取当前元素，只有在元素上才显示菜单
        item = self.itemAt(pos)
        if item:
            # 生成右键菜单
            menu = QMenu()
            # 填充右键菜单内容
            self.fill_menu(item, menu)
            # 右键菜单点击事件
            menu.triggered.connect(self.right_menu_func)
            # 右键菜单弹出位置跟随焦点位置
            menu.exec_(QCursor.pos())

    def fill_menu(self, item, menu): ...

    def right_menu_func(self, action):
        """
        点击右键菜单选项后触发事件
        :param action: 右键菜单中的选项
        """
        # 获取右键点击的项
        item = self.currentItem()
        action_text = action.text()
        self.do_right_menu_func(item, action_text)

    def do_right_menu_func(self, item, action_text): ...
