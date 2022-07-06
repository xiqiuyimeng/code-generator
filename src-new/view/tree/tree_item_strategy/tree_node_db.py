# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt

from constant.constant import NO_TBS_PROMPT, OPEN_TB_TITLE, CANCEL_OPEN_DB_MENU, OPEN_DB_MENU, CLOSE_DB_MENU
from service.async_func.async_mysql_task import OpenDBExecutor
from view.box.message_box import pop_fail
from view.tree.tree_function import make_table_items
from view.tree.tree_item_strategy.tree_node_abstract import TreeNodeAbstract

_author_ = 'luwt'
_date_ = '2022/7/6 22:04'


class TreeNodeDB(TreeNodeAbstract):

    def __init__(self, *args):
        super().__init__(*args)
        self.db_name = self.item.text(0)
        self.open_db_executor = ...

    def open_item(self):
        if not self.item.childCount():
            # 设置正在打开中状态
            self.item.setData(1, Qt.UserRole, True)
            self.open_db_executor = OpenDBExecutor(self.item, self.window, self.open_item_ui, self.open_item_fail)
            # 将打开连接的线程执行器绑定到item中
            self.item.setData(1, Qt.UserRole + 1, self.open_db_executor)
            self.open_db_executor.start()
        self.tree_widget.set_selected_focus(self.item)

    def open_item_ui(self, table_names):
        self.item.setData(1, Qt.UserRole, False)
        if table_names:
            make_table_items(self.tree_widget, self.item, table_names)
            self.item.setExpanded(True)
            self.tree_widget.set_selected_focus(self.item)
        else:
            pop_fail(NO_TBS_PROMPT.format(self.item.parent().text(0), self.db_name), OPEN_TB_TITLE, self.window)

    def open_item_fail(self):
        self.item.setData(1, Qt.UserRole, False)

    def close_item(self):
        ...

    def get_menu_names(self):
        return [
            # 根据是否在打开中标识
            CANCEL_OPEN_DB_MENU.format(self.db_name)
            if self.item.data(1, Qt.UserRole) else OPEN_DB_MENU.format(self.db_name)
            if not self.item.childCount() else CLOSE_DB_MENU.format(self.db_name),
        ]

    def handle_menu_func(self, func):
        # 打开数据库
        if func == OPEN_DB_MENU.format(self.db_name):
            self.open_item()
        # 取消打开数据库
        elif func == CANCEL_OPEN_DB_MENU.format(self.db_name):
            self.item.data(1, Qt.UserRole + 1).worker_terminate(self.open_item_fail)
        # 关闭数据库
        elif func == CLOSE_DB_MENU.format(self.db_name):
            pass
