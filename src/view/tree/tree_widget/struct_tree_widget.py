# -*- coding: utf-8 -*-
from src.constant.tree_constant import LIST_ALL_STRUCT_BOX_TITLE
from src.service.async_func.async_struct_task import ListStructExecutor
from src.service.system_storage.opened_tree_item_sqlite import OpenedTreeItem
from src.service.util.tree_node import TreeData
from src.view.tab.tab_widget.tab_widget import TabWidget
from src.view.tree.tree_item.context import get_struct_tree_node
from src.view.tree.tree_item.struct_tree_node.abstract_struct_tree_node import AbstractStructTreeNode
from src.view.tree.tree_widget.abstract_tree_widget import AbstractTreeWidget
from src.view.tree.tree_widget.tree_function import add_struct_tree_item

_author_ = 'luwt'
_date_ = '2022/9/15 17:10'


class StructTreeWidget(AbstractTreeWidget):
    """结构体数据源树结构"""

    def __init__(self, parent, window):
        super().__init__(parent, window)
        self.list_struct_executor = ...
        # 保存 struct tree 选中数据
        self.tree_data = TreeData()
        self.top_item = OpenedTreeItem()
        self.top_item.level = -1
        self.top_item.id = 0

    def reopen_tree(self):
        # 如果还没初始化过，再执行初始化
        if self.list_struct_executor is Ellipsis:
            # 初始化数据
            self.list_struct_executor = ListStructExecutor(self.reopen_items, self.reopen_tab, self.main_window,
                                                           self.main_window, LIST_ALL_STRUCT_BOX_TITLE,
                                                           self.reopen_end, self.reopen_end)
            self.reopening_flag = True
            self.list_struct_executor.start()

    def reopen_items(self, opened_items):
        """
        重新打开树节点
        :param opened_items: 打开记录表中元素
        """
        level = opened_items[0].level
        # 如果是第一层节点，单独处理
        if level == self.top_item.level + 1:
            [add_struct_tree_item(self, self, opened_item, opened_item.data_type.display_name)
             for opened_item in opened_items]
        else:
            # 如果是其他类型，按策略来执行
            self.reopen_tree_item(opened_items)

    def get_current_tab_widget(self) -> TabWidget:
        return self.main_window.struct_tab_widget

    def link_parent_node(self, item, parent_item=None):
        self.get_item_node(item).link_parent_node(parent_item)

    def get_item_node(self, item) -> AbstractStructTreeNode:
        return get_struct_tree_node(item, self, self.main_window)
