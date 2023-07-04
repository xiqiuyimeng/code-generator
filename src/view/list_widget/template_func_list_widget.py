# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem

from src.constant.list_constant import TEMPLATE_FUNC_NAME, EDIT_TEMPLATE_FUNC_BOX_TITLE
from src.service.system_storage.template_func_sqlite import CurrentEnum
from src.view.list_widget.custom_list_widget import CustomListWidget
from src.view.list_widget.list_item_func import get_template_func_data, set_template_func_data

_author_ = 'luwt'
_date_ = '2023/3/27 17:44'


class TemplateFuncListWidget(CustomListWidget):

    def __init__(self, edit_function_func, *args):
        self.edit_function_func = edit_function_func
        super().__init__(TEMPLATE_FUNC_NAME, *args)

    def connect_signal(self):
        super().connect_signal()
        # 模板方法支持双击进入编辑模式
        self.doubleClicked.connect(lambda index: self.edit_item_func(self.itemFromIndex(index)))

    def fill_list_widget(self, func_list):
        for func in func_list:
            set_template_func_data(self.add_item(func.func_name, func.checked), func)

    def add_item(self, func_name, check_state=Qt.Unchecked):
        func_item = QListWidgetItem(func_name)
        func_item.setCheckState(check_state)
        self.addItem(func_item)
        return func_item

    def edit_item_func(self, item):
        template_func = get_template_func_data(item)
        self.edit_function_func(EDIT_TEMPLATE_FUNC_BOX_TITLE, template_func)

    def collect_template_func_list(self):
        template_func_list = list()
        for row in range(self.count()):
            item = self.item(row)
            template_func = get_template_func_data(item)
            template_func.checked = item.checkState()
            template_func.is_current = CurrentEnum.current_func.value \
                if item is self.currentItem() else CurrentEnum.not_current_func.value
            template_func_list.append(template_func)
        return template_func_list

    def remove_selected_item(self):
        for row in reversed(range(self.count())):
            if self.item(row).checkState():
                self.takeItem(row)

    def select_all_item(self):
        for row in range(self.count()):
            if self.item(row).checkState() == Qt.Unchecked:
                self.item(row).setCheckState(Qt.Checked)

    def unselect_all_item(self):
        for row in range(self.count()):
            if self.item(row).checkState() == Qt.Checked:
                self.item(row).setCheckState(Qt.Unchecked)

    def copy_func_list(self, func_list):
        # 逐一添加元素，如果已经存在，删除原有项
        exists_func_names = self.collect_item_text()
        for func in func_list:
            set_template_func_data(self.add_item(func.func_name), func)
        # 筛选重复项，删除重复项
        duplicate_rows = reversed([exists_func_names.index(func.func_name)
                                   for func in func_list if func.func_name in exists_func_names])
        for row in duplicate_rows:
            self.takeItem(row)
