# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from src.view.frame.datasource.table_frame import get_table_frame

_author_ = 'luwt'
_date_ = '2022/10/10 12:12'


class TabTableUI(QWidget):

    def __init__(self, main_window, table_tab, item, tree_widget):
        super().__init__()
        self.main_window = main_window
        self.table_tab = table_tab
        self.column_list = table_tab.col_list
        self.tree_item = item
        self.tree_widget = tree_widget
        self.table_frame = ...
        self._layout = QVBoxLayout(self)
        self.setup_ui()

    def setup_ui(self):
        self.table_frame = get_table_frame(self.main_window.current_ds_category.name, self,
                                           self.column_list, self.tree_item, self.tree_widget)
        self._layout.addWidget(self.table_frame)

    def refresh_ui(self, table_tab):
        self.column_list = table_tab.col_list
        self.table_frame.refresh_ui(self.column_list)
