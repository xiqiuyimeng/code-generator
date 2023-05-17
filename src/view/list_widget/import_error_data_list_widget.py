# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem

from src.view.list_widget.list_item_func import set_import_error_data, get_import_error_data
from src.view.list_widget.list_widget_abc import ListWidgetABC

_author_ = 'luwt'
_date_ = '2023/5/12 16:52'


class ImportErrorDataListWidget(ListWidgetABC):

    def fill_list_widget(self, duplicate_data_list):
        for data in duplicate_data_list:
            item = QListWidgetItem(data.get_name())
            item.setCheckState(Qt.Unchecked)
            set_import_error_data(item, data)
            self.addItem(item)

    def select_all_items(self):
        [self.item(row).setCheckState(Qt.CheckState.Checked) for row in range(self.count())]

    def unselect_all_items(self):
        [self.item(row).setCheckState(Qt.CheckState.Unchecked) for row in range(self.count())]

    def get_selected_data_list(self):
        return [get_import_error_data(self.item(row))
                for row in range(self.count()) if self.item(row).checkState()]

    def remove_selected_items(self):
        [self.takeItem(row) for row in reversed(range(self.count())) if self.item(row).checkState()]

    def remove_item_by_name(self, data):
        for row in range(self.count()):
            if self.item(row).text() == data.get_name():
                self.takeItem(row)
                break
