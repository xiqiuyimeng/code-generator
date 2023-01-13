# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QAction

from constant.constant import EDIT_STRUCT_ACTION, DEL_STRUCT_ACTION, CANCEL_OPEN_STRUCT_ACTION, OPEN_STRUCT_ACTION, \
    CLOSE_STRUCT_ACTION, EDIT_STRUCT_PROMPT, DEL_STRUCT_PROMPT, REFRESH_ACTION
from constant.icon_enum import get_icon
from service.async_func.async_struct_executor import *
from service.async_func.async_struct_task import DelStructExecutor
from view.box.message_box import pop_question
from view.tab.tab_ui import TabTableUI
from view.tree.tree_item.struct_tree_node.abstract_struct_tree_node import AbstractStructTreeNode
from view.tree.tree_item.tree_item_func import get_item_opened_tab, set_item_opened_tab, \
    link_table_checkbox, save_tree_data, get_add_del_data
from view.tree.tree_widget.tree_function import edit_struct_func

_author_ = 'luwt'
_date_ = '2022/12/2 12:09'


class StructTreeNode(AbstractStructTreeNode):

    def __init__(self, *args):
        super().__init__(*args)
        self.item_name = self.item.text(0)
        self.open_struct_executor: OpenStructExecutor = ...
        self.del_struct_executor: DelStructExecutor = ...
        self.is_opening = False

    def open_item(self):
        # 获取打开的tab
        tab_widget = get_item_opened_tab(self.item)
        # 如果存在打开的tab，展示到当前页
        if tab_widget:
            self.window.struct_tab_widget.setCurrentWidget(tab_widget)
        else:
            # 执行打开tab页, 设置正在打开中状态
            self.is_opening = True
            self.open_struct_executor = globals()[self.opened_item.data_type.parse_executor](
                self.item, self.window, self.open_item_ui, self.open_item_fail)
            self.open_struct_executor.start()

    def open_item_ui(self, table_tab):
        tab = self.reopen_item(table_tab)
        self.window.struct_tab_widget.setCurrentWidget(tab)
        self.is_opening = False

    def open_item_fail(self):
        self.is_opening = False

    def reopen_item(self, table_tab):
        # 创建tab页
        tab = TabTableUI(self.window, table_tab, self.item)
        self.window.struct_tab_widget.addTab(tab, self.item_name)
        # 记录tab对象
        set_item_opened_tab(self.item, tab)
        # 连接表头复选框变化信号
        tab.table_frame.table_widget.table_header.header_check_state_changed.connect(
            lambda check_state: self.set_check_state(check_state))
        return tab

    def close_item(self):
        tab = get_item_opened_tab(self.item)
        if tab:
            index = self.window.struct_tab_widget.indexOf(tab)
            tab_bar = self.window.struct_tab_widget.tab_bar
            if tab_bar.table_allow_close((index,)):
                # 删除tab
                tab_bar.remove_tab(index)
            else:
                return
        return True

    def change_check_box(self, check_state, clicked):
        # 保存复选框状态变化
        self.save_check_state()
        # 联动表格内的复选框
        link_table_checkbox(self.item, check_state)
        # 如果是点击，联动父节点变化
        if clicked:
            self.link_parent_node()

    def do_fill_menu(self, menu):
        # 打开
        open_struct_action = CANCEL_OPEN_STRUCT_ACTION \
            if self.is_opening else OPEN_STRUCT_ACTION \
            if not get_item_opened_tab(self.item) else CLOSE_STRUCT_ACTION
        menu.addAction(QAction(get_icon(open_struct_action), open_struct_action.format(self.item_name), menu))
        menu.addSeparator()

        # 编辑
        menu.addAction(QAction(get_icon(EDIT_STRUCT_ACTION),
                               EDIT_STRUCT_ACTION.format(self.item_name), menu))
        # 删除
        menu.addAction(QAction(get_icon(DEL_STRUCT_ACTION),
                               DEL_STRUCT_ACTION.format(self.item_name), menu))
        # 刷新
        menu.addSeparator()
        menu.addAction(QAction(get_icon(REFRESH_ACTION), f'{REFRESH_ACTION}结构体[{self.item_name}]', menu))

    def handle_menu_func(self, func):
        # 打开结构体
        if func == OPEN_STRUCT_ACTION.format(self.item_name):
            self.open_item()
        # 取消打开结构体
        elif func == CANCEL_OPEN_STRUCT_ACTION.format(self.item_name):
            self.open_struct_executor.worker_terminate(self.open_item_fail)
        # 关闭结构体
        elif func == CLOSE_STRUCT_ACTION.format(self.item_name):
            self.close_item()
        # 编辑结构体
        elif func == EDIT_STRUCT_ACTION.format(self.item_name):
            self.edit_struct()
        # 删除结构体
        elif func == DEL_STRUCT_ACTION.format(self.item_name):
            if pop_question(DEL_STRUCT_PROMPT, DEL_STRUCT_ACTION.format(self.item_name), self.window) \
                    and self.close_item():
                self.del_struct()
        # 刷新
        elif func == REFRESH_ACTION.format(self.item_name):
            self.refresh()

    def edit_struct(self):
        # 如果结构体已经打开，先关闭，再进行编辑
        editable = False
        if get_item_opened_tab(self.item):
            if pop_question(EDIT_STRUCT_PROMPT, EDIT_STRUCT_ACTION.format(self.item_name), self.window) \
                    and self.close_item():
                editable = True
        else:
            editable = True

        if editable:
            edit_struct_func(self.opened_item.data_type.display_name, self.tree_widget,
                             self.window.geometry(), self.opened_item.id)

    def del_struct(self):
        # 删除结构体后，应该对同级别的其他项进行重排序
        reorder_items = self.get_need_reorder_items()
        self.del_struct_executor = DelStructExecutor(self.item, self.opened_item, reorder_items,
                                                     self.del_struct_callback, self.window)
        self.del_struct_executor.start()

    def del_struct_callback(self):
        self.worker_terminate()
        self.del_callback()

    def close_tab_callback(self):
        # 清空列数据，提供给tab bar调用，在关闭tab时调用
        if self.item.checkState(0):
            del_data = get_add_del_data(self.item)
            self.tree_widget.tree_data.clear_node_children(del_data)

    def set_check_state(self, check_state):
        # 结构体表头复选框联动方法
        self.item.setCheckState(0, check_state)
        self.save_check_state()
        # 联动父节点变化
        self.link_parent_node()

    def worker_terminate(self):
        if self.open_struct_executor is not Ellipsis:
            self.open_struct_executor.worker_terminate()

    def refresh(self): ...
