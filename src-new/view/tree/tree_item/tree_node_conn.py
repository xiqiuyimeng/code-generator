# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMenu, QAction

from constant.constant import CANCEL_OPEN_CONN_ACTION, OPEN_CONN_ACTION, CLOSE_CONN_ACTION, CANCEL_TEST_CONN_ACTION, \
    TEST_CONN_ACTION, ADD_CONN_ACTION, EDIT_CONN_ACTION, DEL_CONN_ACTION, TEST_CONN_SUCCESS_PROMPT, TEST_CONN_TITLE, \
    ADD_DS_ACTION
from constant.icon_enum import get_icon
from service.async_func.async_sql_ds_task import OpenConnExecutor, TestConnIconMovieExecutor
from view.bar.bar_action import add_sql_ds_actions
from view.box.message_box import pop_ok
from view.tree.tree_item.abstract_tree_node import AbstractTreeNode
from view.tree.tree_widget.tree_function import make_db_items, edit_conn_func, set_item_opening_flag, \
    set_item_testing_flag, get_item_conn_type
from view.tree.tree_widget.tree_item_func import set_item_opening_worker, get_item_opening_flag, \
    get_item_testing_flag, get_item_sql_conn, get_item_testing_worker, get_item_opening_worker, set_item_testing_worker, \
    get_item_opened_record

_author_ = 'luwt'
_date_ = '2022/7/6 22:04'


class ConnTreeNode(AbstractTreeNode):

    def __init__(self, *args):
        super().__init__(*args)
        self.conn_name = self.item.text(0)
        self.open_conn_executor: OpenConnExecutor = ...
        self.test_conn_executor: TestConnIconMovieExecutor = ...

    def open_item(self):
        if not self.item.childCount():
            # 设置正在打开中状态
            set_item_opening_flag(self.item, True)
            self.open_conn_executor = OpenConnExecutor(self.item, self.window, self.open_item_ui, self.open_item_fail)
            # 将打开连接的线程执行器绑定到item中
            set_item_opening_worker(self.item, self.open_conn_executor)
            self.open_conn_executor.start()
        self.tree_widget.set_selected_focus(self.item)

    def open_item_ui(self, opened_db_items):
        set_item_opening_flag(self.item, False)
        make_db_items(self.item, opened_db_items)
        self.item.setExpanded(True)
        self.tree_widget.set_selected_focus(self.item)

    def open_item_fail(self):
        set_item_opening_flag(self.item, False)

    def reopen_item(self, opened_items):
        # 打开连接下的库节点
        make_db_items(self.item, opened_items)
        opened_item_record = get_item_opened_record(self.item)
        self.item.setExpanded(opened_item_record.expanded)
        if opened_item_record.is_current:
            self.tree_widget.set_selected_focus(self.item)

    def close_item(self):
        ...

    def do_fill_menu(self, menu: QMenu):
        # 添加连接需要有二级菜单
        add_conn_menu = QMenu(ADD_CONN_ACTION, menu)
        add_conn_menu.setIcon(get_icon(ADD_DS_ACTION))
        # 二级菜单
        add_sql_ds_actions(add_conn_menu, self.window)
        menu.addMenu(add_conn_menu)
        menu.addSeparator()

        # 打开连接、取消打开连接、关闭连接
        open_menu_name = CANCEL_OPEN_CONN_ACTION \
            if get_item_opening_flag(self.item) else OPEN_CONN_ACTION \
            if not self.item.childCount() else CLOSE_CONN_ACTION
        menu.addAction(QAction(get_icon(open_menu_name), open_menu_name.format(self.conn_name), menu))
        # 测试连接、取消测试连接
        test_conn_menu = CANCEL_TEST_CONN_ACTION \
            if get_item_testing_flag(self.item) else TEST_CONN_ACTION
        menu.addAction(QAction(get_icon(test_conn_menu), test_conn_menu.format(self.conn_name), menu))
        # 编辑连接
        menu.addAction(QAction(get_icon(EDIT_CONN_ACTION), EDIT_CONN_ACTION.format(self.conn_name), menu))
        menu.addSeparator()

        # 删除连接
        menu.addAction(QAction(get_icon(DEL_CONN_ACTION), DEL_CONN_ACTION.format(self.conn_name), menu))

    def test_conn(self):
        set_item_testing_flag(self.item, True)
        self.test_conn_executor = TestConnIconMovieExecutor(self.item, self.window,
                                                            self.test_conn_success, self.test_conn_fail)
        # 将测试连接的线程执行器绑定到item中
        set_item_testing_worker(self.item, self.test_conn_executor)
        self.test_conn_executor.start()

    def test_conn_success(self):
        set_item_testing_flag(self.item, False)
        pop_ok(f'[{self.conn_name}]\n{TEST_CONN_SUCCESS_PROMPT}', TEST_CONN_TITLE, self.window)

    def test_conn_fail(self):
        set_item_testing_flag(self.item, False)

    def handle_menu_func(self, func):
        # 打开连接
        if func == OPEN_CONN_ACTION.format(self.conn_name):
            self.open_item()
        # 取消打开连接
        elif func == CANCEL_OPEN_CONN_ACTION.format(self.conn_name):
            get_item_opening_worker(self.item).worker_terminate(self.open_item_fail)
        # 关闭连接
        elif func == CLOSE_CONN_ACTION.format(self.conn_name):
            pass
        # 测试连接
        elif func == TEST_CONN_ACTION.format(self.conn_name):
            self.test_conn()
        # 取消测试连接
        elif func == CANCEL_TEST_CONN_ACTION.format(self.conn_name):
            get_item_testing_worker(self.item).worker_terminate(self.test_conn_fail)
        # 编辑连接
        elif func == EDIT_CONN_ACTION.format(self.conn_name):
            edit_conn_func(get_item_conn_type(self.item).display_name, self.tree_widget,
                           self.window.geometry(), get_item_sql_conn(self.item))
        # 删除连接
        elif func == DEL_CONN_ACTION.format(self.conn_name):
            pass
