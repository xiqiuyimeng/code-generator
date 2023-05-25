# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt

from src.constant.tree_constant import OPEN_DB_BOX_TITLE, NO_TBS_PROMPT, CLOSE_DB_ACTION, CLOSE_DB_PROMPT, \
    CANCEL_OPEN_DB_ACTION, CANCEL_REFRESH_DB_ACTION, UNSELECT_TB_ACTION, SELECT_ALL_TB_ACTION, OPEN_DB_ACTION, \
    REFRESH_DB_ACTION, REFRESH_DB_BOX_TITLE
from src.service.async_func.async_sql_conn_task import CloseDBExecutor
from src.service.async_func.async_sql_ds_task import OpenDBExecutor, RefreshDBExecutor
from src.view.box.message_box import pop_fail, pop_question
from src.view.tree.tree_item.sql_tree_node.sql_tree_node_abc import SqlTreeNodeABC
from src.view.tree.tree_item.sql_tree_node.table_tree_node import TableTreeNode
from src.view.tree.tree_item.tree_item_func import get_item_opened_tab, get_add_del_data, get_children_opened_ids, \
    get_item_opened_record, refresh_tree_item_callback
from src.view.tree.tree_widget.tree_function import make_table_items, check_table_status, make_sql_tree_item

_author_ = 'luwt'
_date_ = '2022/7/6 22:04'


class DBTreeNode(SqlTreeNodeABC):

    def __init__(self, *args):
        super().__init__(*args)
        self.open_db_executor: OpenDBExecutor = ...
        self.close_db_executor: CloseDBExecutor = ...
        self.refresh_db_executor: RefreshDBExecutor = ...

    def open_item(self):
        if not self.item.childCount():
            if self.is_opening or self.is_refreshing:
                return
            # 设置正在打开中状态
            self.is_opening = True
            self.tree_widget.get_item_node(self.item.parent()).add_opening_child_count()
            self.open_db_executor = OpenDBExecutor(self.item, self.window, OPEN_DB_BOX_TITLE,
                                                   self.open_item_ui, self.open_item_fail)
            self.open_db_executor.start()
        else:
            self.tree_widget.set_selected_focus(self.item)

    def open_item_ui(self, opened_table_items):
        self.is_opening = False
        self.tree_widget.get_item_node(self.item.parent()).sub_opening_child_count()
        if opened_table_items:
            make_table_items(self.tree_widget, self.item, opened_table_items, self.tree_widget.tree_data)
            self.item.setExpanded(True)
            self.tree_widget.set_selected_focus(self.item)
        else:
            pop_fail(NO_TBS_PROMPT.format(self.item.parent().text(0), self.item_name),
                     OPEN_DB_BOX_TITLE, self.window)

    def reopen_item(self, opened_items):
        # 打开库下的表节点
        make_table_items(self.tree_widget, self.item, opened_items, self.tree_widget.tree_data)
        opened_record = get_item_opened_record(self.item)
        self.item.setExpanded(opened_record.expanded)
        if opened_record.is_current:
            self.tree_widget.set_selected_focus(self.item)

    def close_item(self):
        # 检查库是否可以关闭
        close_db_prompt = self.not_allow_operate_prompt()
        if close_db_prompt:
            close_db_prompt = close_db_prompt.format(self.item_name)
            pop_fail(close_db_prompt, CLOSE_DB_ACTION.format(self.item_name), self.window)
            return
        # 判断是否有选中数据
        del_data = get_add_del_data(self.item)
        db_data_node = self.tree_widget.tree_data.get_node(del_data)
        # 如果能找到选中数据，提示将清空数据，是否继续
        if db_data_node:
            if not pop_question(CLOSE_DB_PROMPT, CLOSE_DB_ACTION.format(self.item_name), self.window):
                return
        tab_indexes, tab_ids = self.get_tab_indexes_and_ids()
        child_opened_ids = get_children_opened_ids(self.item)
        self.close_db_executor = CloseDBExecutor(self.item_name, child_opened_ids, tab_indexes,
                                                 tab_ids, self.item, self.window, self.close_db_callback)
        self.close_db_executor.start()

    def close_db_callback(self, tab_indexes):
        # 首先删除选中数据
        del_data = get_add_del_data(self.item)
        self.tree_widget.tree_data.del_node(del_data)
        # 处理tab
        if tab_indexes:
            [self.tree_widget.get_current_tab_widget().tab_bar.remove_tab(index, False, False)
             for index in tab_indexes]
        # 再处理子节点线程
        for i in range(self.item.childCount()):
            child_item = self.item.child(i)
            child_node = TableTreeNode(child_item, self.tree_widget)
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
                tab_indexes.append(self.tree_widget.get_current_tab_widget().indexOf(tab))
                tab_ids.append(tab.table_tab.id)
        if tab_indexes:
            # 倒序
            tab_indexes.sort(reverse=True)
        return tab_indexes, tab_ids

    def do_fill_menu(self, menu):
        # 取消打开和取消刷新
        if self.add_cancel_open_refresh_menu(CANCEL_OPEN_DB_ACTION,
                                             CANCEL_REFRESH_DB_ACTION, menu):
            return

        if self.item.childCount():
            check_state = check_table_status(self.item)
            self.add_menu(CLOSE_DB_ACTION, menu)
            # 全选时：添加取消选择菜单
            if check_state[0]:
                self.add_menu(UNSELECT_TB_ACTION, menu)
            # 部分选中时：添加全选菜单和取消选择菜单
            elif check_state[1]:
                self.add_menu(SELECT_ALL_TB_ACTION, menu)
                self.add_menu(UNSELECT_TB_ACTION, menu)
            else:
                # 都未选中时：添加全选菜单
                self.add_menu(SELECT_ALL_TB_ACTION, menu)
        else:
            self.add_menu(OPEN_DB_ACTION, menu)

        # 刷新
        self.add_refresh_menu(REFRESH_DB_ACTION, menu)

    def handle_menu_func(self, func):
        # 打开数据库
        if func == OPEN_DB_ACTION.format(self.item_name):
            self.open_item()
        # 取消打开数据库
        elif func == CANCEL_OPEN_DB_ACTION.format(self.item_name):
            self.open_db_executor.worker_terminate(self.open_item_fail)
        # 关闭数据库
        elif func == CLOSE_DB_ACTION.format(self.item_name):
            self.close_item()
        # 全选所有表
        elif func == SELECT_ALL_TB_ACTION:
            self.tree_widget.handle_child_item_checked(self.item, Qt.Checked)
        # 取消全选所有表
        elif func == UNSELECT_TB_ACTION:
            self.tree_widget.handle_child_item_checked(self.item, Qt.Unchecked)
        # 刷新
        elif func == REFRESH_DB_ACTION.format(self.item_name):
            self.refresh()
        # 取消刷新
        elif func == CANCEL_REFRESH_DB_ACTION.format(self.item_name):
            self.refresh_db_executor.worker_terminate()

    def refresh(self):
        if self.is_refreshing or self.is_opening:
            return
        refresh_prompt = self.not_allow_operate_prompt()
        if refresh_prompt:
            pop_fail(refresh_prompt.format(self.item_name),
                     REFRESH_DB_ACTION.format(self.item_name), self.window)
            return
        self.refresh_db_executor = RefreshDBExecutor(self.refresh_tables_callback, self.refresh_cols_callback,
                                                     self.tree_widget, self.item, self.window, REFRESH_DB_BOX_TITLE)
        self.refresh_db_executor.start()

    def refresh_tables_callback(self, table_changed_dict: dict, refresh_executor=None):
        refresh_tree_item_callback(self.tree_widget, self.item, table_changed_dict,
                                   self.handle_refresh_unchanged_records,
                                   self.handle_refresh_delete_records,
                                   make_sql_tree_item,
                                   refresh_executor)

    def handle_refresh_unchanged_records(self, unchanged_item, refresh_executor=None):
        # 只停止没有打开tab表的节点动画
        if not get_item_opened_tab(unchanged_item):
            self.stop_refresh_movie(unchanged_item, refresh_executor)
            # 显示子节点复选框
            self.tree_widget.get_item_node(unchanged_item).show_check_box()

    def handle_refresh_delete_records(self, del_item, refresh_executor=None):
        # 停止动画
        self.stop_refresh_movie(del_item, refresh_executor)
        del_tab = get_item_opened_tab(del_item)
        if del_tab:
            del_tab_index = self.tree_widget.get_current_tab_widget().indexOf(del_tab)
            # 删除tab，清除对应数据由槽函数处理
            self.tree_widget.get_current_tab_widget().tab_bar.remove_tab(del_tab_index, False)

    def stop_refresh_movie(self, item, executor=None):
        if executor:
            executor.stop_one_movie(item)
        else:
            self.refresh_db_executor.stop_one_movie(item)

    def refresh_cols_callback(self, table_tab, tb_item_order):
        # 刷新tab页面
        item = self.item.child(tb_item_order - 1)
        node = self.tree_widget.get_item_node(item)
        # 显示子节点复选框
        node.show_check_box()
        node.refresh_success(table_tab)
        # 刷新完成，停止tab动画
        self.refresh_db_executor.stop_one_movie(item)

    def worker_terminate(self):
        if self.open_db_executor is not Ellipsis:
            self.open_db_executor.worker_terminate()
