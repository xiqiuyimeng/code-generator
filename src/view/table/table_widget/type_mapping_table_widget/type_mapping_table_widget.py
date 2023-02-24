# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QToolButton, QMenu, QAction

from src.constant.icon_enum import get_icon
from src.constant.table_constant import TYPE_MAPPING_TABLE_HEADER_LABELS, TYPE_MAPPING_OPERATION_ICON, \
    TYPE_MAPPING_OPERATION_TEXT, TYPE_MAPPING_CAT_EDIT_TEXT, TYPE_MAPPING_CAT_EDIT_ICON, TYPE_MAPPING_REMOVE_TEXT, \
    TYPE_MAPPING_REMOVE_ICON
from src.view.table.table_widget.abstract_table_widget import AbstractTableWidget

_author_ = 'luwt'
_date_ = '2023/2/13 11:09'


class TypeMappingTableWidget(AbstractTableWidget):
    # 编辑行信号，发送类型映射id和行序号
    row_edit_signal = pyqtSignal(int, int)
    # 删除行信号，发送类型映射id、行序号和类型映射名称
    row_del_signal = pyqtSignal(int, int, str)

    def __init__(self, *args):
        super().__init__(*args)
        self.cols = list()

    def setup_other_ui(self):
        # 设置表格列数
        self.setColumnCount(len(TYPE_MAPPING_TABLE_HEADER_LABELS))
        # 设置表头字段
        self.setHorizontalHeaderLabels(TYPE_MAPPING_TABLE_HEADER_LABELS)
        # 设置表头列宽度
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 不可编辑
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def fill_table(self, cols):
        self.cols = cols
        for i, col in enumerate(cols):
            self._do_add_row(col, i)

    def _do_add_row(self, type_mapping, row_index):
        self.insertRow(row_index)
        order_item = self.make_item(row_index + 1)
        order_item.setCheckState(Qt.Unchecked)
        self.setItem(row_index, 0, order_item)
        self.setItem(row_index, 1, self.make_item(type_mapping.mapping_name))
        self.setItem(row_index, 2, self.make_item(type_mapping.ds_type))
        self.setItem(row_index, 3, self.make_item(type_mapping.comment))
        self.setItem(row_index, 4, self.make_item(type_mapping.create_time))
        self.setItem(row_index, 5, self.make_item(type_mapping.update_time))
        # 添加操作按钮
        self.setCellWidget(row_index, 6, self.make_operation_buttons(order_item, type_mapping.id,
                                                                     type_mapping.mapping_name))

        # 行高设为原行高的1.5倍，主要为了美观
        self.setRowHeight(row_index, round(self.rowHeight(row_index) * 1.5))

    def make_operation_buttons(self, order_item, type_mapping_id, mapping_name):
        """
        添加操作按钮
        """
        tool_button = QToolButton(self)
        tool_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        tool_button.setPopupMode(QToolButton.InstantPopup)
        tool_button.setText(TYPE_MAPPING_OPERATION_TEXT)
        tool_button.setIcon(get_icon(TYPE_MAPPING_OPERATION_ICON))
        tool_button.setAutoRaise(True)
        self.pop_menu(tool_button, order_item, type_mapping_id, mapping_name)
        return tool_button

    def pop_menu(self, tool_button, order_item, type_mapping_id, mapping_name):
        menu = QMenu(self)
        cat_edit_act = QAction(get_icon(TYPE_MAPPING_CAT_EDIT_ICON), TYPE_MAPPING_CAT_EDIT_TEXT, self)
        # 动态获取行序号
        cat_edit_act.triggered.connect(lambda: self.row_edit_signal.emit(type_mapping_id, int(order_item.text()) - 1))
        menu.addAction(cat_edit_act)
        del_act = QAction(get_icon(TYPE_MAPPING_REMOVE_ICON), TYPE_MAPPING_REMOVE_TEXT, self)
        del_act.triggered.connect(lambda: self.row_del_signal.emit(type_mapping_id,
                                                                   int(order_item.text()) - 1, mapping_name))
        menu.addAction(del_act)
        tool_button.setMenu(menu)

    def add_row(self, type_mapping):
        # 获取当前表格的最大行，添加新行
        self._do_add_row(type_mapping, self.rowCount())

    def del_row(self, row):
        self.removeRow(row)
        # 移除行后，需要重新构建序号
        for row_index in range(row, self.rowCount()):
            self.item(row_index, 0).setText(str(row_index + 1))

    def edit_row(self, type_mapping, row_index):
        # 重新渲染数据
        self.setItem(row_index, 1, self.make_item(type_mapping.mapping_name))
        self.setItem(row_index, 2, self.make_item(type_mapping.ds_type))
        self.setItem(row_index, 3, self.make_item(type_mapping.comment))
        self.setItem(row_index, 5, self.make_item(type_mapping.update_time))

