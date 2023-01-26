# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction

from constant.constant import CANCEL_OPEN_TABLE_MENU, OPEN_TABLE_MENU, CLOSE_TABLE_MENU, REFRESH_ACTION
from constant.icon_enum import get_icon
from service.async_func.async_sql_ds_task import OpenTBExecutor, RefreshTBExecutor
from view.box.message_box import pop_fail, pop_question
from view.tab.tab_ui import TabTableUI
from view.tree.tree_item.sql_tree_node.abstract_sql_tree_node import AbstractSqlTreeNode
from view.tree.tree_item.tree_item_func import get_item_opened_tab, \
    set_item_opened_tab, link_table_checkbox, save_tree_data, get_add_del_data

_author_ = 'luwt'
_date_ = '2022/7/6 22:05'


class TableTreeNode(AbstractSqlTreeNode):

    def __init__(self, *args):
        super().__init__(*args)
        self.table_name = self.item.text(0)
        self.open_tb_executor: OpenTBExecutor = ...
        self.refresh_tb_executor: RefreshTBExecutor = ...

    def open_item(self):
        # 获取打开的tab
        tab_widget = get_item_opened_tab(self.item)
        # 如果存在打开的tab，展示到当前页
        if tab_widget:
            self.window.sql_tab_widget.setCurrentWidget(tab_widget)
        else:
            # 执行打开tab页, 设置正在打开中状态
            self.is_opening = True
            self.open_tb_executor = OpenTBExecutor(self.item, self.window, self.open_item_ui, self.open_item_fail)
            self.open_tb_executor.start()

    def open_item_ui(self, table_tab):
        tab = self.reopen_item(table_tab)
        self.window.sql_tab_widget.setCurrentWidget(tab)
        self.is_opening = False

    def reopen_item(self, table_tab):
        # 创建tab页
        tab = TabTableUI(self.window, table_tab, self.item)
        self.window.sql_tab_widget.addTab(tab, self.table_name)
        # 记录tab对象
        set_item_opened_tab(self.item, tab)
        # 连接表头复选框变化信号
        tab.table_frame.table_widget.table_header.header_check_state_changed.connect(
            lambda check_state: self.set_check_state(check_state))
        return tab

    def open_item_fail(self):
        self.is_opening = False

    def close_item(self):
        tab = get_item_opened_tab(self.item)
        if tab:
            index = self.window.sql_tab_widget.indexOf(tab)
            tab_bar = self.window.sql_tab_widget.tab_bar
            if tab_bar.table_allow_close((index, )):
                # 删除tab
                tab_bar.remove_tab(index)

    def change_check_box(self, check_state, clicked):
        # 保存复选框状态变化
        self.save_check_state()
        # 联动表格内的复选框
        link_table_checkbox(self.item, check_state)

    def save_check_state(self):
        # 保存选中数据
        save_tree_data(self.item, self.tree_widget.tree_data)
        self.tree_widget.item_changed_executor.item_checked(self.item)

    def set_check_state(self, check_state):
        # 当表格表头变化，联动当前节点表头复选框变化
        self.item.setCheckState(0, check_state)
        self.save_check_state()

    def do_fill_menu(self, menu):
        open_menu_name = CANCEL_OPEN_TABLE_MENU.format(self.table_name) \
            if self.is_opening else OPEN_TABLE_MENU.format(self.table_name) \
            if not get_item_opened_tab(self.item) else CLOSE_TABLE_MENU.format(self.table_name)

        menu.addAction(QAction(open_menu_name.format(self.table_name), menu))

        # 刷新
        menu.addSeparator()
        menu.addAction(QAction(get_icon(REFRESH_ACTION), f'{REFRESH_ACTION}表[{self.table_name}]', menu))

    def handle_menu_func(self, func):
        # 打开表
        if func == OPEN_TABLE_MENU.format(self.table_name):
            self.open_item()
        # 取消打开表
        elif func == CANCEL_OPEN_TABLE_MENU.format(self.table_name):
            self.open_tb_executor.worker_terminate(self.open_item_fail)
        # 关闭表
        elif func == CLOSE_TABLE_MENU.format(self.table_name):
            self.close_item()
        # 刷新
        elif func == f'{REFRESH_ACTION}表[{self.table_name}]':
            self.refresh()

    def close_tab_callback(self):
        # 如果选中了数据，那么清空列数据，提供给tab bar调用，在关闭tab时调用
        if self.item.checkState(0):
            del_data = get_add_del_data(self.item)
            self.tree_widget.tree_data.clear_node_children(del_data)

    def refresh(self):
        if self.is_refreshing:
            return
        self.is_refreshing = True
        # 刷新表
        self.refresh_tb_executor = RefreshTBExecutor(self.item, get_item_opened_tab(self.item), self.window,
                                                     self.refresh_success, self.refresh_fail)
        self.refresh_tb_executor.start()

    def refresh_success(self, table_tab):
        if table_tab:
            # 开始刷新tab页面
            tab = get_item_opened_tab(self.item)
            tab.refresh_ui(table_tab)
            # 连接表头复选框变化信号
            tab.table_frame.table_widget.table_header.header_check_state_changed.connect(
                lambda check_state: self.set_check_state(check_state))
        # 将当前项置为非选中
        self.item.setCheckState(0, Qt.Unchecked)
        self.tree_widget.item_changed_executor.item_checked(self.item)
        # 清空选中数据
        del_data = get_add_del_data(self.item)
        self.tree_widget.tree_data.del_node(del_data)
        self.is_refreshing = False

    def refresh_fail(self):
        # 清空数据
        self.close_item()
        # 清空选中数据
        del_data = get_add_del_data(self.item)
        self.tree_widget.tree_data.del_node(del_data)
        # 删除当前元素
        parent_item = self.item.parent()
        parent_item.removeChild(self.item)
        # 如果上级节点没有子节点，将状态置为收起
        if not parent_item.childCount():
            parent_item.setExpanded(False)
        self.is_refreshing = False

    def worker_terminate(self):
        if self.open_tb_executor is not Ellipsis:
            self.open_tb_executor.worker_terminate()
