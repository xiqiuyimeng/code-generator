# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem

from constant.constant import OPEN_CONN_MENU, CANCEL_OPEN_CONN_MENU, CLOSE_CONN_MENU, CANCEL_TEST_CONN_MENU, \
    TEST_CONN_MENU, ADD_CONN_MENU, EDIT_CONN_MENU, DEL_CONN_MENU, CANCEL_OPEN_DB_MENU, OPEN_DB_MENU, CLOSE_DB_MENU, \
    CANCEL_OPEN_TABLE_MENU, OPEN_TABLE_MENU, CLOSE_TABLE_MENU, TEST_CONN_TITLE, TEST_CONN_SUCCESS_PROMPT, OPEN_TB_TITLE, \
    NO_TBS_PROMPT
from service.async_func.async_mysql_task import OpenConnExecutor, OpenDBExecutor, OpenTBExecutor, \
    TestConnIconMovieExecutor
from view.box.message_box import pop_fail, pop_ok
from view.table.table_function import fill_table, resize_table_rows
from view.tree.tree_function import make_db_items, make_table_items, add_conn_func, edit_conn_func

_author_ = 'luwt'
_date_ = '2022/5/31 18:14'


def get_tree_node(item, tree_widget, window):
    """
    获取树节点对应的实例化对象。
    树结构：
        树的根：树的顶层
            连接：第一级，父节点为根
                数据库：第二级，父节点为连接
                    表：第三级，父节点为库
    目前树的根节点为空，所以可以根据这一特性发现当前节点的层级，
    从而返回相应的实例
    """
    # 如果父级为空，那么则为连接
    if item.parent() is None:
        return TreeNodeConn(item, tree_widget, window)
    elif item.parent().parent() is None:
        return TreeNodeDB(item, tree_widget, window)
    elif item.parent().parent().parent() is None:
        return TreeNodeTable(item, tree_widget, window)


class Context:

    def __init__(self, *args):
        self.tree_node = get_tree_node(*args)

    def open_item(self):
        return self.tree_node.open_item()

    def close_item(self):
        return self.tree_node.close_item()

    def change_check_box(self, check_state):
        return self.tree_node.change_check_box(check_state)

    def get_menu_names(self):
        return self.tree_node.get_menu_names()

    def handle_menu_func(self, func):
        return self.tree_node.handle_menu_func(func)


class TreeNodeAbstract:

    def __init__(self, item: QTreeWidgetItem, tree_widget, window):
        self.item = item
        self.tree_widget = tree_widget
        self.window = window

    def open_item(self): ...

    def open_item_ui(self, *args): ...

    def open_item_fail(self): ...

    def close_item(self): ...

    def change_check_box(self, check_state): ...

    def get_menu_names(self): ...

    def handle_menu_func(self, func): ...


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

    def close_item(self): ...
    
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
    
    def close_item(self): ...
    
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
    

class TreeNodeTable(TreeNodeAbstract):

    def __init__(self, *args):
        super().__init__(*args)
        self.table_name = self.item.text(0)
        self.open_tb_executor = ...

    def open_item(self):
        # 如果当前节点没有打开表，在执行打开
        if self.window.table_widget.tree_item is not self.item:
            # 设置正在打开中状态
            self.item.setData(1, Qt.UserRole, True)
            self.window.table_widget.tree_item = self.item
            self.open_tb_executor = OpenTBExecutor(self.item, self.window, self.open_item_ui, self.open_item_fail)
            # 将打开连接的线程执行器绑定到item中
            self.item.setData(1, Qt.UserRole + 1, self.open_tb_executor)
            self.open_tb_executor.start()

    def open_item_ui(self, column_list):
        self.item.setData(1, Qt.UserRole, False)
        self.window.table_frame.setHidden(False)
        fill_table(self.window.table_widget, column_list)

    def open_item_fail(self):
        self.item.setData(1, Qt.UserRole, False)

    def close_item(self):
        self.window.table_frame.setHidden(True)
        # 将表格行数置位0
        resize_table_rows(0, self.window.table_widget)
        self.window.table_widget.tree_item = None
    
    def change_check_box(self, check_state): ...
    
    def get_menu_names(self):
        return [
            # 根据是否在打开中标识
            CANCEL_OPEN_TABLE_MENU.format(self.table_name)
            if self.item.data(1, Qt.UserRole) else OPEN_TABLE_MENU.format(self.table_name)
            if self.window.table_widget.tree_item is not self.item else CLOSE_TABLE_MENU.format(self.table_name)
        ]
    
    def handle_menu_func(self, func):
        # 打开表
        if func == OPEN_TABLE_MENU.format(self.table_name):
            self.open_item()
        # 取消打开表
        elif func == CANCEL_OPEN_TABLE_MENU.format(self.table_name):
            self.item.data(1, Qt.UserRole + 1).worker_terminate(self.open_item_fail)
        # 关闭表
        elif func == CLOSE_TABLE_MENU.format(self.table_name):
            pass
