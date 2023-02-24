# -*- coding: utf-8 -*-
from src.constant.ds_type_constant import STRUCT_COL_ICON
from src.constant.generator_dialog_constant import STRUCTURE_CONFIRM_SELECTED_HEADER_TXT
from src.constant.icon_enum import get_icon
from src.service.system_storage.opened_tree_item_sqlite import OpenedTreeItem
from src.view.dialog.generator.abstract_generator_dialog import AbstractDisplaySelectedDialog
from src.view.tree.tree_widget.tree_function import make_display_tree_item

_author_ = 'luwt'
_date_ = '2022/11/1 10:30'


class StructureConfirmSelectedDialog(AbstractDisplaySelectedDialog):

    def __init__(self, selected_data, *args):
        self.selected_data = selected_data
        super().__init__(*args)

    def get_header_text(self) -> str:
        return STRUCTURE_CONFIRM_SELECTED_HEADER_TXT

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
