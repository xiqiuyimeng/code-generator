# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMenu, QAction

from constant.constant import ADD_DS_ACTION, ADD_STRUCT_ACTION, CREATE_NEW_FOLDER_ACTION, RENAME_FOLDER_ACTION, \
    DEL_FOLDER_ACTION
from constant.icon_enum import get_icon
from view.bar.bar_action import add_structure_ds_actions
from view.tree.tree_item.struct_tree_node.abstract_struct_tree_node import AbstractStructTreeNode
from view.tree.tree_item.tree_item_func import get_item_opened_record
from view.tree.tree_widget.tree_function import add_folder_func, edit_folder_func, add_struct_tree_item

_author_ = 'luwt'
_date_ = '2022/12/2 12:08'


class FolderTreeNode(AbstractStructTreeNode):

    def reopen_item(self, opened_items):
        for opened_item in opened_items:
            add_struct_tree_item(self.tree_widget, self.item, opened_item, opened_item.data_type.display_name)

    def change_check_box(self, check_state):
        self.tree_widget.item_changed_executor.item_checked(self.item)

    def do_fill_menu(self, menu):
        # 添加结构体需要有二级菜单
        add_struct_menu = QMenu(ADD_STRUCT_ACTION, menu)
        add_struct_menu.setIcon(get_icon(ADD_DS_ACTION))
        # 二级菜单
        add_structure_ds_actions(add_struct_menu, self.window, get_item_opened_record(self.item), self.item)
        menu.addMenu(add_struct_menu)
        menu.addSeparator()

        # 新建文件夹
        menu.addAction(QAction(get_icon(CREATE_NEW_FOLDER_ACTION), CREATE_NEW_FOLDER_ACTION, menu))
        menu.addSeparator()

        # 重命名
        menu.addAction(QAction(get_icon(RENAME_FOLDER_ACTION),
                               RENAME_FOLDER_ACTION.format(self.item.text(0)), menu))
        # 删除
        menu.addAction(QAction(get_icon(DEL_FOLDER_ACTION),
                               DEL_FOLDER_ACTION.format(self.item.text(0)), menu))

    def handle_menu_func(self, func):
        # 新建文件夹
        if func == CREATE_NEW_FOLDER_ACTION:
            add_folder_func(self.window.geometry(), self.tree_widget)
        # 重命名
        elif func == RENAME_FOLDER_ACTION.format(self.item.text(0)):
            parent_item = self.item.parent()
            parent_opened_item = self.tree_widget.top_item \
                if parent_item is None else get_item_opened_record(parent_item)
            # 打开重命名文件夹对话框
            edit_folder_func(self.window.geometry(), self.tree_widget, parent_opened_item,
                             get_item_opened_record(self.item), parent_item)
        # 删除
        elif func == DEL_FOLDER_ACTION.format(self.item.text(0)):
            pass
