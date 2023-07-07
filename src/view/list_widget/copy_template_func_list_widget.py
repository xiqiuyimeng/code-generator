# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QListWidgetItem

from src.view.list_widget.list_item_func import set_template_func_data, get_template_func_data
from src.view.list_widget.list_widget_abc import ListWidgetABC

_author_ = 'luwt'
_date_ = '2023/6/26 11:29'


class CopyTemplateFuncListWidget(ListWidgetABC):

    def fill_list_widget(self, func_list):
        for func in func_list:
            item = QListWidgetItem(func.func_name)
            item.setCheckState(Qt.CheckState.Unchecked)
            set_template_func_data(item, func)
            self.addItem(item)

    def select_all_item(self):
        for row in range(self.count()):
            if self.item(row).checkState() == Qt.CheckState.Unchecked:
                self.item(row).setCheckState(Qt.CheckState.Checked)

    def unselect_all_item(self):
        for row in range(self.count()):
            if self.item(row).checkState() == Qt.CheckState.Checked:
                self.item(row).setCheckState(Qt.CheckState.Unchecked)

    def collect_selected_data(self):
        template_func_list = list()
        for row in range(self.count()):
            item = self.item(row)
            if item.checkState() == Qt.CheckState.Checked:
                template_func = get_template_func_data(item)
                template_func_list.append(template_func)
                item.setCheckState(Qt.CheckState.Unchecked)
        return template_func_list
