# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMenu, QAction

from constant.constant import CANCEL_OPEN_CONN_ACTION, OPEN_CONN_ACTION, CLOSE_CONN_ACTION, CANCEL_TEST_CONN_ACTION, \
    TEST_CONN_ACTION, ADD_CONN_ACTION, EDIT_CONN_ACTION, DEL_CONN_ACTION, TEST_CONN_SUCCESS_PROMPT, TEST_CONN_TITLE, \
    ADD_DS_ACTION, EDIT_CONN_PROMPT, DEL_CONN_PROMPT, CLOSE_CONN_PROMPT
from constant.icon_enum import get_icon
from service.async_func.async_sql_conn_task import DelConnExecutor
from service.async_func.async_sql_ds_task import OpenConnExecutor, TestConnIconMovieExecutor
from view.bar.bar_action import add_sql_ds_actions
from view.box.message_box import pop_ok, pop_question
from view.tree.tree_item.sql_tree_node.abstract_sql_tree_node import AbstractSqlTreeNode
from view.tree.tree_item.tree_item_func import get_item_opened_record, set_item_no_change, get_add_del_data
from view.tree.tree_item.sql_tree_node.db_tree_node import DBTreeNode
from view.tree.tree_widget.tree_function import make_db_items, edit_conn_func

_author_ = 'luwt'
_date_ = '2022/7/6 22:04'


class ConnTreeNode(AbstractSqlTreeNode):

    def __init__(self, *args):
        super().__init__(*args)
        self.conn_name = self.item.text(0)
        self.open_conn_executor: OpenConnExecutor = ...
        self.test_conn_executor: TestConnIconMovieExecutor = ...
        self.del_conn_executor: DelConnExecutor = ...
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

    def open_item_fail(self):
        self.is_opening = False

    def reopen_item(self, opened_items):
        # 打开连接下的库节点
        make_db_items(self.tree_widget, self.item, opened_items)
        self.item.setExpanded(self.opened_item.expanded)
        if self.opened_item.is_current:
            self.tree_widget.set_selected_focus(self.item)

    def close_item(self):
        # 判断是否有选中数据
        del_data = get_add_del_data(self.item)
        conn_data_node = self.tree_widget.tree_data.get_node(del_data)
        # 如果能找到选中数据，提示应先清空
        if conn_data_node:
            if pop_question(CLOSE_CONN_PROMPT, CLOSE_CONN_ACTION, self.window):
                # 删除选中数据
                self.tree_widget.tree_data.del_node(del_data)
            else:
                return
        if self.item.childCount():
            index_list = self.get_tab_indexes()
            # 首先处理tab
            [self.window.sql_tab_widget.tab_bar.remove_tab(index) for index in index_list if index_list]
            # 遍历子元素，停止线程
            for i in range(self.item.childCount()):
                child_item = self.item.child(i)
                if child_item.childCount():
                    child_node = DBTreeNode(child_item, self.tree_widget, self.window)
                    # 将线程停止
                    child_node.worker_terminate()
            # 删除连接下的节点
            self.tree_widget.item_changed_executor.close_item(self.item)
            self.item.takeChildren()
            self.item.setExpanded(False)
        return True

    def get_tab_indexes(self):
        index_list = list()
        for i in range(self.item.childCount()):
            child_item = self.item.child(i)
            child_node = DBTreeNode(child_item, self.tree_widget, self.window)
            child_tab_index_list = child_node.get_tab_indexes()
            index_list.extend(child_tab_index_list)
        index_list.sort(reverse=True)
        return index_list

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
            self.edit_conn()
        # 删除连接
        elif func == DEL_CONN_ACTION.format(self.conn_name):
            if pop_question(DEL_CONN_PROMPT, DEL_CONN_ACTION.format(self.conn_name), self.window) \
                    and self.close_item():
                self.del_conn()

    def edit_conn(self):
        # 如果连接已打开，必须先关闭，再编辑
        editable = False
        if self.item.childCount():
            if pop_question(EDIT_CONN_PROMPT, EDIT_CONN_ACTION.format(self.conn_name), self.window) \
                    and self.close_item():
                editable = True
        else:
            editable = True

        if editable:
            edit_conn_func(self.opened_item.data_type.display_name, self.tree_widget,
                           self.window.geometry(), self.opened_item.parent_id)

    def del_conn(self):
        # 在删除连接之后的连接项，应该对其进行重新排序
        reorder_items = self.get_need_reorder_items()
        self.del_conn_executor = DelConnExecutor(self.opened_item.parent_id, self.opened_item.item_name,
                                                 self.item, self.window, self.del_conn_callback, reorder_items)
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

    def del_conn_callback(self):
        self.worker_terminate()
        # 禁止变化的连接节点，增加标志位，不再触发节点改变事件（删除当前节点以后，只有其后的第一个节点会触发改变事件）
        item_idx = self.tree_widget.indexOfTopLevelItem(self.item)
        if self.tree_widget.topLevelItemCount() - 1 > item_idx:
            set_item_no_change(self.tree_widget.topLevelItem(item_idx + 1), True)
        # 删除节点
        self.tree_widget.takeTopLevelItem(self.tree_widget.indexOfTopLevelItem(self.item))

    def worker_terminate(self):
        if self.open_conn_executor is not Ellipsis:
            self.open_conn_executor.worker_terminate()
        if self.test_conn_executor is not Ellipsis:
            self.test_conn_executor.worker_terminate()