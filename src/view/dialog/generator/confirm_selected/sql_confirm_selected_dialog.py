# -*- coding: utf-8 -*-
from src.constant.icon_enum import get_icon
from src.view.dialog.generator.generator_dialog import DisplaySelectedDialogABC
from src.view.tree.tree_widget.tree_function import make_display_tree_item

_author_ = 'luwt'
_date_ = '2022/11/1 9:12'


class SqlConfirmSelectedDialog(DisplaySelectedDialogABC):

    def __init__(self, selected_data, *args):
        self.selected_data = selected_data
        self.icon_names = ('db_icon_name', 'tb_icon_name', 'col_icon_name')
        super().__init__(*args)

    def setup_tree_ui(self):
        # 读取已选中数据，填充树结构
        for node in self.selected_data.root_children().values():
            # 获取连接类型
            conn_type = node.data.data_type
            icon = get_icon(conn_type.display_name)
            item = make_display_tree_item(self.display_tree_widget, node.node_name, icon)
            # 处理子元素
            self._iterate_make_node(node, item, conn_type)

    def _iterate_make_node(self, parent_node, parent_item, conn_type):
        if parent_node.children:
            first_node = tuple(parent_node.children.values())[0]
            icon = get_icon(eval(f'conn_type.{self.icon_names[first_node.item_level - 1]}'))
            for node in parent_node.children.values():
                item = make_display_tree_item(parent_item, node.node_name, icon)
                self._iterate_make_node(node, item, conn_type)

