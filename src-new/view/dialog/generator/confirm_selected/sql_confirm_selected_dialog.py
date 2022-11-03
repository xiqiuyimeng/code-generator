# -*- coding: utf-8 -*-
from constant.constant import SQL_CONFIRM_SELECTED_HEADER_TXT
from constant.icon_enum import get_icon
from service.system_storage.conn_type import get_conn_type_by_type
from view.dialog.generator.abstract_generator_dialog import AbstractDisplaySelectedDialog
from view.tree.tree_widget.tree_function import make_sql_tree_item

_author_ = 'luwt'
_date_ = '2022/11/1 9:12'


class SqlConfirmSelectedDialog(AbstractDisplaySelectedDialog):

    def __init__(self, selected_data, *args):
        self.selected_data = selected_data
        super().__init__(*args)

    def get_header_text(self) -> str:
        return SQL_CONFIRM_SELECTED_HEADER_TXT

    def setup_tree_ui(self):
        # 读取已选中数据，填充树结构
        for node in self.selected_data.root_children().values():
            # 获取连接类型
            conn_type = get_conn_type_by_type(node.top_level_data.conn_type)
            item = make_sql_tree_item(self.display_tree_widget, node.name_text, get_icon(conn_type.display_name))
            # 处理子元素
            self._iterate_make_node(node, item, conn_type)

    def _iterate_make_node(self, parent_node, parent_item, conn_type):
        if parent_node.children:
            for node in parent_node.children.values():
                item = make_sql_tree_item(parent_item, node.name_text,
                                          get_icon(eval(f'conn_type.{parent_node.child_type}_icon_name')))
                self._iterate_make_node(node, item, conn_type)

