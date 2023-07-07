# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt, QVariant

from src.view.tree.tree_item.tree_item_func import get_add_del_data, save_tree_data
from src.view.tree.tree_item.tree_node_abc import TreeNodeABC

_author_ = 'luwt'
_date_ = '2022/12/2 11:32'


class StructTreeNodeABC(TreeNodeABC):

    def __init__(self, *args):
        super().__init__(*args)

    def set_check_state(self, *args):
        ...

    def save_check_state(self):
        # 保存选中数据
        save_tree_data(self.item, self.tree_widget.tree_data)
        self.tree_widget.item_changed_executor.item_checked(self.item)

    def hide_check_box(self):
        # 隐藏复选框
        self.item.setData(0, Qt.ItemDataRole.CheckStateRole, QVariant())
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
