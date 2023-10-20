# -*- coding: utf-8 -*-
"""
表格结构，大体与树结构类似
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QToolButton, QLabel

from src.enum.icon_enum import get_icon
from src.constant.table_constant import EXPAND_CHILD_TABLE_ICON, COLLAPSE_CHILD_TABLE_ICON
from src.view.table.table_header.check_box_table_header import CheckBoxButtonHeader
from src.view.table.table_item.table_item import make_checkbox_num_button
from src.view.table.table_widget.ds_table_widget.ds_col_table_widget_abc import DsColTableWidgetABC
from src.view.tree.tree_item.tree_item_func import get_add_del_data

_author_ = 'luwt'
_date_ = '2022/5/10 15:25'


class StructDsColTableWidget(DsColTableWidgetABC):

    def __init__(self, *args, parent_table=None):
        self.parent_table: DsColTableWidgetABC = parent_table
        super().__init__(*args)

    def get_header(self, header_labels):
        return CheckBoxButtonHeader(header_labels, self)

    def batch_deal_checked(self, check_state):
        super().batch_deal_checked(check_state)
        # 检查每一行是否有子表，如果存在子表，联动子表复选框
        for row in range(len(self.cols)):
            self.link_child_table_checked(check_state, row)

    def make_checkbox_num_widget(self, row_index, col_data):
        if col_data.children:
            button = QToolButton()
            button.setIcon(get_icon(EXPAND_CHILD_TABLE_ICON))
            button.clicked.connect(
                lambda: self.add_child_table_func(col_data, row_index))
        else:
            button = QLabel()
        return make_checkbox_num_button(row_index + 1, self.click_row_checkbox, button)

    def fill_post_process(self):
        checked_list, child_table_count = list(), 0
        # 循环设置选中项
        for row, col in enumerate(self.cols):
            if col.checked:
                checked_list.append(col)
                # 需要展开子表的不处理，因为子表会自动联动父行状态
                if not col.expanded:
                    self.cellWidget(row + child_table_count, 0).check_box.setCheckState(Qt.CheckState.Checked)
            if col.expanded:
                self.add_child_table_func(col, row, reopen=True)
                child_table_count += 1
        if checked_list:
            # 将选中项保存到选中树结构中
            self.add_checked_data(checked_list)
            # 在重新填充表格时，需要考虑一种情况：之前已经选中但是未展示的子表，也应该添加到选中数据中
            self.add_children_checked_data(checked_list)

    def get_actual_row_index(self, row):
        # 找到给定行索引之前的所有行（row：列数据列表中的索引值）
        before_rows = self.cols[:row]
        # 之前行中存在的子表数
        child_tables = len([row for row in before_rows if row.has_child_table])
        # 所以当前行的实际索引值 = 在列数据列表中的索引值 + 存在的子表数
        return row + child_tables

    def add_child_table_func(self, col_data, row_index, reopen=False):
        # 获取真实的行索引值
        actual_row_index = self.get_actual_row_index(row_index)
        # 获取添加子表格的 button，这里必须使用当前的实际行数获取部件，不能直接用创建表格时的行数计算，因为可能前面行会增加
        button: QToolButton = self.cellWidget(actual_row_index, 0).button
        # 新的子表，需要在当前行下，新插入一行放入子表，
        # 子表的索引 = 当前实际行索引 + 1
        child_table_row_index = actual_row_index + 1
        # 如果是重新打开表，渲染界面，那么直接插入新的子表
        if reopen:
            self.add_child_table(child_table_row_index, col_data)
            button.setIcon(get_icon(COLLAPSE_CHILD_TABLE_ICON))
        else:
            # 如果表格已经显示，再次点击应该隐藏子表
            if col_data.expanded:
                button.setIcon(get_icon(EXPAND_CHILD_TABLE_ICON))
                self.hideRow(child_table_row_index)
                col_data.expanded = 0
            else:
                button.setIcon(get_icon(COLLAPSE_CHILD_TABLE_ICON))
                col_data.expanded = 1
                # 如果存在子表，但是被隐藏了，展示即可，否则应该创建表
                if col_data.has_child_table:
                    self.showRow(child_table_row_index)
                else:
                    self.add_child_table(child_table_row_index, col_data)
            # 保存数据
            self.async_save_executor.update_col_expanded(col_data)
        self.resize_child_table_row(child_table_row_index)

    def add_child_table(self, row_index, col_data):
        # 还没有创建过子表，创建一个新的子表
        # 首先插入新行
        self.insert_row(row_index)
        # 为了美观，将新行单元格所有列合并
        self.setSpan(row_index, 0, 1, 6)
        child_table_widget = self.do_add_child_table(col_data)
        self.setCellWidget(row_index, 0, child_table_widget)
        # 标记当前列数据，已经存在子表
        col_data.has_child_table = 1

    def do_add_child_table(self, col_data):
        child_widget = QWidget()
        # 维护树节点引用，方便子表格使用
        child_widget.tree_item = self.tree_item
        child_layout = QHBoxLayout()
        child_widget.setLayout(child_layout)
        # 创建子表格
        child_table = StructDsColTableWidget(self.tree_widget, child_widget,
                                             col_data.children, parent_table=self)
        child_widget.child_table = child_table
        child_layout.addWidget(child_table)

        # 连接表头信号，当子表表头变化时，应该触发父表对应行复选框变化
        child_table.table_header.header_check_changed.connect(
            lambda check_state: self.change_parent_col_check_state(check_state, col_data))

        child_table.fill_table()
        return child_widget

    def change_parent_col_check_state(self, check_state, col_data):
        # 获取子表在父表中的实际行索引，当前行之前的行（列数据列表）
        row_index = self.get_actual_row_index(self.cols.index(col_data))
        # 设置父行复选框状态
        self.cellWidget(row_index, 0).check_box.setCheckState(check_state)
        # 重新计算表头复选框状态
        self.table_header.calculate_header_check_state()

    def resize_child_table_row(self, row_index):
        child_table_widget = self.cellWidget(row_index, 0)
        child_table: DsColTableWidgetABC = child_table_widget.child_table
        # 子表的所有行的高度 = 所有未隐藏行的高度之和
        child_table_row_height = 0
        for row in range(child_table.rowCount()):
            if not child_table.isRowHidden(row):
                child_table_row_height += child_table.rowHeight(row)
        # 当前子表所在行行高 = 子表所有行的高度 + 子表表头高度 x 2 （主要是为了美观，所以拉大距离）
        self.setRowHeight(row_index, child_table_row_height + (child_table.table_header.height() << 1))

        # 如果当前表也是个子表，那么当前表行大小变化，可能会引起当前表的父表行大小变化，所以调用父表，重新计算行大小
        if self.parent_table:
            for row in range(self.parent_table.rowCount()):
                table_cell_widget = self.parent_table.cellWidget(row, 0)
                if hasattr(table_cell_widget, 'child_table') and table_cell_widget.child_table is self:
                    self.parent_table.resize_child_table_row(row)

    def add_children_checked_data(self, checked_col_list):
        for checked_col in checked_col_list:
            # 如果存在子项，但是不存在子表，将数据选中
            if checked_col.children and not checked_col.has_child_table:
                self.add_checked_data(checked_col.children)
                self.add_children_checked_data(checked_col.children)

    def click_row_checkbox(self, checked, row):
        super().click_row_checkbox(checked, row)
        self.link_child_table_checked(checked, int(row) - 1)

    def link_child_table_checked(self, checked, row):
        """当前行复选框变化时，如果存在子表，应该联动子表的复选框"""
        if self.cols[row].has_child_table:
            # 实际行索引
            actual_row_index = self.get_actual_row_index(row)
            # 子表所在行 = 实际行索引 + 1
            child_table = self.cellWidget(actual_row_index + 1, 0).child_table
            child_table.table_header.link_header_check_state(checked)
            # 批量处理
            child_table.batch_deal_checked(checked)
        # 当前列数据如果存在子项并且还没有创建子表，应该同步子项选中状态并保存
        elif not self.cols[row].has_child_table and self.cols[row].children:
            # 递归处理
            self.recursive_update_children_checked(self.cols[row].children, checked)

    def recursive_update_children_checked(self, cols, checked):
        self.batch_update_check_state(cols, checked)
        for child_row in range(len(cols)):
            if cols[child_row].children:
                self.recursive_update_children_checked(cols[child_row].children, checked)

    def get_add_del_col_data(self, add_del_data, checked_cols):
        """根据选中数据获取表层次的数据，由于选择的列数据是最底层，所以需要依次推导出上一层节点，构造层次数据"""
        # 获取父列数据，选中的列一定属于同一个表格内，所以它们拥有共同的父列
        parent_col = checked_cols[0].parent_col if isinstance(checked_cols, list) else checked_cols.parent_col
        # 如果父列存在，那么继续寻找上一层
        if parent_col:
            self.get_add_del_col_data(add_del_data, parent_col)
        # 构建表层次数据
        add_del_data[max(add_del_data) + 1] = checked_cols

    def add_checked_data(self, cols):
        # 首先获取树节点层次数据
        add_data = get_add_del_data(self.tree_item)
        # 获取表层次数据
        self.get_add_del_col_data(add_data, cols)
        self.tree_data.add_node(add_data)

    def remove_checked_data(self, cols):
        # 首先获取树节点层次数据
        del_data = get_add_del_data(self.tree_item)
        # 获取表层次数据
        self.get_add_del_col_data(del_data, cols)
        self.tree_data.del_node(del_data)

    def remove_all_table_checked(self, cols):
        self.remove_checked_data(cols)

    def update_checked_data(self, col_data):
        # 首先获取树节点层次数据
        update_data = get_add_del_data(self.tree_item)
        # 获取表层次数据
        self.get_add_del_col_data(update_data, col_data)
        self.tree_data.update_node_name(update_data)

