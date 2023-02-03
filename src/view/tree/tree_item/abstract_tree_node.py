# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTreeWidgetItem

from view.tab.tab_ui import TabTableUI
from view.tree.tree_item.tree_item_func import set_item_opened_tab, get_item_opened_tab, \
    get_add_del_data

_author_ = 'luwt'
_date_ = '2022/12/2 11:36'


class AbstractTreeNode:

    def __new__(cls, item: QTreeWidgetItem, tree_widget, window):
        if not hasattr(item, 'tree_node'):
            item.tree_node = object.__new__(cls)
        return item.tree_node

    def __init__(self, item: QTreeWidgetItem, tree_widget, window):
        self.item = item
        self.tree_widget = tree_widget
        self.window = window
        self.is_refreshing = False
        # 只记录当前节点下一层，正在刷新的子节点数量，不关心子节点下有多少节点刷新
        self.refreshing_child_count = 0

    def reopen_tab(self, table_tab, tab_name, check_state_func):
        # 创建tab页
        tab = TabTableUI(self.window, table_tab, self.item, self.tree_widget)
        self.tree_widget.get_current_tab_widget().addTab(tab, tab_name)
        # 记录tab对象
        set_item_opened_tab(self.item, tab)
        # 连接表头复选框变化信号
        tab.table_frame.table_widget.table_header.header_check_state_changed.connect(
            lambda check_state: check_state_func(check_state))
        return tab

    def refresh_item_tab(self, table_tab, check_state_func):
        if table_tab:
            # 开始刷新tab页面
            tab = get_item_opened_tab(self.item)
            if tab:
                tab.refresh_ui(table_tab)
                # 连接表头复选框变化信号
                tab.table_frame.table_widget.table_header.header_check_state_changed.connect(
                    lambda check_state: check_state_func(check_state))
        # 清空选中数据
        del_data = get_add_del_data(self.item)
        self.tree_widget.tree_data.del_node(del_data)

    def add_refreshing_child_count(self):
        # 如果当前刷新子节点数为0，那么这次增加之后，需要传递给上层节点
        self.refreshing_child_count += 1
        if self.refreshing_child_count == 1:
            parent_item = self.item.parent()
            if parent_item:
                self.tree_widget.get_item_node(parent_item).add_refreshing_child_count()

    def sub_refreshing_child_count(self):
        # 如果当前刷新子节点数为1，那么这次增加之后，需要传递给上层节点
        self.refreshing_child_count -= 1
        # 如果当前节点正在刷新，提交数量变化，应由当前节点触发，而非子节点，否则会多次提交
        if self.is_refreshing:
            return
        if self.refreshing_child_count == 0:
            parent_item = self.item.parent()
            if parent_item:
                self.tree_widget.get_item_node(parent_item).sub_refreshing_child_count()

    def open_item(self): ...

    def open_item_ui(self, *args): ...

    def open_item_fail(self): ...

    def reopen_item(self, opened_items): ...

    def close_item(self): ...

    def change_check_box(self, check_state, clicked): ...

    def hide_check_box(self): ...

    def show_check_box(self): ...

    def do_fill_menu(self, menu): ...

    def handle_menu_func(self, func): ...

    def refresh(self): ...

    def refresh_success(self, *args): ...

    def refresh_fail(self): ...

    def worker_terminate(self): ...
