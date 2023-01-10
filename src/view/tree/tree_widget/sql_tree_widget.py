# -*- coding: utf-8 -*-
"""
sql数据源树结构
"""

from service.async_func.async_sql_conn_task import ListConnExecutor
from service.system_storage.opened_tree_item_sqlite import SqlTreeItemLevel
from service.util.tree_node import TreeData
from view.tab.tab_ui import TabTableUI
from view.tree.tree_item.context import get_sql_tree_node
from view.tree.tree_item.tree_item_func import get_item_opened_tab
from view.tree.tree_widget.abstract_tree_widget import AbstractTreeWidget
from view.tree.tree_widget.tree_function import make_conn_tree_items

_author_ = 'luwt'
_date_ = '2022/5/7 17:21'


class SqlTreeWidget(AbstractTreeWidget):
    """sql数据源树部件"""

    def __init__(self, parent, window):
        super().__init__(parent, window)
        self.main_window = window
        self.list_conn_executor = ...
        # 保存 sql tree 选中数据
        self.tree_data = TreeData()

    def reopen_tree(self):
        # 如果还没初始化过，再执行初始化
        if self.list_conn_executor is Ellipsis:
            # 初始化数据
            self.list_conn_executor = ListConnExecutor(self.main_window, self.main_window,
                                                       self.reopen_start,
                                                       self.reopen_items,
                                                       self.reopen_tab,
                                                       self.reopen_end)
            self.list_conn_executor.start()

    def get_current_tab(self) -> TabTableUI:
        return self.main_window.sql_tab_widget.currentWidget()

    def reopen_start(self):
        self.reopening_flag = True

    def reopen_items(self, opened_items):
        """
        重新打开树节点
        :param opened_items: 打开记录表中元素
        """
        level = opened_items[0].level
        # 如果是连接，单独处理
        if level == SqlTreeItemLevel.conn_level.value:
            make_conn_tree_items(opened_items, self)
        else:
            # 如果是其他类型，按策略来执行
            self.reopen_tree_item(opened_items)

    def reopen_tab(self, opened_tabs):
        """
        重新打开tab页
        """
        current_tab = None
        for opened_tab in opened_tabs:
            # 找到表节点
            item = self.get_item_by_opened_id(opened_tab.parent_opened_id)
            get_sql_tree_node(item, self, self.main_window).reopen_item(opened_tab)
            tab = get_item_opened_tab(item)
            if opened_tab.is_current:
                current_tab = tab
        # 将当前页置为当前
        self.main_window.sql_tab_widget.setCurrentWidget(current_tab)

    def reopen_end(self):
        # 找出当前项，选中
        self.set_record_current_item()
        self.reopening_flag = False

    def reopen_tree_item(self, opened_items):
        # 首先获取父元素
        parent_item = self.get_item_by_opened_id(opened_items[0].parent_id)
        get_sql_tree_node(parent_item, self, self.main_window).reopen_item(opened_items)

    def do_open_tree_item(self, item):
        get_sql_tree_node(item, self, self.main_window).open_item()

    def do_fill_menu(self, item, menu):
        get_sql_tree_node(item, self, self.main_window).do_fill_menu(menu)

    def do_handle_right_menu_func(self, item, func_name):
        get_sql_tree_node(item, self, self.main_window).handle_menu_func(func_name)

    def do_handle_checkbox_changed(self, item, clicked):
        get_sql_tree_node(item, self, self.main_window).change_check_box(item.checkState(0))
