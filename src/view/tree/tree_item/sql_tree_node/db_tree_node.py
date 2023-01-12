# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction

from constant.constant import NO_TBS_PROMPT, OPEN_TB_TITLE, CANCEL_OPEN_DB_MENU, OPEN_DB_MENU, CLOSE_DB_MENU, \
    SELECT_ALL_TB_MENU, UNSELECT_TB_MENU, CLOSE_DB_PROMPT
from service.async_func.async_sql_conn_task import CloseDBExecutor
from service.async_func.async_sql_ds_task import OpenDBExecutor
from view.box.message_box import pop_fail, pop_question
from view.tree.tree_item.sql_tree_node.abstract_sql_tree_node import AbstractSqlTreeNode
from view.tree.tree_item.sql_tree_node.table_tree_node import TableTreeNode
from view.tree.tree_item.tree_item_func import get_item_opened_tab, get_add_del_data, get_children_opened_ids
from view.tree.tree_widget.tree_function import make_table_items, check_table_status

_author_ = 'luwt'
_date_ = '2022/7/6 22:04'


class DBTreeNode(AbstractSqlTreeNode):

    def __init__(self, *args):
        super().__init__(*args)
        self.db_name = self.item.text(0)
        self.open_db_executor: OpenDBExecutor = ...
        self.close_db_executor: CloseDBExecutor = ...

    def open_item(self):
        if not self.item.childCount():
            # 设置正在打开中状态
            self.is_opening = True
            self.open_db_executor = OpenDBExecutor(self.item, self.window, self.open_item_ui, self.open_item_fail)
            self.open_db_executor.start()
        self.tree_widget.set_selected_focus(self.item)

    def open_item_ui(self, opened_table_items):
        self.is_opening = False
        if opened_table_items:
            make_table_items(self.tree_widget, self.item, opened_table_items, self.tree_widget.tree_data)
            self.item.setExpanded(True)
            self.tree_widget.set_selected_focus(self.item)
        else:
            pop_fail(NO_TBS_PROMPT.format(self.item.parent().text(0), self.db_name), OPEN_TB_TITLE, self.window)

    def open_item_fail(self):
        self.is_opening = False

    def reopen_item(self, opened_items):
        # 打开库下的表节点
        make_table_items(self.tree_widget, self.item, opened_items, self.tree_widget.tree_data)
        self.item.setExpanded(self.opened_item.expanded)
        if self.opened_item.is_current:
            self.tree_widget.set_selected_focus(self.item)

    def close_item(self):
        # 判断是否有选中数据
        del_data = get_add_del_data(self.item)
        db_data_node = self.tree_widget.tree_data.get_node(del_data)
        # 如果能找到选中数据，提示将清空数据，是否继续
        if db_data_node:
            if not pop_question(CLOSE_DB_PROMPT, CLOSE_DB_MENU.format(self.db_name), self.window):
                return
        tab_indexes, tab_ids = self.get_tab_indexes_and_ids()
        child_opened_ids = get_children_opened_ids(self.item)
        self.close_db_executor = CloseDBExecutor(self.db_name, child_opened_ids, tab_indexes,
                                                 tab_ids, self.item, self.window, self.close_db_callback)
        self.close_db_executor.start()

    def close_db_callback(self, tab_indexes):
        # 首先删除选中数据
        del_data = get_add_del_data(self.item)
        self.tree_widget.tree_data.del_node(del_data)
        # 处理tab
        if tab_indexes:
            [self.window.sql_tab_widget.tab_bar.remove_tab(index, False, False) for index in tab_indexes]
        # 再处理子节点线程
        for i in range(self.item.childCount()):
            child_item = self.item.child(i)
            child_node = TableTreeNode(child_item, self.tree_widget, self.window)
            # 将线程停止
            child_node.worker_terminate()
        # 删除库下的节点
        self.item.takeChildren()
        self.item.setExpanded(False)

    def get_tab_indexes_and_ids(self):
        tab_indexes, tab_ids = list(), list()
        for i in range(self.item.childCount()):
            item = self.item.child(i)
            tab = get_item_opened_tab(item)
            if tab:
                tab_indexes.append(self.window.sql_tab_widget.indexOf(tab))
                tab_ids.append(tab.table_tab.id)
        if tab_indexes:
            # 倒序
            tab_indexes.sort(reverse=True)
        return tab_indexes, tab_ids

    def do_fill_menu(self, menu):
        if self.item.childCount():
            check_state = check_table_status(self.item)
            menu.addAction(QAction(CLOSE_DB_MENU.format(self.db_name), menu))
            # 全选时：添加取消选择菜单
            if check_state[0]:
                menu.addAction(QAction(UNSELECT_TB_MENU, menu))
            # 部分选中时：添加全选菜单和取消选择菜单
            elif check_state[1]:
                menu.addAction(QAction(SELECT_ALL_TB_MENU, menu))
                menu.addAction(QAction(UNSELECT_TB_MENU, menu))
            else:
                # 都未选中时：添加全选菜单
                menu.addAction(QAction(SELECT_ALL_TB_MENU, menu))
        # 根据打开标识判断是否正在打开中
        elif self.item.data(1, Qt.UserRole):
            menu.addAction(QAction(CANCEL_OPEN_DB_MENU.format(self.db_name), menu))
        else:
            menu.addAction(QAction(OPEN_DB_MENU.format(self.db_name), menu))

    def handle_menu_func(self, func):
        # 打开数据库
        if func == OPEN_DB_MENU.format(self.db_name):
            self.open_item()
        # 取消打开数据库
        elif func == CANCEL_OPEN_DB_MENU.format(self.db_name):
            self.open_db_executor.worker_terminate(self.open_item_fail)
        # 关闭数据库
        elif func == CLOSE_DB_MENU.format(self.db_name):
            self.close_item()
        # 全选所有表
        elif func == SELECT_ALL_TB_MENU:
            self.tree_widget.handle_child_item_checked(self.item, Qt.Checked)
        # 取消全选所有表
        elif func == UNSELECT_TB_MENU:
            self.tree_widget.handle_child_item_checked(self.item, Qt.Unchecked)

    def worker_terminate(self):
        if self.open_db_executor is not Ellipsis:
            self.open_db_executor.worker_terminate()
