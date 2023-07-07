# -*- coding: utf-8 -*-
from src.constant.ds_type_constant import STRUCT_COL_ICON
from src.enum.icon_enum import get_icon
from src.service.system_storage.opened_tree_item_sqlite import OpenedTreeItem
from src.view.frame.generator.selected_data.selected_data_dialog_frame_abc import SelectedDataDialogFrameABC
from src.view.tree.tree_widget.tree_function import make_display_tree_item

_author_ = 'luwt'
_date_ = '2023/4/4 11:39'


class StructSelectedDataDialogFrame(SelectedDataDialogFrameABC):
    """展示选中结构体数据对话框框架"""

    def __init__(self, selected_data, *args):
        self.selected_data = selected_data
        super().__init__(*args)

    def setup_tree_ui(self):
        # 读取已选中数据，填充树结构
        for node in self.selected_data.root_children().values():
            # 处理子元素
            self._iterate_make_node(node, self.display_tree_widget)

    def _iterate_make_node(self, node, parent_item):
        # 根据类型，判定是树节点还是列数据
        if isinstance(node.data, OpenedTreeItem):
            struct_type = node.data.data_type
            icon = get_icon(struct_type.display_name)
        else:
            icon = get_icon(STRUCT_COL_ICON)
        item = make_display_tree_item(parent_item, node.node_name, icon)

        if node.children:
            for child_node in node.children.values():
                self._iterate_make_node(child_node, item)
