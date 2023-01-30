# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMenu, QAction

from constant.constant import CANCEL_OPEN_CONN_ACTION, OPEN_CONN_ACTION, CLOSE_CONN_ACTION, CANCEL_TEST_CONN_ACTION, \
    TEST_CONN_ACTION, ADD_CONN_ACTION, EDIT_CONN_ACTION, DEL_CONN_ACTION, TEST_CONN_SUCCESS_PROMPT, TEST_CONN_TITLE, \
    ADD_DS_ACTION, EDIT_CONN_PROMPT, DEL_CONN_PROMPT, CLOSE_CONN_PROMPT, REFRESH_ACTION
from constant.icon_enum import get_icon
from service.async_func.async_sql_conn_task import DelConnExecutor, CloseConnExecutor
from service.async_func.async_sql_ds_task import OpenConnExecutor, TestConnIconMovieExecutor, RefreshConnExecutor
from view.bar.bar_action import add_sql_ds_actions
from view.box.message_box import pop_ok, pop_question
from view.tree.tree_item.sql_tree_node.abstract_sql_tree_node import AbstractSqlTreeNode
from view.tree.tree_item.sql_tree_node.db_tree_node import DBTreeNode
from view.tree.tree_item.tree_item_func import get_item_opened_record, get_add_del_data, get_children_opened_ids, \
    get_item_opened_tab, set_item_opened_record
from view.tree.tree_widget.tree_function import make_db_items, edit_conn_func, make_sql_tree_item

_author_ = 'luwt'
_date_ = '2022/7/6 22:04'


class ConnTreeNode(AbstractSqlTreeNode):

    def __init__(self, *args):
        super().__init__(*args)
        self.conn_name = self.item.text(0)
        self.open_conn_executor: OpenConnExecutor = ...
        self.test_conn_executor: TestConnIconMovieExecutor = ...
        self.del_conn_executor: DelConnExecutor = ...
        self.close_conn_executor: CloseConnExecutor = ...
        self.refresh_conn_executor: RefreshConnExecutor = ...
        self.is_testing = False

    def open_item(self):
        if not self.is_opening and not self.item.childCount():
            # 设置正在打开中状态
            self.is_opening = True
            self.open_conn_executor = OpenConnExecutor(self.item, self.window, self.open_item_ui, self.open_item_fail)
            self.open_conn_executor.start()
        else:
            self.tree_widget.set_selected_focus(self.item)

    def open_item_ui(self, opened_db_items):
        self.is_opening = False
        make_db_items(self.tree_widget, self.item, opened_db_items)
        self.item.setExpanded(True)
        self.tree_widget.set_selected_focus(self.item)

    def reopen_item(self, opened_items):
        # 打开连接下的库节点
        make_db_items(self.tree_widget, self.item, opened_items)
        self.item.setExpanded(self.opened_item.expanded)
        if self.opened_item.is_current:
            self.tree_widget.set_selected_focus(self.item)

    def close_item(self, close_for_edit=False):
        # 判断是否有选中数据
        del_data = get_add_del_data(self.item)
        conn_data_node = self.tree_widget.tree_data.get_node(del_data)
        # 如果能找到选中数据，提示将会清空数据，是否继续
        if conn_data_node:
            if not pop_question(CLOSE_CONN_PROMPT, CLOSE_CONN_ACTION.format(self.conn_name), self.window):
                return

        # 关闭连接
        tab_indexes, tab_ids = self.get_tab_indexes_and_ids()
        opened_record = get_item_opened_record(self.item)
        child_opened_ids = get_children_opened_ids(self.item)
        self.close_conn_executor = CloseConnExecutor(opened_record.parent_id, self.conn_name,
                                                     child_opened_ids, tab_indexes, tab_ids,
                                                     close_for_edit, self.item, self.window,
                                                     self.close_conn_callback)
        self.close_conn_executor.start()

    def close_conn_callback(self, tab_indexes, close_for_edit):
        self.do_close_conn_callback(tab_indexes)
        # 删除连接下的节点
        self.item.takeChildren()
        self.item.setExpanded(False)
        # 如果是针对于在编辑时关闭连接，那么下一步需要调用编辑方法
        if close_for_edit:
            self.edit_conn()

    def do_close_conn_callback(self, tab_indexes):
        # 首先删除选中数据
        del_data = get_add_del_data(self.item)
        self.tree_widget.tree_data.del_node(del_data)
        # 移除界面中属于当前连接的tab页
        if tab_indexes:
            [self.tree_widget.get_current_tab_widget().tab_bar.remove_tab(index, False, False)
             for index in tab_indexes]
        # 停止子节点线程
        for i in range(self.item.childCount()):
            child_item = self.item.child(i)
            if child_item.childCount():
                child_node = DBTreeNode(child_item, self.tree_widget, self.window)
                # 将线程停止
                child_node.worker_terminate()

    def get_tab_indexes_and_ids(self):
        tab_indexes, tab_ids = list(), list()
        for i in range(self.item.childCount()):
            child_item = self.item.child(i)
            child_node = DBTreeNode(child_item, self.tree_widget, self.window)
            child_tab_index_list, child_tab_ids = child_node.get_tab_indexes_and_ids()
            tab_indexes.extend(child_tab_index_list)
            tab_ids.extend(child_tab_ids)
        tab_indexes.sort(reverse=True)
        return tab_indexes, tab_ids

    def do_fill_menu(self, menu: QMenu):
        # 添加连接需要有二级菜单
        add_conn_menu = QMenu(ADD_CONN_ACTION, menu)
        add_conn_menu.setIcon(get_icon(ADD_DS_ACTION))
        # 二级菜单
        add_sql_ds_actions(add_conn_menu, self.window)
        menu.addMenu(add_conn_menu)
        menu.addSeparator()

        # 打开连接、取消打开连接、关闭连接
        if not self.is_testing:
            open_menu_name = CANCEL_OPEN_CONN_ACTION \
                if self.is_opening else OPEN_CONN_ACTION \
                if not self.item.childCount() else CLOSE_CONN_ACTION
            menu.addAction(QAction(get_icon(open_menu_name), open_menu_name.format(self.conn_name), menu))
        if not self.is_opening:
            # 测试连接、取消测试连接
            test_conn_menu = CANCEL_TEST_CONN_ACTION \
                if self.is_testing else TEST_CONN_ACTION
            menu.addAction(QAction(get_icon(test_conn_menu), test_conn_menu.format(self.conn_name), menu))
        # 编辑连接
        menu.addAction(QAction(get_icon(EDIT_CONN_ACTION), EDIT_CONN_ACTION.format(self.conn_name), menu))
        menu.addSeparator()

        # 删除连接
        menu.addAction(QAction(get_icon(DEL_CONN_ACTION), DEL_CONN_ACTION.format(self.conn_name), menu))

        # 刷新
        menu.addSeparator()
        menu.addAction(QAction(get_icon(REFRESH_ACTION), f'{REFRESH_ACTION}连接 [{self.conn_name}]', menu))

    def test_conn(self):
        self.is_testing = True
        self.test_conn_executor = TestConnIconMovieExecutor(self.item, self.window,
                                                            self.test_conn_success, self.test_conn_fail)
        self.test_conn_executor.start()

    def test_conn_success(self):
        self.is_testing = False
        pop_ok(f'[{self.conn_name}]\n{TEST_CONN_SUCCESS_PROMPT}', TEST_CONN_TITLE, self.window)

    def test_conn_fail(self):
        self.is_testing = False

    def handle_menu_func(self, func):
        # 打开连接
        if func == OPEN_CONN_ACTION.format(self.conn_name):
            self.open_item()
        # 取消打开连接
        elif func == CANCEL_OPEN_CONN_ACTION.format(self.conn_name):
            self.open_conn_executor.worker_terminate(self.open_item_fail)
        # 关闭连接
        elif func == CLOSE_CONN_ACTION.format(self.conn_name):
            self.close_item()
        # 测试连接
        elif func == TEST_CONN_ACTION.format(self.conn_name):
            self.test_conn()
        # 取消测试连接
        elif func == CANCEL_TEST_CONN_ACTION.format(self.conn_name):
            self.test_conn_executor.worker_terminate(self.test_conn_fail)
        # 编辑连接
        elif func == EDIT_CONN_ACTION.format(self.conn_name):
            if self.item.childCount():
                if pop_question(EDIT_CONN_PROMPT, EDIT_CONN_ACTION.format(self.conn_name), self.window):
                    self.close_item(close_for_edit=True)
            else:
                self.edit_conn()
        # 删除连接
        elif func == DEL_CONN_ACTION.format(self.conn_name):
            if pop_question(DEL_CONN_PROMPT, DEL_CONN_ACTION.format(self.conn_name), self.window):
                self.del_conn()
        # 刷新
        elif func == f'{REFRESH_ACTION}连接 [{self.conn_name}]':
            self.refresh()

    def edit_conn(self):
        edit_conn_func(self.opened_item.data_type.display_name, self.tree_widget,
                       self.window.geometry(), self.opened_item.parent_id)

    def del_conn(self):
        # 在删除连接之后的连接项，应该对其进行重新排序
        reorder_items = self.get_need_reorder_items()
        tab_indexes, tab_ids = self.get_tab_indexes_and_ids()
        self.del_conn_executor = DelConnExecutor(self.opened_item.parent_id, self.opened_item.item_name,
                                                 reorder_items, tab_indexes, tab_ids,
                                                 self.del_conn_callback, self.item, self.window)
        self.del_conn_executor.start()

    def get_need_reorder_items(self):
        conn_items = self.tree_widget.get_top_level_items()
        index = conn_items.index(self.item)
        need_reorder_items = conn_items[index + 1:]
        if need_reorder_items:
            reorder_items = tuple(map(lambda x: get_item_opened_record(x), need_reorder_items))
            for reorder_item in reorder_items:
                reorder_item.item_order -= 1
            return reorder_items

    def del_conn_callback(self, tab_indexes):
        self.do_close_conn_callback(tab_indexes)
        self.worker_terminate()
        # 删除节点
        self.tree_widget.takeTopLevelItem(self.tree_widget.indexOfTopLevelItem(self.item))

    def refresh(self):
        if self.is_refreshing:
            return
        self.is_refreshing = True
        self.refresh_conn_executor = RefreshConnExecutor(self.item, self.window,
                                                         self.refresh_db_callback,
                                                         self.refresh_table_callback,
                                                         self.refresh_cols_callback,
                                                         self.refresh_db_finished_callback,
                                                         self.refresh_success, self.refresh_fail)
        self.refresh_conn_executor.start()

    def refresh_db_callback(self, table_changed_dict: dict):
        # 清空选中数据
        del_data = get_add_del_data(self.item)
        self.tree_widget.tree_data.del_node(del_data)

        new_items = table_changed_dict.get('new')
        exists_items = table_changed_dict.get('exists')
        delete_items = table_changed_dict.get('delete')

        # 首先处理删除的元素
        for delete_item_record in delete_items:
            del_item = self.tree_widget.get_item_by_opened_id(delete_item_record.id)
            # 如果存在子节点
            if del_item.childCount():
                for del_index in range(del_item.childCount()):
                    del_child_item = del_item.child(del_index)
                    # 寻找子节点打开的tab页，将其删除
                    del_tab = get_item_opened_tab(del_child_item)
                    if del_tab:
                        del_tab_index = self.tree_widget.get_current_tab_widget().indexOf(del_tab)
                        # 删除tab，清除对应数据由槽函数处理
                        self.tree_widget.get_current_tab_widget().tab_bar.remove_tab(del_tab_index, False)
                    del_item.removeChild(del_child_item)
            # 删除树节点
            self.item.removeChild(del_item)
        # 处理需要更新的元素
        for exists_item_record in exists_items:
            update_item = self.tree_widget.get_item_by_opened_id(exists_item_record.id)
            set_item_opened_record(update_item, exists_item_record)
            # 只停止没有子节点的节点动画
            if not update_item.childCount():
                self.refresh_conn_executor.stop_one_movie(update_item)
        # 最后处理需要插入的节点元素
        icon = get_icon(get_item_opened_record(self.item).data_type.db_icon_name)
        for new_item_record in new_items:
            # 根据顺序来插入
            new_item = make_sql_tree_item(self.tree_widget, self.item, new_item_record.item_name,
                                          icon, new_item_record)
            self.item.insertChild(new_item_record.item_order, new_item)

    def refresh_table_callback(self, table_changed_dict: dict):
        db_item = self.tree_widget.get_item_by_opened_id(table_changed_dict.get('parent_id'))
        self.tree_widget.get_item_node(db_item).refresh_tables_callback(
            table_changed_dict, self.refresh_conn_executor)

    def refresh_cols_callback(self, table_tab):
        # 刷新tab页面
        tb_item = self.tree_widget.get_item_by_opened_id(table_tab.parent_opened_id)
        self.tree_widget.get_item_node(tb_item).refresh_success(table_tab)
        # 刷新完成，停止tab动画
        self.refresh_conn_executor.stop_one_movie(tb_item)

    def refresh_db_finished_callback(self, opened_db_id):
        db_item = self.tree_widget.get_item_by_opened_id(opened_db_id)
        self.refresh_conn_executor.stop_one_movie(db_item)

    def worker_terminate(self):
        if self.open_conn_executor is not Ellipsis:
            self.open_conn_executor.worker_terminate()
        if self.test_conn_executor is not Ellipsis:
            self.test_conn_executor.worker_terminate()
