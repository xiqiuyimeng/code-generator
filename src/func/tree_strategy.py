# -*- coding: utf-8 -*-
"""
处理所有关于树节点的操作
    双击节点事件
    右键菜单生成菜单及菜单动作
    列表复选框
"""

from abc import ABC, abstractmethod

from PyQt5.QtCore import Qt

from src.constant.constant import OPEN_CONN_MENU, CLOSE_CONN_MENU, TEST_CONN_MENU, ADD_CONN_MENU, EDIT_CONN_MENU, \
    DEL_CONN_MENU, CLOSE_CONN_PROMPT, EDIT_CONN_WITH_FIELD_PROMPT, EDIT_CONN_PROMPT, DEL_CONN_WITH_FIELD_PROMPT, \
    DEL_CONN_PROMPT, OPEN_DB_MENU, CLOSE_DB_MENU, SELECT_ALL_TB_MENU, UNSELECT_TB_MENU, CLOSE_DB_PROMPT, \
    OPEN_TABLE_MENU, CLOSE_TABLE_MENU, SELECT_ALL_FIELD_MENU, UNSELECT_FIELD_MENU
from src.func.connection_function import close_connection
from src.func.gui_function import check_table_status, set_children_check_state
from src.func.open_conn_thread import AsyncOpenConn
from src.func.select_table_thread import AsyncSelectTable
from src.func.selected_data import SelectedData
from src.func.table_func import change_table_checkbox, close_table, check_table_opened
from src.func.test_conn_thread import AsyncTestConn
from src.func.tree_function import show_conn_dialog, add_conn_func
from src.little_widget.message_box import pop_question
from src.little_widget.right_menu import get_conn_menu_names, get_db_menu_names, get_table_menu_names
from src.sys.sys_info_storage.conn_sqlite import ConnSqlite

_author_ = 'luwt'
_date_ = '2020/6/23 16:21'


def tree_node_factory(item):
    """
    获取树节点对应的实例化对象。
    树结构：
        树的根：树的顶层
            连接：第一级，父节点为根
                数据库：第二级，父节点为连接
                    表：第三级，父节点为库
    目前树的根节点为空，所以可以根据这一特性发现当前节点的层级，
    从而返回相应的实例
    :param item: 当前的元素
    """
    # 如果父级为空，那么则为连接
    if item.parent() is None:
        return TreeNodeConn()
    elif item.parent().parent() is None:
        return TreeNodeDB()
    elif item.parent().parent().parent() is None:
        return TreeNodeTable()


class Context:

    def __init__(self, tree_node):
        self.tree_node = tree_node

    def open_item(self, item, gui):
        return self.tree_node.open_item(item, gui)

    def close_item(self, item, gui):
        return self.tree_node.close_item(item, gui)

    def change_check_box(self, item, check_state, gui):
        return self.tree_node.change_check_box(item, check_state, gui)

    def get_menu_names(self, item, gui):
        return self.tree_node.get_menu_names(item, gui)

    def handle_menu_func(self, item, func, gui):
        return self.tree_node.handle_menu_func(item, func, gui)


class TreeNodeAbstract(ABC):

    @abstractmethod
    def open_item(self, item, gui): ...

    @abstractmethod
    def close_item(self, item, gui): ...

    @abstractmethod
    def change_check_box(self, item, check_state, gui): ...

    @abstractmethod
    def get_menu_names(self, item, gui): ...

    @abstractmethod
    def handle_menu_func(self, item, func, gui): ...


class TreeNodeConn(TreeNodeAbstract, ABC):

    def open_item(self, item, gui):
        """
        打开连接，展示连接下的所有库列表
        :param item: 当前点击树节点元素
        :param gui: 启动的主窗口界面对象
        """
        # 仅当子元素不存在时，获取子元素并填充
        if item.childCount() == 0:
            # 连接的id，连接名称
            conn_id, conn_name = TreeNodeConn.get_node_info(item)
            open_conn = AsyncOpenConn(gui, item, conn_id, conn_name)
            open_conn.connect_db()

    def close_item(self, item, gui):
        """
        关闭树的某项，将其下所有子项移除，并将扩展状态置为false
        :param item: 当前点击树节点元素
        :param gui: 启动的主窗口界面对象
        """
        TreeNodeDB().close_item(item, gui)
        item.setExpanded(False)

    def change_check_box(self, item, check_state, gui): ...

    def get_menu_names(self, item, gui):
        """
        获取树中，第一级连接项的右键菜单名字列表
        :param item: 当前点击树节点元素
        :param gui: 启动的主窗口界面对象
        """
        return get_conn_menu_names(item)

    def handle_menu_func(self, item, func, gui):
        """
        在连接层，右键菜单的功能实现
        :param item: 当前点击树节点元素
        :param func: 右键菜单中功能名称
        :param gui: 启动的主窗口界面对象
        """
        # 获取当前选中的连接id，连接名称
        conn_id, conn_name = self.get_node_info(item)
        # 打开连接
        if func == OPEN_CONN_MENU:
            self.open_item(item, gui)
            item.setExpanded(True)
        # 关闭连接
        elif func == CLOSE_CONN_MENU:
            if self.close_conn(conn_name, func, gui):
                self.close_item(item, gui)
        # 测试连接
        elif func == TEST_CONN_MENU:
            self.test_conn(gui.display_conn_dict.get(conn_id), item)
        # 添加连接
        elif func == ADD_CONN_MENU:
            add_conn_func(gui, gui.screen_rect)
        # 编辑连接
        elif func == EDIT_CONN_MENU:
            self.edit_conn(func, gui, conn_name, conn_id, item)
        # 删除连接
        elif func == DEL_CONN_MENU:
            self.del_conn(func, gui, conn_name, conn_id, item)

    def test_conn(self, conn, item):
        test_conn = AsyncTestConn(conn, TEST_CONN_MENU, item)
        test_conn.test_conn()

    @staticmethod
    def close_conn(conn_name, func, gui):
        """
        关闭数据连接，关闭特定连接，name为标识，
        如果在此连接下已选择了字段。那么弹窗确认是否关闭，
        如果关闭将清空此连接所选的字段
        :param conn_name: 连接名称
        :param func: 功能名称，用于展示在弹窗标题处
        :param gui: 启动的主窗口界面对象
        """
        if SelectedData().get_db_dict(conn_name, True):
            reply = pop_question(func, CLOSE_CONN_PROMPT)
            if reply:
                SelectedData().unset_conn(conn_name)
            else:
                return False
        close_connection(gui, conn_name)
        return True

    def edit_conn(self, func, gui, conn_name, conn_id, item):
        """
        编辑连接，首先需要判断连接是否打开，
        如果打开，进一步判断是否有选中的字段数据，如果有，
        则弹窗提示需要先关闭连接并清空字段。
        如果没有选中字段，则弹窗需要关闭连接。
        否则直接弹编辑窗口
        :param func: 功能名称
        :param gui: 启动的主窗口界面对象
        :param conn_name: 连接名称
        :param conn_id: 连接id
        :param item: 当前点击树节点元素
        """
        # 先判断是否打开
        if item.isExpanded():
            # 再判断是否有选中字段
            if SelectedData().get_db_dict(conn_name, True):
                if pop_question(func, EDIT_CONN_WITH_FIELD_PROMPT):
                    SelectedData().unset_conn(conn_name)
                    # 关闭连接
                    close_connection(gui, conn_name)
                    self.close_item(item, gui)
                else:
                    return
            else:
                if pop_question(func, EDIT_CONN_PROMPT):
                    # 关闭连接
                    close_connection(gui, conn_name)
                    self.close_item(item, gui)
                else:
                    return
        conn_info = gui.display_conn_dict.get(conn_id)
        show_conn_dialog(gui, conn_info, func, gui.screen_rect)

    def del_conn(self, func, gui, conn_name, conn_id, item):
        """
        删除连接，如果连接下有选择字段，弹窗确认是否清空字段并删除连接，
        否则弹窗是否删除连接
        :param func: 功能名称
        :param gui: 启动的主窗口界面对象
        :param conn_name: 连接名称
        :param conn_id: 连接id
        :param item: 当前点击树节点元素
        """
        # 判断是否有选择字段
        if SelectedData().get_db_dict(conn_name, True):
            if pop_question(func, DEL_CONN_WITH_FIELD_PROMPT):
                SelectedData().unset_conn(conn_name)
                self.close_and_delete_conn(gui, conn_name, conn_id, item)
        else:
            # 弹出关闭连接确认框
            if pop_question(func, DEL_CONN_PROMPT):
                self.close_and_delete_conn(gui, conn_name, conn_id, item)

    def close_and_delete_conn(self, gui, conn_name, conn_id, item):
        """
        关闭连接，删除连接
        :param gui: 启动的主窗口界面对象
        :param conn_name: 连接名称
        :param conn_id: 连接id
        :param item: 当前点击树节点元素
        """
        self.close_item(item, gui)
        # 关闭连接
        close_connection(gui, conn_name)
        conn_info = gui.display_conn_dict[conn_id]
        ConnSqlite().delete(conn_info.id)
        del gui.display_conn_dict[conn_id]
        # 删除树元素
        # 树型部件的takeTopLevelItem方法可以从树型部件中删除对应项的节点并返回该项，语法：takeTopLevelItem(index)
        # 通过调用树型部件的indexOfTopLevelItem方法可以获得对应项在顶层项的位置，语法：indexOfTopLevelItem
        #
        # self.treeWidget.removeItemWidget，它从一个项中移除一个小部件，而不是QTreeWidgetItem。它对应于setItemWidget方法
        gui.treeWidget.takeTopLevelItem(gui.treeWidget.indexOfTopLevelItem(item))

    @staticmethod
    def get_node_info(item):
        """获取连接id和连接名称"""
        conn_id = int(item.text(1))
        conn_name = item.text(0)
        return conn_id, conn_name


class TreeNodeDB(TreeNodeAbstract, ABC):

    def open_item(self, item, gui):
        """
        打开数据库，展示数据库下的所有表，
        并将表的复选框置为未选中
        :param item: 当前点击树节点元素
        :param gui: 启动的主窗口界面对象
        """
        # 仅当子元素不存在时，获取子元素并填充
        if item.childCount() == 0:
            # 获取连接id和名称，从而获取该连接的数据库操作对象
            conn_id, conn_name, db_name = TreeNodeDB.get_node_info(item)
            open_conn = AsyncOpenConn(gui, item, conn_id, conn_name, db_name)
            open_conn.connect_db()

    def close_item(self, item, gui):
        """
        关闭树的某项，将其下所有子项移除，并将扩展状态置为false
        :param item: 当前点击树节点元素
        :param gui: 启动的主窗口界面对象
        """
        # 关闭表格，由于当前item不是表，所以应该使用当前表对象（如果有的话）
        if hasattr(gui, 'table_frame'):
            TreeNodeTable().close_item(gui.current_table, gui)
        # 移除所有子项目
        item.takeChildren()
        item.setExpanded(False)

    def change_check_box(self, item, check_state, gui): ...

    def get_menu_names(self, item, gui):
        """
        获取树中，数据库项的右键菜单名字列表
        :param item: 当前点击树节点元素
        :param gui: 启动的主窗口界面对象
        """
        # 检查表的复选框状态
        check_state = check_table_status(item)
        return get_db_menu_names(item, check_state)

    def handle_menu_func(self, item, func, gui):
        """
        在数据库层，右键菜单的功能实现
        :param item: 当前点击树节点元素
        :param func: 右键菜单中功能名称
        :param gui: 启动的主窗口界面对象
        """
        conn_id, conn_name, db_name = TreeNodeDB.get_node_info(item)
        # 打开数据库
        if func == OPEN_DB_MENU:
            self.open_item(item, gui)
            item.setExpanded(True)
        # 关闭数据库
        elif func == CLOSE_DB_MENU:
            if self.close_db(item, func, conn_name, db_name, gui):
                self.close_item(item, gui)
        # 全选所有表
        elif func == SELECT_ALL_TB_MENU:
            select_table = AsyncSelectTable(gui, item, conn_id, conn_name, db_name)
            select_table.select_table()
        # 取消全选表
        elif func == UNSELECT_TB_MENU:
            # 将子节点都置为未选中状态
            set_children_check_state(item, Qt.Unchecked)
            # 清空容器中的值
            SelectedData().unset_tbs(gui, conn_name, db_name)
            if hasattr(gui, 'table_frame') and gui.current_table.parent() is item:
                change_table_checkbox(gui, gui.current_table, False)

    @staticmethod
    def close_db(item, func, conn_name, db_name, gui):
        """
        关闭数据库，如果此库下已选择了字段，弹窗确认是否关闭，
        如果关闭，将清空此库下所选字段
        :param item: 当前点击树节点元素，也就是库
        :param func: 功能名称，用于展示在弹窗标题处
        :param conn_name: 连接名称
        :param db_name: 库名称
        :param gui: 启动的主窗口界面对象
        """
        check_status = check_table_status(item)
        if any(check_status):
            if pop_question(func, CLOSE_DB_PROMPT):
                SelectedData().unset_db(gui, conn_name, db_name)
            else:
                return False
        return True

    @staticmethod
    def get_node_info(item):
        """获取连接id、连接名称、数据库名称"""
        conn_id = int(item.parent().text(1))
        conn_name = item.parent().text(0)
        db_name = item.text(0)
        return conn_id, conn_name, db_name


class TreeNodeTable(TreeNodeAbstract, ABC):

    def open_item(self, item, gui):
        """
        打开表，可获取表中所有列名信息，然后展示在表格控件中，
        列的复选框与表格的复选框联动
        :param item: 当前点击树节点元素
        :param gui: 启动的主窗口界面对象
        """
        # 如果当前展示的表存在且与欲打开之表不是同一表，先删除当前展示的表
        if hasattr(gui, 'table_frame') and gui.current_table is not item:
            close_table(gui)
        # 如果当前打开表是欲打开之表，什么都不需要做
        elif check_table_opened(gui, item):
            return
        conn_id, conn_name, db_name, tb_name = TreeNodeTable.get_node_info(item)
        open_conn = AsyncOpenConn(gui, item, conn_id, conn_name, db_name, tb_name)
        open_conn.connect_db()

    def close_item(self, item, gui):
        """
        关闭右侧表格
        :param item: 当前点击树节点元素
        :param gui: 启动的主窗口界面对象
        """
        if check_table_opened(gui, item):
            # 关闭表格
            close_table(gui)

    def change_check_box(self, item, check_state, gui):
        """
        修改复选框状态，当前元素复选框状态应与表格控件中的复选框联动
        :param item: 当前点击树节点元素
        :param check_state: 复选框选中状态：全选、部分选、未选择
        :param gui: 启动的主窗口界面对象
        """
        conn_id, conn_name, db_name, tb_name = TreeNodeTable.get_node_info(item)
        # 如果表已经选中，那么右侧表格需全选字段
        if check_state == Qt.Checked:
            select_table = AsyncSelectTable(gui, item, conn_id, conn_name, db_name, tb_name)
            select_table.select_table()
        # 如果表未选中，那么右侧表格需清空选择
        elif check_state == Qt.Unchecked:
            # 从容器删除表名
            SelectedData().unset_tbs(gui, conn_name, db_name, tb_name)
            change_table_checkbox(gui, item, False)

    def get_menu_names(self, item, gui):
        """
        获取树中，表的右键菜单名字列表
        :param item: 当前点击树节点元素
        :param gui: 启动的主窗口界面对象
        """
        table_opened = hasattr(gui, 'table_frame') \
            and gui.table_header.isVisible() \
            and gui.current_table is item
        check_state = item.checkState(0)
        return get_table_menu_names(table_opened, check_state)

    def handle_menu_func(self, item, func, gui):
        """
        在表层，右键菜单的功能实现
        :param item: 当前点击树节点元素
        :param func: 右键菜单中功能名称
        :param gui: 启动的主窗口界面对象
        """
        # 打开表
        if func == OPEN_TABLE_MENU:
            self.open_item(item, gui)
        # 关闭表
        elif func == CLOSE_TABLE_MENU:
            close_table(gui)
        # 全选字段
        elif func == SELECT_ALL_FIELD_MENU:
            item.setCheckState(0, Qt.Checked)
            self.change_check_box(item, Qt.Checked, gui)
        # 取消选择字段
        elif func == UNSELECT_FIELD_MENU:
            item.setCheckState(0, Qt.Unchecked)
            self.change_check_box(item, Qt.Unchecked, gui)

    @staticmethod
    def get_node_info(item):
        """获取连接id，连接名称，数据库名，表名"""
        conn_id = int(item.parent().parent().text(1))
        conn_name = item.parent().parent().text(0)
        db_name = item.parent().text(0)
        tb_name = item.text(0)
        return conn_id, conn_name, db_name, tb_name

