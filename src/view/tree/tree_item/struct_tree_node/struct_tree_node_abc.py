# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QVariant

from src.view.tree.tree_item.tree_node_abc import TreeNodeABC
from src.view.tree.tree_item.tree_item_func import get_item_opened_record, get_add_del_data, save_tree_data

_author_ = 'luwt'
_date_ = '2022/12/2 11:32'


class StructTreeNodeABC(TreeNodeABC):

    def __init__(self, *args):
        super().__init__(*args)

    def set_check_state(self, *args): ...

    def save_check_state(self):
        # 保存选中数据
        save_tree_data(self.item, self.tree_widget.tree_data)
        self.tree_widget.item_changed_executor.item_checked(self.item)

    def hide_check_box(self):
        # 隐藏复选框
        self.item.setData(0, Qt.CheckStateRole, QVariant())
        parent_item = self.item.parent()
        if parent_item:
            parent_node = self.tree_widget.get_item_node(parent_item)
            parent_node.hide_check_box()

    def link_parent_node(self, parent_item=None):
        # 联动父节点变化
        parent_item = parent_item if parent_item else self.item.parent()
        if parent_item:
            parent_node = self.tree_widget.get_item_node(parent_item)
            # 如果父节点正在刷新，或包含正在刷新的节点，不触发复选框的变化
            if parent_node.is_refreshing or parent_node.refreshing_child_count \
                    or parent_node.is_opening or parent_node.opening_child_count:
                return
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

    def del_callback(self):
        parent_item = self.item.parent()
        # 同步删除选中数据
        if self.item.checkState(0):
            del_data = get_add_del_data(self.item)
            self.tree_widget.tree_data.del_node(del_data)
        if parent_item:
            self.item.parent().removeChild(self.item)
            # 联动父节点选中状态
            self.tree_widget.link_parent_node(self.item, parent_item)
            # 最后处理下父节点的展开状态
            if not parent_item.childCount():
                parent_item.setExpanded(False)
        else:
            self.tree_widget.takeTopLevelItem(self.tree_widget.indexOfTopLevelItem(self.item))
