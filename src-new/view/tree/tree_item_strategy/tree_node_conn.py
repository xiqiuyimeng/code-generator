# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt

from constant.constant import CANCEL_OPEN_CONN_MENU, OPEN_CONN_MENU, CLOSE_CONN_MENU, CANCEL_TEST_CONN_MENU, \
    TEST_CONN_MENU, ADD_CONN_MENU, EDIT_CONN_MENU, DEL_CONN_MENU, TEST_CONN_SUCCESS_PROMPT, TEST_CONN_TITLE
from service.async_func.async_mysql_task import OpenConnExecutor, TestConnIconMovieExecutor
from view.box.message_box import pop_ok
from view.tree.tree_function import make_db_items, add_conn_func, edit_conn_func
from view.tree.tree_item_strategy.tree_node_abstract import TreeNodeAbstract

_author_ = 'luwt'
_date_ = '2022/7/6 22:04'


class TreeNodeConn(TreeNodeAbstract):

    def __init__(self, *args):
        super().__init__(*args)
        self.conn_name = self.item.text(0)
        self.open_conn_executor: OpenConnExecutor = ...
        self.test_conn_executor: TestConnIconMovieExecutor = ...

    def open_item(self):
        if not self.item.childCount():
            # 设置正在打开中状态
            self.item.setData(1, Qt.UserRole, True)
            self.open_conn_executor = OpenConnExecutor(self.item, self.window, self.open_item_ui, self.open_item_fail)
            # 将打开连接的线程执行器绑定到item中
            self.item.setData(1, Qt.UserRole + 1, self.open_conn_executor)
            self.open_conn_executor.start()
        self.tree_widget.set_selected_focus(self.item)

    def open_item_ui(self, db_names):
        self.item.setData(1, Qt.UserRole, False)
        make_db_items(self.tree_widget, self.item, db_names)
        self.item.setExpanded(True)
        self.tree_widget.set_selected_focus(self.item)

    def open_item_fail(self):
        self.item.setData(1, Qt.UserRole, False)

    def close_item(self):
        ...

    def get_menu_names(self):
        return [
            # 根据是否在打开中标识
            CANCEL_OPEN_CONN_MENU.format(self.conn_name)
            if self.item.data(1, Qt.UserRole) else OPEN_CONN_MENU.format(self.conn_name)
            if not self.item.childCount() else CLOSE_CONN_MENU.format(self.conn_name),
            # 根据是否在测试中标识
            CANCEL_TEST_CONN_MENU.format(self.conn_name)
            if self.item.data(2, Qt.UserRole) else TEST_CONN_MENU.format(self.conn_name),
            ADD_CONN_MENU,
            EDIT_CONN_MENU.format(self.conn_name),
            DEL_CONN_MENU.format(self.conn_name),
        ]

    def test_conn(self):
        self.item.setData(2, Qt.UserRole, True)
        self.test_conn_executor = TestConnIconMovieExecutor(self.item, self.window,
                                                            self.test_conn_success, self.test_conn_fail)
        # 将测试连接的线程执行器绑定到item中
        self.item.setData(2, Qt.UserRole + 1, self.test_conn_executor)
        self.test_conn_executor.start()

    def test_conn_success(self):
        self.item.setData(2, Qt.UserRole, False)
        pop_ok(f'[{self.conn_name}]\n{TEST_CONN_SUCCESS_PROMPT}', TEST_CONN_TITLE, self.window)

    def test_conn_fail(self):
        self.item.setData(2, Qt.UserRole, False)

    def handle_menu_func(self, func):
        # 打开连接
        if func == OPEN_CONN_MENU.format(self.conn_name):
            self.open_item()
        # 取消打开连接
        elif func == CANCEL_OPEN_CONN_MENU.format(self.conn_name):
            self.item.data(1, Qt.UserRole + 1).worker_terminate(self.open_item_fail)
        # 关闭连接
        elif func == CLOSE_CONN_MENU.format(self.conn_name):
            pass
        # 测试连接
        elif func == TEST_CONN_MENU.format(self.conn_name):
            self.test_conn()
        # 取消测试连接
        elif func == CANCEL_TEST_CONN_MENU.format(self.conn_name):
            self.item.data(2, Qt.UserRole + 1).worker_terminate(self.test_conn_fail)
        # 添加连接
        elif func == ADD_CONN_MENU:
            add_conn_func(self.tree_widget, self.window.geometry())
        # 编辑连接
        elif func == EDIT_CONN_MENU.format(self.conn_name):
            edit_conn_func(self.tree_widget, self.window.geometry(), self.item.data(0, Qt.UserRole))
        # 删除连接
        elif func == DEL_CONN_MENU.format(self.conn_name):
            pass
