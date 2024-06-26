# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt, QVariant

from src.constant.tree_constant import OPEN_TB_BOX_TITLE, CANCEL_OPEN_TABLE_ACTION, CANCEL_REFRESH_TB_ACTION, \
    OPEN_TABLE_ACTION, CLOSE_TABLE_ACTION, REFRESH_TB_ACTION, REFRESH_TB_BOX_TITLE
from src.enum.common_enum import get_checked_enum
from src.service.async_func.async_sql_ds_task import OpenTBExecutor, RefreshTBExecutor
from src.view.tree.tree_item.sql_tree_node.sql_tree_node_abc import SqlTreeNodeABC
from src.view.tree.tree_item.tree_item_func import get_item_opened_tab, link_table_checkbox, save_tree_data, \
    get_add_del_data, get_item_opened_record

_author_ = 'luwt'
_date_ = '2022/7/6 22:05'


class TableTreeNode(SqlTreeNodeABC):

    def __init__(self, *args):
        super().__init__(*args)
        self.open_tb_executor: OpenTBExecutor = ...
        self.refresh_tb_executor: RefreshTBExecutor = ...

    def open_item(self):
        # 获取打开的tab
        tab_widget = get_item_opened_tab(self.item)
        # 如果存在打开的tab，展示到当前页
        if tab_widget:
            self.tree_widget.get_current_tab_widget().setCurrentWidget(tab_widget)
        else:
            if self.is_opening:
                return
            # 执行打开tab页, 设置正在打开中状态
            self.is_opening = True
            # 将当前表的复选框隐藏
            self.hide_check_box()
            # 向上传递正在打开节点数变化
            self.tree_widget.get_item_node(self.item.parent()).add_opening_child_count()
            self.open_tb_executor = OpenTBExecutor(self.item, self.window, OPEN_TB_BOX_TITLE,
                                                   self.open_item_ui, self.open_item_fail)
            self.open_tb_executor.start()

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
            if tab_bar.check_tab_allow_close((index,)):
                # 删除tab
                tab_bar.remove_tab(index)

    def change_check_box(self, check_state, clicked):
        # 保存复选框状态变化
        if clicked:
            self.save_check_state()
        # 联动表格内的复选框
        return link_table_checkbox(self.item, check_state)

    def save_check_state(self):
        # 保存选中数据
        save_tree_data(self.item, self.tree_widget.tree_data)
        self.tree_widget.item_changed_executor.item_checked(self.item)

    def set_check_state(self, check_state):
        # 当表格表头变化，联动当前节点表头复选框变化
        self.item.setCheckState(0, check_state)
        self.save_check_state()

    def hide_check_box(self):
        # 隐藏复选框
        self.item.setData(0, Qt.ItemDataRole.CheckStateRole, QVariant())

    def show_check_box(self):
        # 显示复选框，选中状态根据 opened record 决定
        self.item.setCheckState(0, get_checked_enum(get_item_opened_record(self.item).checked))

    def do_fill_menu(self, menu):
        # 取消打开和取消刷新
        if self.add_cancel_open_refresh_menu(CANCEL_OPEN_TABLE_ACTION,
                                             CANCEL_REFRESH_TB_ACTION, menu):
            return
        # 添加打开或关闭菜单
        self.add_open_close_table_menu(OPEN_TABLE_ACTION, CLOSE_TABLE_ACTION, menu)

        # 刷新
        self.add_refresh_menu(REFRESH_TB_ACTION, menu)

    def handle_menu_func(self, func):
        # 打开表
        if func == OPEN_TABLE_ACTION.format(self.item_name):
            self.open_item()
        # 取消打开表
        elif func == CANCEL_OPEN_TABLE_ACTION.format(self.item_name):
            self.open_tb_executor.worker_terminate(self.open_item_fail)
        # 关闭表
        elif func == CLOSE_TABLE_ACTION.format(self.item_name):
            self.close_item()
        # 刷新
        elif func == REFRESH_TB_ACTION.format(self.item_name):
            self.refresh()
        # 取消刷新
        elif func == CANCEL_REFRESH_TB_ACTION.format(self.item_name):
            self.refresh_tb_executor.worker_terminate()

    def close_tab_callback(self):
        # 如果选中了数据，那么清空列数据，提供给tab bar调用，在关闭tab时调用
        check_state = self.item.checkState(0)
        if check_state == Qt.CheckState.Checked or check_state == Qt.CheckState.PartiallyChecked:
            del_data = get_add_del_data(self.item)
            self.tree_widget.tree_data.clear_node_children(del_data)

    def refresh(self):
        if self.is_refreshing or self.is_opening:
            return
        # 刷新表
        self.refresh_tb_executor = RefreshTBExecutor(self.tree_widget, self.item, self.window,
                                                     REFRESH_TB_BOX_TITLE, self.refresh_success,
                                                     self.refresh_fail)
        self.refresh_tb_executor.start()

    def refresh_success(self, table_tab):
        self.refresh_item_tab(table_tab, self.set_check_state)

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

    def worker_terminate(self):
        if self.open_tb_executor is not Ellipsis:
            self.open_tb_executor.worker_terminate()
