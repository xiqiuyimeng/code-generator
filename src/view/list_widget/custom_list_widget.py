# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QAction

from src.constant.icon_enum import get_icon
from src.constant.list_constant import EDIT_ITEM_ACTION, EDIT_LIST_ITEM_ICON, DEL_ITEM_ACTION, DEL_LIST_ITEM_ICON, \
    DEL_ITEM_PROMPT, DEL_ALL_ITEMS_ACTION, DEL_ALL_LIST_ITEMS_ICON, DEL_ALL_ITEMS_PROMPT, DEL_ITEM_BOX_TITLE, \
    DEL_ALL_ITEMS_BOX_TITLE
from src.view.box.message_box import pop_question
from src.view.list_widget.list_widget_abc import ListWidgetABC

_author_ = 'luwt'
_date_ = '2023/3/24 15:15'


class CustomListWidget(ListWidgetABC):

    def __init__(self, item_type_name, *args):
        self.item_type_name = item_type_name
        super().__init__(*args)

    def fill_menu(self, item, menu):
        # 编辑
        menu.addAction(QAction(get_icon(EDIT_LIST_ITEM_ICON),
                               EDIT_ITEM_ACTION.format(self.item_type_name, item.text()),
                               menu))
        menu.addSeparator()
        # 删除
        menu.addAction(QAction(get_icon(DEL_LIST_ITEM_ICON),
                               DEL_ITEM_ACTION.format(self.item_type_name, item.text()),
                               menu))
        # 删除所有
        menu.addAction(QAction(get_icon(DEL_ALL_LIST_ITEMS_ICON),
                               DEL_ALL_ITEMS_ACTION.format(self.item_type_name),
                               menu))

    def do_right_menu_func(self, item, action_text):
        if action_text == EDIT_ITEM_ACTION.format(self.item_type_name, item.text()):
            self.edit_item_func(item)
        elif action_text == DEL_ITEM_ACTION.format(self.item_type_name, item.text()):
            if pop_question(DEL_ITEM_PROMPT.format(self.item_type_name, item.text()),
                            DEL_ITEM_BOX_TITLE.format(self.item_type_name, item.text()),
                            self.parent()):
                self.remove_item_func(item)
        elif action_text == DEL_ALL_ITEMS_ACTION.format(self.item_type_name):
            if pop_question(DEL_ALL_ITEMS_PROMPT.format(self.item_type_name),
                            DEL_ALL_ITEMS_BOX_TITLE.format(self.item_type_name),
                            self.parent()):
                self.clear_items_func()

    def edit_item_func(self, item):
        ...

    def remove_item_func(self, item):
        self.takeItem(self.row(item))

    def clear_items_func(self):
        self.clear()

    def collect_item_text(self):
        return [self.item(row).text() for row in range(self.count())]
