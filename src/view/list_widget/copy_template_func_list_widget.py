# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem

from src.view.list_widget.list_item_func import set_template_func_data, get_template_func_data
from src.view.list_widget.list_widget_abc import ListWidgetABC

_author_ = 'luwt'
_date_ = '2023/6/26 11:29'


class CopyTemplateFuncListWidget(ListWidgetABC):

    def fill_list_widget(self, func_list):
        for func in func_list:
            item = QListWidgetItem(func.func_name)
            item.setCheckState(Qt.Unchecked)
            set_template_func_data(item, func)
            self.addItem(item)

    def select_all_item(self):
        for row in range(self.count()):
            if self.item(row).checkState() == Qt.Unchecked:
                self.item(row).setCheckState(Qt.Checked)

    def unselect_all_item(self):
        for row in range(self.count()):
            if self.item(row).checkState() == Qt.Checked:
                self.item(row).setCheckState(Qt.Unchecked)

    def collect_selected_data(self):
        template_func_list = list()
        for row in range(self.count()):
            item = self.item(row)
            if item.checkState() == Qt.Checked:
                template_func = get_template_func_data(item)
                template_func_list.append(template_func)
                item.setCheckState(Qt.Unchecked)
        return template_func_list
