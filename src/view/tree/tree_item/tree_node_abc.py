# -*- coding: utf-8 -*-
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QTreeWidgetItem

from src.enum.icon_enum import get_icon
from src.constant.tree_constant import CLOSE_REFRESHING_NODE_PROMPT, CLOSE_REFRESHING_CHILD_NODE_PROMPT, \
    CLOSE_OPENING_CHILD_NODE_PROMPT
from src.view.tab.tab_ui import TabTableUI
from src.view.tree.tree_item.tree_item_func import set_item_opened_tab, get_item_opened_tab, get_add_del_data, \
    get_item_opened_record
from src.view.window.main_window_func import get_window

_author_ = 'luwt'
_date_ = '2022/12/2 11:36'


class TreeNodeABC:

    def __new__(cls, item: QTreeWidgetItem, tree_widget):
        if not hasattr(item, 'tree_node'):
            item.tree_node = object.__new__(cls)
        return item.tree_node

    def __init__(self, item: QTreeWidgetItem, tree_widget):
        self.item = item
        self.item_name = self.item.text(0)
        self.tree_widget = tree_widget
        self.window = get_window()
        self.is_opening = False
        # 记录当前节点下一层，正在打开的节点数量
        self.opening_child_count = 0
        self.is_refreshing = False
        # 只记录当前节点下一层，正在刷新的子节点数量，不关心子节点下有多少节点刷新
        self.refreshing_child_count = 0

    def open_item_fail(self):
        self.is_opening = False
        parent_item = self.item.parent()
        if parent_item:
            self.tree_widget.get_item_node(parent_item).sub_opening_child_count()

    def reopen_tab(self, table_tab, tab_name, check_state_func):
        # 创建tab页
        tab = TabTableUI(self.window, table_tab, self.item, self.tree_widget)
        self.tree_widget.get_current_tab_widget().addTab(tab, tab_name)
        # 记录tab对象
        set_item_opened_tab(self.item, tab)
        # 连接表头复选框变化信号
        tab.table_frame.table_widget.table_header.header_check_changed.connect(
            lambda check_state: check_state_func(check_state))
        return tab

    def add_opening_child_count(self):
        # 如果当前节点的正在打开子节点数为0，那么需要向上传递打开节点数变化
        self.opening_child_count += 1
        if self.opening_child_count == 1:
            parent_item = self.item.parent()
            if parent_item:
                self.tree_widget.get_item_node(parent_item).add_opening_child_count()

    def sub_opening_child_count(self):
        # 如果当前节点的正在打开子节点数为1，那么需要向上传递打开节点数变化
        self.opening_child_count -= 1
        if self.opening_child_count == 0:
            parent_item = self.item.parent()
            if parent_item:
                self.tree_widget.get_item_node(parent_item).sub_opening_child_count()

    def refresh_item_tab(self, table_tab, check_state_func):
        if table_tab:
            # 开始刷新tab页面
            tab = get_item_opened_tab(self.item)
            if tab:
                tab.refresh_ui(table_tab)
                # 连接表头复选框变化信号
                tab.table_frame.table_widget.table_header.header_check_changed.connect(
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

    def not_allow_operate_prompt(self):
        # 当前节点正在刷新中、子节点处于刷新中、子节点处于打开中，都不允许操作当前节点
        if self.is_refreshing:
            return CLOSE_REFRESHING_NODE_PROMPT
        elif self.refreshing_child_count:
            return CLOSE_REFRESHING_CHILD_NODE_PROMPT
        elif self.opening_child_count:
            return CLOSE_OPENING_CHILD_NODE_PROMPT

    def add_open_close_table_menu(self, open_table_action_text, close_table_action_text, menu):
        open_table_action = open_table_action_text \
            if not get_item_opened_tab(self.item) else close_table_action_text
        self.add_menu(open_table_action, menu)

    def add_cancel_open_refresh_menu(self, cancel_open_action_text, cancel_refresh_action_text, menu):
        # 如果正在打开，只显示取消打开
        if self.is_opening:
            self.add_menu(cancel_open_action_text, menu)
            return True
        # 如果正在刷新，只显示取消刷新菜单
        if self.is_refreshing:
            self.add_menu(cancel_refresh_action_text, menu)
            return True

    def add_refresh_menu(self, refresh_action_text, menu):
        # 刷新
        menu.addSeparator()
        self.add_menu(refresh_action_text, menu)

    def add_menu(self, action_text, menu, with_item_name=True):
        action_display_text = action_text.format(self.item_name) if with_item_name else action_text
        menu.addAction(QAction(get_icon(action_text), action_display_text, menu))

    def get_need_reorder_item_records(self):
        """当前节点之后的节点需要调整顺序"""
        # 当前节点不是顶层节点，确定节点同级别项目数，获取同级别项目的方法
        if self.item.parent():
            item_count = self.item.parent().childCount()
            item_idx = self.item.parent().indexOfChild(self.item)
            get_item_by_idx_func = self.item.parent().child
        else:
            item_count = self.tree_widget.topLevelItemCount()
            item_idx = self.tree_widget.indexOfTopLevelItem(self.item)
            get_item_by_idx_func = self.tree_widget.topLevelItem

        # 对于需要排序的节点，是在当前节点之后，也就是索引大于当前节点
        reorder_opened_item_records = list()
        for idx in range(item_idx + 1, item_count):
            item = get_item_by_idx_func(idx)
            opened_record = get_item_opened_record(item)
            opened_record.item_order -= 1
            reorder_opened_item_records.append(opened_record)
        return reorder_opened_item_records

    def open_item(self):
        ...

    def open_item_ui(self, *args):
        ...

    def reopen_item(self, opened_items):
        ...

    def close_item(self):
        ...

    def change_check_box(self, check_state, clicked) -> bool:
        ...

    def hide_check_box(self):
        ...

    def show_check_box(self):
        ...

    def do_fill_menu(self, menu):
        ...

    def handle_menu_func(self, func):
        ...

    def refresh(self):
        ...

    def refresh_success(self, *args):
        ...

    def refresh_fail(self):
        ...

    def worker_terminate(self):
        ...
