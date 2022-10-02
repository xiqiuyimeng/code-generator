# -*- coding: utf-8 -*-
"""
sql数据源树结构
"""

from service.async_func.async_sql_conn_task import ListConnExecutor
from view.tree.tree_item.context import Context
from view.tree.tree_widget.abstract_tree_widget import AbstractTreeWidget
from view.tree.tree_widget.tree_function import make_sql_conn_tree_items

_author_ = 'luwt'
_date_ = '2022/5/7 17:21'


class SqlTreeWidget(AbstractTreeWidget):
    """sql数据源树部件"""

    def __init__(self, parent, window):
        super().__init__(parent, window)
        self.main_window = window
        # 存储连接id和名称
        self.conn_name_id_dict: dict = ...
        # 初始化数据
        self.list_conn_executor = ListConnExecutor(parent, parent, self.init_conn_tree_items)
        self.list_conn_executor.start()

    def init_conn_tree_items(self, conns):
        make_sql_conn_tree_items(conns, self)
        self.init_conn_name_list(conns)

    def init_conn_name_list(self, conns):
        self.conn_name_id_dict = dict(zip(map(lambda conn: conn.conn_name, conns), map(lambda conn: conn.id, conns)))

    def add_conn_name(self, conn_id, conn_name):
        self.conn_name_id_dict[conn_name] = conn_id

    def update_conn_name(self, conn_id, conn_name):
        self.conn_name_id_dict[conn_name] = conn_id

    def del_conn_name(self, conn_name):
        del self.conn_name_id_dict[conn_name]

    def do_open_tree_item(self, item):
        Context(item, self, self.main_window).open_item()

    def do_fill_menu(self, item, menu):
        Context(item, self, self.main_window).do_fill_menu(menu)

    def do_handle_right_menu_func(self, item, func_name):
        Context(item, self, self.main_window).handle_menu_func(func_name)

    def do_handle_item_change(self, item):
        Context(item, self, self.main_window).change_check_box(item.checkState(0))

