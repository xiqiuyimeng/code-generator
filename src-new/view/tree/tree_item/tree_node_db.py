# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction

from constant.constant import NO_TBS_PROMPT, OPEN_TB_TITLE, CANCEL_OPEN_DB_MENU, OPEN_DB_MENU, CLOSE_DB_MENU, \
    SELECT_ALL_TB_MENU, UNSELECT_TB_MENU
from service.async_func.async_sql_ds_task import OpenDBExecutor
from view.box.message_box import pop_fail
from view.tree.tree_item.abstract_tree_node import AbstractTreeNode
from view.tree.tree_item.tree_node_table import TableTreeNode
from view.tree.tree_widget.tree_function import make_table_items, check_table_status, set_children_check_state
from view.tree.tree_widget.tree_item_func import get_item_opened_record, get_item_opened_tab

_author_ = 'luwt'
_date_ = '2022/7/6 22:04'


class DBTreeNode(AbstractTreeNode):

    def __init__(self, *args):
        super().__init__(*args)
        self.db_name = self.item.text(0)
        if not hasattr(self, 'open_db_executor'):
            self.open_db_executor: OpenDBExecutor = ...

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
            make_table_items(self.item, opened_table_items, self.tree_widget.tree_data)
            self.item.setExpanded(True)
            self.tree_widget.set_selected_focus(self.item)
        else:
            pop_fail(NO_TBS_PROMPT.format(self.item.parent().text(0), self.db_name), OPEN_TB_TITLE, self.window)

    def open_item_fail(self):
        self.is_opening = False

    def reopen_item(self, opened_items):
        # 打开库下的表节点
        make_table_items(self.item, opened_items, self.tree_widget.tree_data)
        opened_item_record = get_item_opened_record(self.item)
        self.item.setExpanded(opened_item_record.expanded)
        if opened_item_record.is_current:
            self.tree_widget.set_selected_focus(self.item)

    def close_item(self):
        # 关闭子项目
        allow_close_children, index_list = self.allow_close_children()
        if allow_close_children:
            # 首先处理tab
            [self.window.sql_tab_widget.tab_bar.remove_tab(index) for index in index_list if index_list]
            # 再处理子节点线程和引用
            for i in range(self.item.childCount()):
                child_item = self.item.child(i)
                child_node = TableTreeNode(child_item, self.tree_widget, self.window)
                # 将线程停止
                child_node.worker_terminate()
            # 删除库下的节点
            self.tree_widget.item_changed_executor.close_item(self.item)
            self.item.takeChildren()
            self.item.setExpanded(False)

    def allow_close_children(self):
        index_list = list()
        for i in range(self.item.childCount()):
            item = self.item.child(i)
            tab = get_item_opened_tab(item)
            if tab:
                index = self.window.sql_tab_widget.indexOf(tab)
                index_list.append(index)
        allow_close = False
        if index_list:
            # 倒序
            index_list.sort(reverse=True)
            if self.window.sql_tab_widget.tab_bar.table_allow_close(index_list):
                allow_close = True
        else:
            allow_close = True
        return allow_close, index_list

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
            set_children_check_state(self.item, Qt.Checked, self.tree_widget, self.window)
            # 再添加
        # 取消全选所有表
        elif func == UNSELECT_TB_MENU:
            set_children_check_state(self.item, Qt.Unchecked, self.tree_widget, self.window)

    def worker_terminate(self):
        if self.open_db_executor is not Ellipsis:
            self.open_db_executor.worker_terminate()
