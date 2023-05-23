# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QListWidgetItem, QAction

from src.constant.icon_enum import get_icon
from src.constant.list_constant import TEMPLATE_FUNC_NAME, EDIT_TEMPLATE_FUNC_BOX_TITLE, EXPORT_ITEM_ICON, \
    EXPORT_ITEM_ACTION
from src.constant.template_dialog_constant import DEL_TEMPLATE_FUNC_BOX_TITLE, CLEAR_TEMPLATE_FUNC_BOX_TITLE
from src.service.async_func.async_template_func_task import DelTemplateFuncExecutor, ClearTemplateFuncExecutor
from src.view.list_widget.custom_list_widget import CustomListWidget
from src.view.list_widget.list_item_func import get_template_func_data, set_template_func_data

_author_ = 'luwt'
_date_ = '2023/3/27 17:44'


class TemplateFuncListWidget(CustomListWidget):

    def __init__(self, edit_function_func, export_template_func, *args):
        self.edit_function_func = edit_function_func
        self.export_template_func = export_template_func
        self.del_template_func_executor: DelTemplateFuncExecutor = ...
        self.clear_template_func_executor: ClearTemplateFuncExecutor = ...
        super().__init__(TEMPLATE_FUNC_NAME, *args)

    def connect_signal(self):
        super().connect_signal()
        # 模板方法支持双击进入编辑模式
        self.doubleClicked.connect(lambda index: self.edit_item_func(self.itemFromIndex(index)))

    def fill_list_widget(self, func_list):
        for func in func_list:
            func_item = QListWidgetItem(func.func_name)
            self.addItem(func_item)
            set_template_func_data(func_item, func)

    def fill_menu(self, item, menu):
        super().fill_menu(item, menu)
        menu.addSeparator()
        # 导出方法
        menu.addAction(QAction(get_icon(EXPORT_ITEM_ICON),
                               EXPORT_ITEM_ACTION.format(self.item_type_name, item.text()),
                               menu))

    def do_right_menu_func(self, item, action_text):
        super().do_right_menu_func(item, action_text)
        if action_text == EXPORT_ITEM_ACTION.format(self.item_type_name, item.text()):
            self.export_template_func(get_template_func_data(item).id)

    def edit_item_func(self, item):
        template_func = get_template_func_data(item)
        self.edit_function_func(EDIT_TEMPLATE_FUNC_BOX_TITLE, template_func)

    def remove_item_func(self, item):
        template_func = get_template_func_data(item)
        self.del_template_func_executor = DelTemplateFuncExecutor(template_func.id, template_func.func_name,
                                                                  self.parent_widget, self.parent_widget,
                                                                  DEL_TEMPLATE_FUNC_BOX_TITLE, self.do_remove_item)
        self.del_template_func_executor.start()

    def do_remove_item(self):
        super().remove_item_func(self.currentItem())

    def clear_items_func(self):
        self.clear_template_func_executor = ClearTemplateFuncExecutor(self.parent_widget, self.parent_widget,
                                                                      CLEAR_TEMPLATE_FUNC_BOX_TITLE,
                                                                      super().clear_items_func)
        self.clear_template_func_executor.start()

    def collect_func_ids(self):
        return tuple(get_template_func_data(self.item(row)).id for row in range(self.count()))

    def del_duplicate_rows(self, duplicate_data_list):
        # 根据名称删除
        duplicate_names = tuple(data.func_name for data in duplicate_data_list)
        [self.takeItem(row) for row in reversed(range(self.count())) if self.item(row).text() in duplicate_names]
