# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAction

from src.constant.icon_enum import get_icon
from src.constant.table_constant import ROW_EXPORT_ICON, ROW_EXPORT_TEXT
from src.view.table.table_widget.custom_table_widget import CustomTableWidget

_author_ = 'luwt'
_date_ = '2023/5/9 12:31'


class CustomExportTableWidget(CustomTableWidget):
    # 行导出信号，发送id
    row_export_signal = pyqtSignal(int)

    def pop_menu(self, tool_button, order_item, row_id):
        super().pop_menu(tool_button, order_item, row_id)
        export_act = QAction(get_icon(ROW_EXPORT_ICON), ROW_EXPORT_TEXT, self)
        export_act.triggered.connect(lambda: self.row_export_signal.emit(row_id))
        # 插入导出菜单，倒数第二个的位置
        tool_button.menu().insertAction(tool_button.menu().actions()[-1], export_act)
