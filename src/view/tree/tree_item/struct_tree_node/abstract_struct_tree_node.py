# -*- coding: utf-8 -*-

from view.tree.tree_item.abstract_tree_node import AbstractTreeNode
from view.tree.tree_item.tree_item_func import get_item_opened_record

_author_ = 'luwt'
_date_ = '2022/12/2 11:32'


class AbstractStructTreeNode(AbstractTreeNode):

    def set_check_state(self, *args): ...

    def link_parent_node(self, parent_item=None):
        # 联动父节点变化
        parent_item = parent_item if parent_item else self.item.parent()
        if parent_item:
            parent_node = parent_item.tree_node
            parent_node.set_check_state()

    def get_need_reorder_items(self):
        """当前节点之后的节点需要调整顺序"""
        reorder_opened_items = list()
        reorder_flag = False
        if self.item.parent():
            for idx in range(self.item.parent().childCount()):
                item = self.item.parent().child(idx)
                if item is self.item:
                    reorder_flag = True
                if reorder_flag:
                    opened_item = get_item_opened_record(item)
                    opened_item.item_order -= 1
                    reorder_opened_items.append(opened_item)
        else:
            # 获取顶层节点
            top_items = self.tree_widget.get_top_level_items()
            for item in top_items:
                if item is self.item:
                    reorder_flag = True
                if reorder_flag:
                    opened_item = get_item_opened_record(item)
                    opened_item.item_order -= 1
                    reorder_opened_items.append(opened_item)
        return reorder_opened_items