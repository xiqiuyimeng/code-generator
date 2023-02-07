# -*- coding: utf-8 -*-

from constant.constant import EDIT_STRUCT_ACTION, DEL_STRUCT_ACTION, CANCEL_OPEN_STRUCT_ACTION, OPEN_STRUCT_ACTION, \
    CLOSE_STRUCT_ACTION, EDIT_STRUCT_PROMPT, DEL_STRUCT_PROMPT, REFRESH_STRUCT_ACTION, \
    CANCEL_REFRESH_STRUCT_ACTION
from service.async_func.async_struct_executor.async_struct_executor import OpenStructExecutor, RefreshStructExecutor
from service.async_func.async_struct_task import DelStructExecutor
from view.box.message_box import pop_question
from view.tree.tree_item.struct_tree_node.abstract_struct_tree_node import AbstractStructTreeNode
from view.tree.tree_item.tree_item_func import get_item_opened_tab, link_table_checkbox, get_add_del_data, \
    get_item_opened_record
from view.tree.tree_widget.tree_function import edit_struct_func

_author_ = 'luwt'
_date_ = '2022/12/2 12:09'


class StructTreeNode(AbstractStructTreeNode):

    def __init__(self, *args):
        super().__init__(*args)
        self.open_struct_executor: OpenStructExecutor = ...
        self.del_struct_executor: DelStructExecutor = ...
        self.refresh_struct_executor: RefreshStructExecutor = ...

    def open_item(self):
        # 获取打开的tab
        tab_widget = get_item_opened_tab(self.item)
        # 如果存在打开的tab，展示到当前页
        if tab_widget:
            self.tree_widget.get_current_tab_widget().setCurrentWidget(tab_widget)
        else:
            if self.is_opening:
                return
            self.hide_check_box()
            # 执行打开tab页, 设置正在打开中状态
            self.is_opening = True
            self.tree_widget.get_item_node(self.item.parent()).add_opening_child_count()
            self.open_struct_executor = OpenStructExecutor(self.item, self.window,
                                                           self.open_item_ui,
                                                           self.open_item_fail)
            self.open_struct_executor.start()

    def open_item_ui(self, table_tab):
        tab = self.reopen_item(table_tab)
        self.tree_widget.get_current_tab_widget().setCurrentWidget(tab)
        self.is_opening = False
        self.tree_widget.get_item_node(self.item.parent()).sub_opening_child_count()
        self.show_check_box()

    def open_item_fail(self):
        super().open_item_fail()
        self.show_check_box()

    def reopen_item(self, table_tab):
        return self.reopen_tab(table_tab, self.item_name, self.set_check_state)

    def close_item(self):
        tab = get_item_opened_tab(self.item)
        if tab:
            index = self.tree_widget.get_current_tab_widget().indexOf(tab)
            tab_bar = self.tree_widget.get_current_tab_widget().tab_bar
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

    def show_check_box(self):
        # 显示复选框，选中状态根据 opened record 决定
        self.item.setCheckState(0, get_item_opened_record(self.item).checked)
        self.link_parent_node()

    def do_fill_menu(self, menu):
        # 取消打开和取消刷新
        if self.add_cancel_open_refresh_menu(CANCEL_OPEN_STRUCT_ACTION,
                                             CANCEL_REFRESH_STRUCT_ACTION, menu):
            return
        # 打开
        self.add_open_close_table_menu(OPEN_STRUCT_ACTION, CLOSE_STRUCT_ACTION, menu)
        menu.addSeparator()

        # 编辑
        self.add_menu(EDIT_STRUCT_ACTION, menu)
        # 删除
        self.add_menu(DEL_STRUCT_ACTION, menu)
        # 刷新
        menu.addSeparator()
        self.add_menu(REFRESH_STRUCT_ACTION, menu)

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
        elif func == REFRESH_STRUCT_ACTION.format(self.item_name):
            self.refresh()
        # 取消刷新
        elif func == CANCEL_REFRESH_STRUCT_ACTION.format(self.item_name):
            self.refresh_struct_executor.worker_terminate()

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
            opened_record = get_item_opened_record(self.item)
            edit_struct_func(opened_record.data_type.display_name, self.tree_widget,
                             self.window.geometry(), opened_record.id)

    def del_struct(self):
        # 删除结构体后，应该对同级别的其他项进行重排序
        reorder_items = self.get_need_reorder_items()
        self.del_struct_executor = DelStructExecutor(self.item, get_item_opened_record(self.item),
                                                     reorder_items, self.del_struct_callback, self.window)
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

    def refresh(self):
        if self.is_refreshing:
            return
        opened_tab = get_item_opened_tab(self.item)
        # 如果不存在打开表，那么无需处理
        if not opened_tab:
            return
        self.refresh_struct_executor = RefreshStructExecutor(self.tree_widget, self.item, self.window,
                                                             opened_tab.table_tab, self.refresh_success)
        self.refresh_struct_executor.start()

    def refresh_success(self, table_tab):
        self.refresh_item_tab(table_tab, self.set_check_state)
