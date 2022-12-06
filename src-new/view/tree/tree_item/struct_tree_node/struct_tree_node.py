# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QAction

from constant.constant import EDIT_STRUCT_ACTION, DEL_STRUCT_ACTION, CANCEL_OPEN_STRUCT_ACTION, OPEN_STRUCT_ACTION, \
    CLOSE_STRUCT_ACTION
from constant.icon_enum import get_icon
from service.async_func.struct_executor import *
from view.tree.tree_item.struct_tree_node.abstract_struct_tree_node import AbstractStructTreeNode
from view.tree.tree_item.tree_item_func import get_item_opened_record
from view.tree.tree_widget.tree_function import edit_struct_func

_author_ = 'luwt'
_date_ = '2022/12/2 12:09'


class StructTreeNode(AbstractStructTreeNode):

    def __init__(self, *args):
        super().__init__(*args)
        self.struct_name = self.item.text(0)
        if not hasattr(self, 'open_struct_executor'):
            self.open_struct_executor: OpenStructExecutor = ...
        if not hasattr(self, 'is_opening'):
            self.is_opening = False
        # 打开数据是不会变的
        if not hasattr(self, 'opened_item'):
            self.opened_item = get_item_opened_record(self.item)

    def open_item(self):
        super().open_item()

    def open_item_ui(self, *args):
        super().open_item_ui(*args)

    def open_item_fail(self):
        super().open_item_fail()

    def reopen_item(self, opened_items):
        super().reopen_item(opened_items)

    def close_item(self):
        super().close_item()

    def change_check_box(self, check_state):
        super().change_check_box(check_state)

    def do_fill_menu(self, menu):
        # 打开
        open_struct_action = CANCEL_OPEN_STRUCT_ACTION \
            if self.is_opening else OPEN_STRUCT_ACTION \
            if not self.item.childCount() else CLOSE_STRUCT_ACTION
        menu.addAction(QAction(get_icon(open_struct_action), open_struct_action.format(self.struct_name), menu))
        menu.addSeparator()

        # 编辑
        menu.addAction(QAction(get_icon(EDIT_STRUCT_ACTION),
                               EDIT_STRUCT_ACTION.format(self.struct_name), menu))
        # 删除
        menu.addAction(QAction(get_icon(DEL_STRUCT_ACTION),
                               DEL_STRUCT_ACTION.format(self.struct_name), menu))

    def handle_menu_func(self, func):
        # 打开结构体
        if func == OPEN_STRUCT_ACTION.format(self.struct_name):
            pass
        # 取消打开结构体
        elif func == CANCEL_OPEN_STRUCT_ACTION.format(self.struct_name):
            pass
        # 关闭结构体
        elif func == CLOSE_STRUCT_ACTION.format(self.struct_name):
            pass
        # 编辑结构体
        elif func == EDIT_STRUCT_ACTION.format(self.struct_name):
            edit_struct_func(self.opened_item.data_type.display_name, self.tree_widget,
                             self.window.geometry(), self.opened_item.id)
        # 删除结构体
        elif func == DEL_STRUCT_ACTION.format(self.struct_name):
            pass

    def worker_terminate(self):
        super().worker_terminate()
