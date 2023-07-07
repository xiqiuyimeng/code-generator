# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QListWidgetItem

from src.view.list_widget.list_item_func import set_import_error_data, get_import_error_data
from src.view.list_widget.list_widget_abc import ListWidgetABC

_author_ = 'luwt'
_date_ = '2023/5/12 16:52'


class ImportErrorDataListWidget(ListWidgetABC):

    def fill_list_widget(self, duplicate_data_list):
        for data in duplicate_data_list:
            item = QListWidgetItem(data.get_name())
            item.setCheckState(Qt.CheckState.Unchecked)
            set_import_error_data(item, data)
            self.addItem(item)

    def select_all_items(self):
        for row in range(self.count()):
            self.item(row).setCheckState(Qt.CheckState.Checked)

    def unselect_all_items(self):
        for row in range(self.count()):
            self.item(row).setCheckState(Qt.CheckState.Unchecked)

    def get_selected_data_list(self):
        return [get_import_error_data(self.item(row))
                for row in range(self.count()) if self.item(row).checkState() == Qt.CheckState.Checked]

    def remove_selected_items(self):
        for row in reversed(range(self.count())):
            if self.item(row).checkState() == Qt.CheckState.Checked:
                self.takeItem(row)

    def remove_item_by_name(self, data):
        for row in range(self.count()):
            if self.item(row).text() == data.get_name():
                self.takeItem(row)
                break
