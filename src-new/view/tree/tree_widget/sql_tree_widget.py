# -*- coding: utf-8 -*-
"""
sql数据源树结构
"""
from PyQt5.QtGui import QIcon

from service.async_func.async_conn_task import ListConnExecutor
from view.tree.tree_item.context import Context
from view.tree.tree_widget.abstract_tree_widget import AbstractTreeWidget
from view.tree.tree_widget.tree_function import make_conn_tree_items

_author_ = 'luwt'
_date_ = '2022/5/7 17:21'


class SqlTreeWidget(AbstractTreeWidget):
    """sql数据源树部件"""

    def __init__(self, parent, window):
        super().__init__(parent, window)
        self.main_window = window
        self.conn_name_dict: dict = ...
        # 连接的图标
        self.conn_icon = QIcon(":/icon/mysql_conn_icon.png")
        # 数据库图标
        self.db_icon = QIcon(":icon/database_icon.png")
        # 数据表图标
        self.tb_icon = QIcon(":icon/table_icon.png")
        # 初始化数据
        self.list_conn_executor = ListConnExecutor(parent, parent, self.init_conn_tree_items)
        self.list_conn_executor.start()

    def init_conn_tree_items(self, conns):
        make_conn_tree_items(conns, self, self.conn_icon)
        self.init_conn_name_list(conns)

    def init_conn_name_list(self, conns):
        self.conn_name_dict = dict(zip(map(lambda conn: conn.id, conns), map(lambda conn: conn.name, conns)))

    def add_conn_name(self, conn_id, conn_name):
        self.conn_name_dict[conn_id] = conn_name

    def update_conn_name(self, conn_id, conn_name):
        self.conn_name_dict[conn_id] = conn_name

    def del_conn_name(self, conn_id):
        del self.conn_name_dict[conn_id]

    def do_open_tree_item(self, item):
        Context(item, self, self.main_window).open_item()

    def do_get_menu_names(self, item):
        return Context(item, self, self.main_window).get_menu_names()

    def do_handle_right_menu_func(self, item, func_name):
        Context(item, self, self.main_window).handle_menu_func(func_name)

    def do_handle_item_change(self, item):
        Context(item, self, self.main_window).change_check_box(item.checkState(0))

