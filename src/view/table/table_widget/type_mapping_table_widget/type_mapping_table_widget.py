# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QAbstractItemView, QToolButton, QMenu, QAction, QHeaderView

from src.constant.icon_enum import get_icon
from src.constant.table_constant import TYPE_MAPPING_TABLE_HEADER_LABELS, TYPE_MAPPING_OPERATION_ICON, \
    TYPE_MAPPING_OPERATION_TEXT, TYPE_MAPPING_CAT_EDIT_TEXT, TYPE_MAPPING_CAT_EDIT_ICON, TYPE_MAPPING_REMOVE_TEXT, \
    TYPE_MAPPING_REMOVE_ICON
from src.view.table.table_header.check_box_table_header import CheckBoxHeader
from src.view.table.table_item.table_item import make_checkbox_num_widget
from src.view.table.table_widget.abstract_table_widget import AbstractTableWidget

_author_ = 'luwt'
_date_ = '2023/2/13 11:09'


class TypeMappingTableWidget(AbstractTableWidget):
    # 编辑行信号，发送类型映射id和行序号
    row_edit_signal = pyqtSignal(int, int)
    # 删除行信号，发送类型映射id、行序号和类型映射名称
    row_del_signal = pyqtSignal(int, int, str)

    def __init__(self, *args):
        # 表头控件
        self.header_widget: CheckBoxHeader = ...
        super().__init__(*args)
        self.cols = list()

    def setup_other_ui(self):
        # 设置表格列数
        self.setColumnCount(7)
        # 构建表头
        self.header_widget = CheckBoxHeader(TYPE_MAPPING_TABLE_HEADER_LABELS, self)
        # 表头高度写死
        self.horizontalHeader().setFixedHeight(self.header_widget.rowHeight(0))
        # 设置窗口层次，表头在表格上方
        self.viewport().stackUnder(self.header_widget)

        # 设置表头列宽度
        self.header_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 不可编辑
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def resizeEvent(self, e) -> None:
        self.header_widget.setGeometry(self.frameWidth(), self.frameWidth(),
                                       self.viewport().width(), self.horizontalHeader().height())
        super().resizeEvent(e)

    def fill_table(self, cols):
        self.cols = cols
        for i, col in enumerate(cols):
            self._do_add_row(col, i)

    def _do_add_row(self, type_mapping, row_index):
        self.insert_row(row_index)
        checkbox_num_widget = make_checkbox_num_widget(row_index + 1,
                                                       self.header_widget.calculate_header_check_state)
        order_item = checkbox_num_widget.check_label
        setattr(order_item, 'row_id', type_mapping.id)
        self.setCellWidget(row_index, 0, checkbox_num_widget)
        self.setItem(row_index, 1, self.make_item(type_mapping.mapping_name))
        self.setItem(row_index, 2, self.make_item(type_mapping.ds_type))
        self.setItem(row_index, 3, self.make_item(type_mapping.comment))
        self.setItem(row_index, 4, self.make_item(type_mapping.create_time))
        self.setItem(row_index, 5, self.make_item(type_mapping.update_time))
        # 添加操作按钮
        self.setCellWidget(row_index, 6, self.make_operation_buttons(order_item, type_mapping.id,
                                                                     type_mapping.mapping_name))

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
        self.resort_row(row)

    def resort_row(self, row=0):
        for row_index in range(row, self.rowCount()):
            self.cellWidget(row_index, 0).check_label.setText(str(row_index + 1))

    def edit_row(self, type_mapping, row_index):
        # 重新渲染数据
        self.setItem(row_index, 1, self.make_item(type_mapping.mapping_name))
        self.setItem(row_index, 2, self.make_item(type_mapping.ds_type))
        self.setItem(row_index, 3, self.make_item(type_mapping.comment))
        self.setItem(row_index, 5, self.make_item(type_mapping.update_time))

    def get_all_checked_id_names(self):
        checked_ids, checked_names = list(), list()
        for row_idx in range(self.rowCount()):
            check_num_widget = self.cellWidget(row_idx, 0)
            # 如果选中，进行收集
            if check_num_widget.check_box.checkState():
                checked_ids.append(int(check_num_widget.check_label.row_id))
                checked_names.append(self.item(row_idx, 1).text())
        return checked_ids, checked_names

    def del_rows(self):
        # 根据选中状态删除
        for row_index in reversed(range(self.rowCount())):
            if self.cellWidget(row_index, 0).check_box.checkState():
                self.removeRow(row_index)
        self.resort_row()
        self.header_widget.calculate_header_check_state()
