# -*- coding: utf-8 -*-
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QCursor, QDropEvent
from PyQt5.QtWidgets import QAbstractItemView, QMenu, QFrame, QTreeWidget, QListWidget, QListWidgetItem, QTreeWidgetItem

from src.view.custom_widget.scrollable_widget import ScrollableWidget

_author_ = 'luwt'
_date_ = '2023/2/13 15:38'


class ItemViewABC(QAbstractItemView, ScrollableWidget):

    def __init__(self, parent):
        super().__init__(parent)
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


class DraggableItemViewABC(ItemViewABC):

    def __init__(self, *args):
        super().__init__(*args)
        # 设置接受拖入
        self.setAcceptDrops(True)
        # 设置开启拖拽
        self.setDragEnabled(True)

    def dropEvent(self, event: QDropEvent):
        """重写，实现拖拽效果"""
        # 获取拖入事件的坐标
        pos = event.pos()
        # 获取当前坐标下的item
        current_item = self.itemAt(pos)

        # 获取拖入item的父组件
        source_widget = event.source()
        # 获取所有拖入item
        source_items = source_widget.selectedItems()
        # 当前允许单选就可以了，这样减少其他地方的复杂度
        for source_item in source_items:
            # 对于树的顶层节点，应该忽略
            if isinstance(source_item, QTreeWidgetItem) and not source_item.parent():
                continue
            # 移除之前的项
            self.remove_source_item(source_widget, source_item)
            # 插入到当前位置
            self.insert_item(source_item, current_item)

    def remove_source_item(self, source_widget, source_item):
        # 判断源控件是列表控件还是树控件
        if isinstance(source_widget, QListWidget):
            self.deal_source_list_item_data(source_item)
            source_widget.takeItem(source_widget.indexFromItem(source_item).row())
        elif isinstance(source_widget, QTreeWidget):
            self.deal_source_tree_item_data(source_item)
            source_item.parent().removeChild(source_item)

    def deal_source_list_item_data(self, source_item): ...

    def deal_source_tree_item_data(self, source_item): ...

    def insert_item(self, source_item, current_item):
        if isinstance(self, QListWidget):
            # 获取该item的index
            current_index = self.indexFromItem(current_item)
            # 获取行数，如果索引有效的话，根据索引获取，否则应该在最后
            current_row = current_index.row() if current_index.isValid() else self.count()
            # 插入到当前位置
            if isinstance(source_item, QListWidgetItem):
                self.deal_new_list_item_data(source_item, source_item)
                self.insertItem(current_row, source_item)
            elif isinstance(source_item, QTreeWidgetItem):
                new_list_item = QListWidgetItem(source_item.text(0))
                self.deal_new_list_item_data(source_item, new_list_item)
                self.insertItem(current_row, new_list_item)
        elif isinstance(self, QTreeWidget):
            # 先根据位置获取节点，如果获取不到，那么根据当前项获取
            if not current_item:
                current_item = self.currentItem()
                if not current_item:
                    return
            # 只有顶层节点，可以接收，如果不是顶层节点，那么寻找顶层节点
            top_item = get_tree_top_item(current_item)
            new_tree_item = QTreeWidgetItem(top_item)
            if isinstance(source_item, QListWidgetItem):
                new_tree_item.setText(0, source_item.text())
            elif isinstance(source_item, QTreeWidgetItem):
                new_tree_item.setText(0, source_item.text(0))
            top_item.setExpanded(True)
            self.deal_new_tree_item_data(source_item, new_tree_item)

    def deal_new_list_item_data(self, source_item, new_item): ...

    def deal_new_tree_item_data(self, source_item, new_item): ...


def get_tree_top_item(item):
    if item.parent():
        return get_tree_top_item(item.parent())
    return item
