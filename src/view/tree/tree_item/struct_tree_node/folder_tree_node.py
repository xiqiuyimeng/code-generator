# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu, QAction

from constant.constant import ADD_DS_ACTION, ADD_STRUCT_ACTION, CREATE_NEW_FOLDER_ACTION, RENAME_FOLDER_ACTION, \
    DEL_FOLDER_ACTION, SELECT_ALL_ACTION, UNSELECT_ACTION, DEL_FOLDER_PROMPT, FOLDER_TYPE, REFRESH_ACTION
from constant.icon_enum import get_icon
from service.async_func.async_struct_task import DelFolderExecutor
from view.bar.bar_action import add_structure_ds_actions
from view.box.message_box import pop_question
from view.tree.tree_item.struct_tree_node.abstract_struct_tree_node import AbstractStructTreeNode
from view.tree.tree_item.tree_item_func import get_item_opened_record, get_item_opened_tab
from view.tree.tree_widget.tree_function import add_folder_func, edit_folder_func, add_struct_tree_item

_author_ = 'luwt'
_date_ = '2022/12/2 12:08'


class FolderTreeNode(AbstractStructTreeNode):

    def __init__(self, *args):
        super().__init__(*args)
        self.item_name = self.item.text(0)
        self.del_folder_executor: DelFolderExecutor = ...

    def reopen_item(self, opened_items):
        for opened_item in opened_items:
            add_struct_tree_item(self.tree_widget, self.item, opened_item, opened_item.data_type.display_name)

    def change_check_box(self, check_state, clicked):
        # 保存数据
        self.save_check_state()
        # 如果是点击，联动父节点变化
        if clicked:
            self.link_parent_node()

    def do_fill_menu(self, menu):
        # 添加结构体需要有二级菜单
        add_struct_menu = QMenu(ADD_STRUCT_ACTION, menu)
        add_struct_menu.setIcon(get_icon(ADD_DS_ACTION))
        # 二级菜单
        add_structure_ds_actions(add_struct_menu, self.window, self.opened_item, self.item)
        menu.addMenu(add_struct_menu)
        menu.addSeparator()

        # 新建文件夹
        menu.addAction(QAction(get_icon(CREATE_NEW_FOLDER_ACTION), CREATE_NEW_FOLDER_ACTION, menu))

        # 如果当前节点复选框状态为全选，菜单应该增加取消全选
        if self.item.checkState(0) == Qt.Checked:
            menu.addAction(QAction(UNSELECT_ACTION, menu))
        elif self.item.checkState(0) == Qt.PartiallyChecked:
            # 如果当前节点复选框状态为部分选择，菜单应该增加全选和取消全选
            menu.addAction(QAction(SELECT_ALL_ACTION, menu))
            menu.addAction(QAction(UNSELECT_ACTION, menu))
        else:
            # 如果当前节点复选框状态为未选择，菜单应该增加全选
            menu.addAction(QAction(SELECT_ALL_ACTION, menu))
        menu.addSeparator()

        # 重命名
        menu.addAction(QAction(get_icon(RENAME_FOLDER_ACTION),
                               RENAME_FOLDER_ACTION.format(self.item_name), menu))
        # 删除
        menu.addAction(QAction(get_icon(DEL_FOLDER_ACTION),
                               DEL_FOLDER_ACTION.format(self.item_name), menu))

        # 刷新
        menu.addSeparator()
        menu.addAction(QAction(get_icon(REFRESH_ACTION), f'{REFRESH_ACTION}[{self.item_name}]', menu))

    def handle_menu_func(self, func):
        # 新建文件夹
        if func == CREATE_NEW_FOLDER_ACTION:
            add_folder_func(self.window.geometry(), self.tree_widget)
        # 全选
        elif func == SELECT_ALL_ACTION:
            self.item.setCheckState(0, Qt.Checked)
            self.tree_widget.handle_checkbox_changed(self.item, clicked=False)
        # 取消全选
        elif func == UNSELECT_ACTION:
            self.item.setCheckState(0, Qt.Unchecked)
            self.tree_widget.handle_checkbox_changed(self.item, clicked=False)
        # 重命名
        elif func == RENAME_FOLDER_ACTION.format(self.item_name):
            parent_item = self.item.parent()
            parent_opened_item = self.tree_widget.top_item \
                if parent_item is None else parent_item.tree_node.opened_item
            # 打开重命名文件夹对话框
            edit_folder_func(self.window.geometry(), self.tree_widget, parent_opened_item,
                             self.opened_item, parent_item)
        # 删除
        elif func == DEL_FOLDER_ACTION.format(self.item_name):
            if pop_question(DEL_FOLDER_PROMPT, DEL_FOLDER_ACTION.format(self.item_name), self.window):
                self.del_folder()
        # 刷新
        elif func == REFRESH_ACTION.format(self.item_name):
            self.refresh()

    def set_check_state(self):
        # 对于文件夹节点而言，由下而上联动复选框，需要考虑当前节点状态，以及应该向上传递的状态
        check_state = self.calculate_check_state()
        self.item.setCheckState(0, check_state)
        self.change_check_box(check_state, False)
        self.link_parent_node()

    def calculate_check_state(self):
        # 如果不存在子元素，那么应该返回未选择
        if self.item.childCount() == 0:
            return Qt.Unchecked
        # 如果子元素全选，那么应该返回全选，如果子元素全未选，应该返回未选择，否则返回部分选择
        check_set = set(map(lambda x: self.item.child(x).checkState(0), range(self.item.childCount())))
        if len(check_set) == 1:
            return check_set.pop()
        else:
            return Qt.PartiallyChecked

    def del_folder(self):
        # 删除结构体后，应该对同级别的其他项进行重排序
        reorder_items = self.get_need_reorder_items()
        tab_indexes, tab_ids = list(), list()
        self.get_child_tab_indexes_and_ids(self.item, tab_indexes, tab_ids)
        # 获取所有子节点的 opened id 和 存在 tab
        self.del_folder_executor = DelFolderExecutor(self.item_name, reorder_items, tab_indexes, tab_ids,
                                                     self.del_folder_callback, self.item, self.window)
        self.del_folder_executor.start()

    def del_folder_callback(self, tab_indexes):
        # 将所有结构体节点中的线程停止，并关闭所有已经打开的tab页
        self.stop_child_worker(self.item, tab_indexes)
        if tab_indexes:
            tab_indexes.sort(reverse=True)
            [self.window.struct_tab_widget.tab_bar.remove_tab(index, False, False) for index in tab_indexes]
        self.del_callback()

    def stop_child_worker(self, parent_item, tab_indexes):
        """停止所有子结构体节点的线程"""
        child_count = parent_item.childCount()
        if not child_count:
            return
        for idx in range(child_count):
            child_item = parent_item.child(idx)
            opened_record = get_item_opened_record(child_item)
            # 如果子节点不是文件夹类型，停止子节点线程
            if opened_record.data_type.type != FOLDER_TYPE:
                child_item.tree_node.worker_terminate()
            else:
                # 对于文件夹节点，递归处理
                self.stop_child_worker(child_item, tab_indexes)

    def get_child_tab_indexes_and_ids(self, parent_item, tab_indexes, tab_ids):
        child_count = parent_item.childCount()
        if not child_count:
            return
        for idx in range(child_count):
            child_item = parent_item.child(idx)
            tab = get_item_opened_tab(child_item)
            if tab:
                tab_indexes.append(self.window.struct_tab_widget.indexOf(tab))
                tab_ids.append(tab.table_tab.id)
            self.get_child_tab_indexes_and_ids(child_item, tab_indexes, tab_ids)

    def refresh(self): ...
