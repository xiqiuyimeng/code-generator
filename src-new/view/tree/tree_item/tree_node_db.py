# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt

from constant.constant import NO_TBS_PROMPT, OPEN_TB_TITLE, CANCEL_OPEN_DB_MENU, OPEN_DB_MENU, CLOSE_DB_MENU, \
    SELECT_ALL_TB_MENU, UNSELECT_TB_MENU
from service.async_func.async_sql_ds_task import OpenDBExecutor
from view.box.message_box import pop_fail
from view.tree.tree_item.abstract_tree_node import AbstractTreeNode
from view.tree.tree_widget.tree_function import make_table_items, check_table_status, set_children_check_state
from view.tree.tree_widget.tree_item_func import set_item_opening_flag, set_item_opening_worker, get_item_opened_record

_author_ = 'luwt'
_date_ = '2022/7/6 22:04'


class DBTreeNode(AbstractTreeNode):

    def __init__(self, *args):
        super().__init__(*args)
        self.db_name = self.item.text(0)
        self.open_db_executor = ...

    def open_item(self):
        if not self.item.childCount():
            # 设置正在打开中状态
            set_item_opening_flag(self.item, True)
            self.open_db_executor = OpenDBExecutor(self.item, self.window, self.open_item_ui, self.open_item_fail)
            # 将打开连接的线程执行器绑定到item中
            set_item_opening_worker(self.item, self.open_db_executor)
            self.open_db_executor.start()
        self.tree_widget.set_selected_focus(self.item)

    def open_item_ui(self, opened_table_items):
        set_item_opening_flag(self.item, False)
        if opened_table_items:
            make_table_items(self.item, opened_table_items)
            self.item.setExpanded(True)
            self.tree_widget.set_selected_focus(self.item)
        else:
            pop_fail(NO_TBS_PROMPT.format(self.item.parent().text(0), self.db_name), OPEN_TB_TITLE, self.window)

    def open_item_fail(self):
        set_item_opening_flag(self.item, False)

    def reopen_item(self, opened_items):
        # 打开库下的表节点
        make_table_items(self.item, opened_items)
        opened_item_record = get_item_opened_record(self.item)
        self.item.setExpanded(opened_item_record.expanded)
        if opened_item_record.is_current:
            self.tree_widget.set_selected_focus(self.item)

    def close_item(self):
        ...

    def do_fill_menu(self, menu):
        menu_names = list()
        if self.item.childCount():
            check_state = check_table_status(self.item)
            menu_names.append(CLOSE_DB_MENU.format(self.db_name))
            # 全选时：添加取消选择菜单
            if check_state[0]:
                menu_names.append(UNSELECT_TB_MENU)
            # 部分选中时：添加全选菜单和取消选择菜单
            elif check_state[1]:
                menu_names.append(SELECT_ALL_TB_MENU)
                menu_names.append(UNSELECT_TB_MENU)
            else:
                # 都未选中时：添加全选菜单
                menu_names.append(SELECT_ALL_TB_MENU)
        # 根据打开标识判断是否正在打开中
        elif self.item.data(1, Qt.UserRole):
            menu_names.append(CANCEL_OPEN_DB_MENU.format(self.db_name))
        else:
            menu_names.append(OPEN_DB_MENU.format(self.db_name))
        return menu_names

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
        # 全选所有表
        elif func == SELECT_ALL_TB_MENU:
            tbs = set_children_check_state(self.item, Qt.Checked)
            # 首先删除已存储的信息
            del_data = {
                'conn': self.item.parent().text(0),
                'db': self.db_name
            }
            self.window.tree_data.del_node(del_data)
            # 再添加
            conn_info = self.item.parent().data(0, Qt.UserRole)
            add_data = {
                'conn': self.item.parent().text(0),
                'db': self.db_name,
                'tb': tbs
            }
            self.window.tree_data.add_node(add_data, conn_info)
        # 取消全选所有表
        elif func == UNSELECT_TB_MENU:
            set_children_check_state(self.item, Qt.Unchecked)
            del_data = {
                'conn': self.item.parent().text(0),
                'db': self.db_name
            }
            self.window.tree_data.del_node(del_data)
