# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QAction

from src.constant.icon_enum import get_icon
from src.constant.list_constant import EDIT_COL_TYPE_ACTION, EDIT_COL_TYPE_ICON, DEL_COL_TYPE_ACTION, DEL_COL_TYPE_ICON, \
    DEL_COL_TYPE_PROMPT, EDIT_DS_COL_TYPE_TITLE, DEL_ALL_COL_TYPE_ACTION, DEL_ALL_COL_TYPE_ICON, \
    DEL_ALL_COL_TYPE_PROMPT, \
    DEL_COL_TYPE_BOX_TITLE, DEL_ALL_COL_TYPE_BOX_TITLE
from src.view.box.message_box import pop_question
from src.view.list_widget.abstract_list_widget import AbstractListWidget

_author_ = 'luwt'
_date_ = '2023/2/13 15:15'


class ColTypeListWidget(AbstractListWidget):

    def __init__(self, col_types, edit_col_type_func, *args):
        self.col_types: list = col_types
        self.edit_col_type_func = edit_col_type_func
        super().__init__(*args)

    def fill_menu(self, item, menu):
        # 编辑列类型
        menu.addAction(QAction(get_icon(EDIT_COL_TYPE_ICON), EDIT_COL_TYPE_ACTION.format(item.text()), menu))
        menu.addSeparator()
        # 删除列类型
        menu.addAction(QAction(get_icon(DEL_COL_TYPE_ICON), DEL_COL_TYPE_ACTION.format(item.text()), menu))
        # 删除所有列类型
        menu.addAction(QAction(get_icon(DEL_ALL_COL_TYPE_ICON), DEL_ALL_COL_TYPE_ACTION, menu))

    def do_right_menu_func(self, item, action_text):
        if action_text == EDIT_COL_TYPE_ACTION.format(item.text()):
            self.edit_col_type_func(EDIT_DS_COL_TYPE_TITLE, item.text())
        elif action_text == DEL_COL_TYPE_ACTION.format(item.text()):
            if pop_question(DEL_COL_TYPE_PROMPT.format(item.text()),
                            DEL_COL_TYPE_BOX_TITLE.format(item.text()), self.parent()):
                self.col_types.remove(item.text())
                self.takeItem(self.row(self.currentItem()))
        elif action_text == DEL_ALL_COL_TYPE_ACTION:
            if pop_question(DEL_ALL_COL_TYPE_PROMPT, DEL_ALL_COL_TYPE_BOX_TITLE, self.parent()):
                self.col_types.clear()
                self.clear()
