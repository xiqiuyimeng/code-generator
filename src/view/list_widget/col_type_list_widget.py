# -*- coding: utf-8 -*-

from src.constant.list_constant import EDIT_DS_COL_TYPE_TITLE, COL_TYPE_NAME
from src.view.list_widget.custom_list_widget import CustomListWidget

_author_ = 'luwt'
_date_ = '2023/2/13 15:15'


class ColTypeListWidget(CustomListWidget):

    def __init__(self, col_types, edit_col_type_func, *args):
        self.col_types: list = col_types
        self.edit_col_type_func = edit_col_type_func
        super().__init__(COL_TYPE_NAME, *args)

    def edit_item_func(self, item):
        self.edit_col_type_func(EDIT_DS_COL_TYPE_TITLE, item.text())

    def remove_item_func(self, item):
        self.col_types.remove(item.text())
        super().remove_item_func(item)

    def clear_items_func(self):
        self.col_types.clear()
        super().clear_items_func()
