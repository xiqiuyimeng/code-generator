# -*- coding: utf-8 -*-
"""
sql数据源树结构
"""
from PyQt5.QtWidgets import QTreeWidgetItemIterator

from service.async_func.async_sql_conn_task import ListConnExecutor
from service.system_storage.opened_tree_item_sqlite import SqlTreeItemLevel
from service.util.tree_node import TreeData
from view.tab.tab_ui import TabTableUI
from view.tree.tree_item.context import get_tree_node
from view.tree.tree_widget.abstract_tree_widget import AbstractTreeWidget
from view.tree.tree_widget.tree_function import make_sql_conn_tree_items
from view.tree.tree_item.tree_item_func import set_item_opened_record, get_item_sql_conn, get_item_opened_tab

_author_ = 'luwt'
_date_ = '2022/5/7 17:21'


class SqlTreeWidget(AbstractTreeWidget):
    """sql数据源树部件"""

    def __init__(self, parent, window):
        super().__init__(parent, window)
        self.main_window = window
        # 存储连接名称和id
        self.conn_name_id_dict: dict = ...
        self.list_conn_executor = ...
        # 保存 sql tree 选中数据
        self.tree_data = TreeData()

    def reopen_tree(self):
        # 如果还没初始化过，再执行初始化
        if self.list_conn_executor is Ellipsis:
            # 初始化数据
            self.list_conn_executor = ListConnExecutor(self.main_window, self.main_window,
                                                       self.init_conn_tree_items,
                                                       self.reopen_items,
                                                       self.reopen_tab,
                                                       self.reopen_end)
            self.list_conn_executor.start()

    def get_current_tab(self) -> TabTableUI:
        return self.main_window.sql_tab_widget.currentWidget()

    def init_conn_tree_items(self, conns):
        self.reopening_flag = True
        make_sql_conn_tree_items(conns, self)
        self.init_conn_name_dict(conns)

    def reopen_items(self, opened_items):
        """
        重新打开树节点
        :param opened_items: 打开记录表中元素
        """
        level = opened_items[0].level
        # 如果是连接，那么只需要设置下打开记录中的信息
        if level == SqlTreeItemLevel.conn_level.value:
            self.set_item_opened_record(opened_items)
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
            get_tree_node(item, self, self.main_window).reopen_item(opened_tab)
            tab = get_item_opened_tab(item)
            if opened_tab.is_current:
                current_tab = tab
        # 将当前页置为当前
        self.main_window.sql_tab_widget.setCurrentWidget(current_tab)

    def reopen_end(self):
        # 找出当前项，选中
        self.set_record_current_item()
        self.reopening_flag = False

    def set_item_opened_record(self, opened_items):
        for opened_item in opened_items:
            item = self.get_item_by_opened_parent_id(opened_item.parent_id)
            set_item_opened_record(item, opened_item)

    def reopen_tree_item(self, opened_items):
        # 首先获取父元素
        parent_item = self.get_item_by_opened_id(opened_items[0].parent_id)
        get_tree_node(parent_item, self, self.main_window).reopen_item(opened_items)

    def get_item_by_opened_parent_id(self, opened_parent_id):
        """
        根据打开记录表中的父id查找，对于连接层，重新打开后，
        只有连接表中的id，即为打开记录表中的父id
        """
        iterator = QTreeWidgetItemIterator(self)
        while iterator.value():
            item = iterator.value()
            conn_info = get_item_sql_conn(item)
            if conn_info and conn_info.id == opened_parent_id:
                return item
            iterator = iterator.__iadd__(1)

    def init_conn_name_dict(self, conns):
        self.conn_name_id_dict = dict(zip(map(lambda conn: conn.conn_name, conns), map(lambda conn: conn.id, conns)))

    def add_conn_name(self, conn_id, conn_name):
        self.conn_name_id_dict[conn_name] = conn_id

    def update_conn_name(self, conn_id, conn_name):
        self.conn_name_id_dict[conn_name] = conn_id

    def del_conn_name(self, conn_name):
        del self.conn_name_id_dict[conn_name]

    def do_open_tree_item(self, item):
        get_tree_node(item, self, self.main_window).open_item()

    def do_fill_menu(self, item, menu):
        get_tree_node(item, self, self.main_window).do_fill_menu(menu)

    def do_handle_right_menu_func(self, item, func_name):
        get_tree_node(item, self, self.main_window).handle_menu_func(func_name)

    def do_handle_item_change(self, item):
        get_tree_node(item, self, self.main_window).change_check_box(item.checkState(0))

