# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QWidget, QHBoxLayout, QToolButton

from src.constant.constant import TABLE_HEADER_LABELS, EXPAND_CHILD_TABLE, COLLAPSE_CHILD_TABLE
from src.constant.icon_enum import get_icon
from src.service.async_func.async_tab_table_task import AsyncSaveTabObjExecutor
from src.service.system_storage.ds_table_col_info_sqlite import DsTableColInfo
from src.view.custom_widget.check_box import CheckBox
from src.view.table.table_header.check_box_table_header import CheckBoxHeader
from src.view.table.table_item.table_item_delegate import ComboboxDelegate
from src.view.table.table_widget.abstract_table_widget import AbstractTableWidget

_author_ = 'luwt'
_date_ = '2022/12/6 15:50'


class AbstractDsColTableWidget(AbstractTableWidget):

    def __init__(self, main_window, tree_widget, parent, cols, parent_table=None):
        self.main_window = main_window
        self.tree_widget = tree_widget
        self.cols = cols
        # 获取tab widget中的队列线程执行器
        self.async_save_executor = self.get_async_save_executor()
        # 选中数据
        self.tree_data = self.tree_widget.tree_data
        self.tree_item = parent.tree_item
        self.table_header: CheckBoxHeader = ...
        self.filling_table = False
        # 进行批量处理的时候，标志位置为true，不再触发单行复选框的处理逻辑
        self.batch_operating = False
        self.parent_table: AbstractDsColTableWidget = parent_table
        # 保存代理引用
        self.combox_delegate = ...
        super().__init__(parent)

    def get_async_save_executor(self) -> AsyncSaveTabObjExecutor:
        return self.tree_widget.get_current_tab_widget().async_save_executor

    def setup_other_ui(self):
        # 设置双击触发修改
        self.setEditTriggers(QAbstractItemView.DoubleClicked)

        # 设置表格列数
        self.setColumnCount(len(TABLE_HEADER_LABELS))
        # 实例化自定义表头
        self.table_header = CheckBoxHeader(parent=self, batch_callback=self.set_batch_operating)
        self.table_header.setObjectName("table_header")
        # 设置表头
        self.setHorizontalHeader(self.table_header)
        # 设置表头字段
        self.setHorizontalHeaderLabels(TABLE_HEADER_LABELS)
        # 设置表头列宽度，第一列全选列
        self.horizontalHeader().resizeSection(0, 80)
        # 第二列字段列，根据大小自动调整宽度
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # 最后备注列拉伸到最大
        self.horizontalHeader().setStretchLastSection(True)

        # 设置第五列（是否是主键）combox代理项，在编辑时触发
        self.combox_delegate = ComboboxDelegate()
        self.setItemDelegateForColumn(4, self.combox_delegate)
        # 第2,3,4,6列设置编辑代理项
        self.set_text_input_delegate((1, 2, 3, 5))

    def connect_other_signal(self):
        # 单行数据变化时，触发
        self.itemChanged.connect(self.data_change)
        # 连接表头复选框点击信号，向下传递选中状态，例如父表表头选中，对应子表表头也应选中
        self.table_header.header_clicked.connect(self.batch_deal_checked)

    def data_change(self, item):
        # 数据变化时触发
        if self.get_allow_checkbox_emit_signal():
            # 保存数据
            self.save_data(item.row(), item.column(), item.text())

    def batch_deal_checked(self, check_state):
        # 调用批量处理方法保存数据
        self.batch_update_check_state(self.cols, check_state)
        # 检查每一行是否有子表，如果存在子表，联动子表复选框
        [self.link_child_table_checked(check_state, row) for row in range(len(self.cols))]

    def set_batch_operating(self, flag):
        self.batch_operating = flag

    def get_allow_checkbox_emit_signal(self):
        return not (self.filling_table or self.batch_operating)

    def fill_table(self):
        """
        根据列数据构建表格
        """
        self.filling_table = True
        checked_col_list = list()
        # 填充数据
        for i, col in enumerate(self.cols):
            # 插入新的一行
            self.insertRow(i)
            # 设置checkbox在第一列
            self.setCellWidget(i, 0, self.make_checkbox_num_item(i, col))

            if col.checked:
                checked_col_list.append(col)

            self.setItem(i, 1, self.make_item(col.col_name))
            self.setItem(i, 2, self.make_item(col.data_type))
            self.setItem(i, 3, self.make_item(col.full_data_type))
            self.setItem(i, 4, self.make_item('是' if col.is_pk else '否'))
            self.setItem(i, 5, self.make_item(col.col_comment if col.col_comment else ''))

            # 根据当前行内容调整行大小
            self.resizeRowToContents(i)

        # 填充完主表格后，进行子表格处理，这样分开处理比较简单，
        # 如果在创建主表格的同时进行子表格插入，那么循环的索引和实际的表格行数将存在偏差
        for i, col in enumerate(self.cols):
            if not col.expanded and col.checked:
                # 填充表格后，统一设置checkbox状态，之所以在这里设置，而不是在创建复选框时设置，是因为需要考虑到复选框变化信号槽触发时机，
                # 如果在创建复选框时设置，那么将触发复选框变化信号槽函数，对表头状态进行设置，而此时并未完全创建所有复选框，会导致表头状态错误；
                # 这里只处理没有子表的情况，因为子表会自动触发父行复选框状态变化
                self.table_header.checkbox_list[i].setCheckState(Qt.Checked)
            elif col.expanded:
                self.add_child_table_func(col, i, reopen=True)
        # 联动表头
        self.table_header.link_header_checked()

        self.filling_table = False

        # 保存选中数据
        if checked_col_list:
            self.add_checked_data(checked_col_list)
            # 在重新填充表格时，需要考虑一种情况：之前已经选中但是未展示的子表，也应该添加到选中数据中
            self.add_children_checked_data(checked_col_list)

    def add_children_checked_data(self, checked_col_list):
        for checked_col in checked_col_list:
            # 如果存在子项，但是不存在子表，将数据选中
            if checked_col.children and not checked_col.has_child_table:
                self.add_checked_data(checked_col.children)
                self.add_children_checked_data(checked_col.children)

    def add_checked_data(self, cols): ...

    def remove_checked_data(self, cols): ...

    def remove_all_table_checked(self, cols): ...

    def update_checked_data(self, col_data): ...

    def make_checkbox_num_item(self, row_index, col_data):
        table_check_widget = QWidget()
        check_layout = QHBoxLayout(table_check_widget)

        check_box = CheckBox(allow_emit_signal=self.get_allow_checkbox_emit_signal)
        check_layout.addWidget(check_box)
        # 如果存在子项，就添加一个展开按钮，连接打开子表方法
        if col_data.children:
            add_child_table_button = QToolButton()
            add_child_table_button.setIcon(get_icon(EXPAND_CHILD_TABLE))
            add_child_table_button.clicked.connect(
                lambda: self.add_child_table_func(col_data, row_index))

            check_layout.addWidget(add_child_table_button)
            # 增加引用，方便槽函数调用
            table_check_widget.add_child_table_button = add_child_table_button

        # 设置布局的左间距变小，主要是为了与表头的复选框对齐
        check_layout.setContentsMargins(4, check_layout.contentsMargins().top(),
                                        check_layout.contentsMargins().right(),
                                        check_layout.contentsMargins().bottom())

        check_box.setText(str(row_index + 1))
        # 复选框点击变化事件
        check_box.click_state_changed.connect(lambda check_state:
                                              self.click_row_checkbox(check_state, row_index))
        # 复选框非点击情况下（子表表头变化，导致父表所在行复选框变化），复选框状态变化信号
        check_box.not_click_state_changed.connect(lambda check_state: self.checkbox_state_changed())
        # 收集复选框
        self.table_header.checkbox_list.append(check_box)
        return table_check_widget

    def add_child_table_func(self, col_data, row_index, reopen=False):
        # 当前行之前的行（列数据列表）
        before_rows = self.cols[:row_index]
        # 当前行之前的行，存在的子表数
        child_tables = len(list(filter(lambda x: x.has_child_table, before_rows)))
        # 获取添加子表格的 button，这里必须使用当前的实际行数获取部件，不能直接用创建表格时的行数计算，因为可能前面行会增加
        button = self.cellWidget(row_index + child_tables, 0).__getattribute__('add_child_table_button')
        # 新的子表，需要在当前行下，新插入一行放入子表，
        # 下一行的索引 = 当前行索引 + 当前行之前，已经插入的新行 + 1
        row_index += 1 + child_tables
        # 如果是重新打开表，渲染界面，那么直接插入新的字表
        if reopen:
            self.add_child_table(row_index, col_data)
            button.setIcon(get_icon(COLLAPSE_CHILD_TABLE))
        else:
            # 如果表格已经显示，再次点击应该隐藏子表
            if col_data.expanded:
                button.setIcon(get_icon(EXPAND_CHILD_TABLE))
                self.hideRow(row_index)
                col_data.expanded = 0
            else:
                button.setIcon(get_icon(COLLAPSE_CHILD_TABLE))
                col_data.expanded = 1
                # 如果存在子表，但是被隐藏了，展示即可，否则应该创建表
                if col_data.has_child_table:
                    self.showRow(row_index)
                else:
                    self.add_child_table(row_index, col_data)
            # 保存数据
            self.update_col_expanded(col_data)
        self.resize_child_table_row(row_index)

    def add_child_table(self, row_index, col_data):
        # 还没有创建过子表，创建一个新的子表
        # 首先插入新行
        self.insertRow(row_index)
        # 为了美观，将新行单元格所有列合并
        self.setSpan(row_index, 0, 1, 6)
        child_table_widget = self.do_add_child_table(col_data, row_index)
        self.setCellWidget(row_index, 0, child_table_widget)
        # 标记当前列数据，已经存在子表
        col_data.has_child_table = 1

    def resize_child_table_row(self, row_index):
        child_table_widget = self.cellWidget(row_index, 0)
        child_table: AbstractDsColTableWidget = child_table_widget.child_table
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

    def do_add_child_table(self, col_data, row_index) -> QWidget: ...

    def click_row_checkbox(self, checked, row):
        # 将列数据置为选中状态，保存数据
        self.save_data(row, 0, checked)
        # 联动表头
        self.table_header.link_header_checked()
        self.link_child_table_checked(checked, row)

    def checkbox_state_changed(self):
        # 联动表头，该方法仅在由子表变化，导致父行变化，联动父表的表头事件
        self.table_header.link_header_checked()

    def link_child_table_checked(self, checked, row):
        """当前行复选框变化时，如果存在子表，应该联动子表的复选框"""
        if self.cols[row].has_child_table:
            # 当前行之前的行（列数据列表）
            before_rows = self.cols[:row]
            # 当前行之前的行，存在的子表数
            child_tables = len(list(filter(lambda x: x.has_child_table, before_rows)))
            # 子表所在行 = 行数 + 当前行之前存在的子表数 + 1
            child_table = self.cellWidget(row + child_tables + 1, 0).child_table
            child_table.table_header.change_header_state(checked)
            # 批量处理
            child_table.batch_deal_checked(checked)
        # 当前列数据如果存在子项并且还没有创建子表，应该同步子项选中状态并保存
        elif not self.cols[row].has_child_table and self.cols[row].children:
            self.batch_update_check_state(self.cols[row].children, checked)

    def save_data(self, row, col, data):
        # 根据row找到对应的列信息数据
        col_data = self.cols[row]
        modify_col_data = DsTableColInfo()
        modify_col_data.id = col_data.id

        if col == 0:
            col_data.checked = data
            modify_col_data.checked = data

            # 保存到树选中数据中，由于保存的列对象是从 self.cols中取的，
            # 所以树中保存的列对象引用指向列表中对象，在数据变化时，无需手动同步
            # 如果是选中，则为添加数据，否则为删除数据
            # 当复选框状态变化时，再处理添加或删除选中数据
            if col_data.checked:
                self.add_checked_data(col_data)
            else:
                self.remove_checked_data(col_data)
        elif col == 1:
            col_data.col_name = data
            modify_col_data.col_name = data

            # 当名称变化时，需要同步更新选中数据
            if col_data.checked:
                self.update_checked_data(col_data)
        elif col == 2:
            col_data.data_type = data
            modify_col_data.data_type = data
        elif col == 3:
            col_data.full_data_type = data
            modify_col_data.full_data_type = data
        elif col == 4:
            is_pk = 1 if data == '是' else 0
            col_data.is_pk = is_pk
            modify_col_data.is_pk = is_pk
        elif col == 5:
            col_data.col_comment = data
            modify_col_data.col_comment = data

        # 保存数据
        self.async_save_executor.save_table_data(modify_col_data)

    def batch_update_check_state(self, cols, check_state):
        modify_col_data_list = list()
        for col in cols:
            if col.checked != check_state:
                col.checked = check_state
                modify_col_data = DsTableColInfo()
                modify_col_data.id = col.id
                modify_col_data.checked = check_state
                modify_col_data_list.append(modify_col_data)
        if not modify_col_data_list:
            return
        # 保存数据
        self.async_save_executor.batch_save_data(modify_col_data_list)
        # 批量选中数据或取消选中
        if check_state == Qt.Unchecked:
            self.remove_all_table_checked(cols)
        elif check_state == Qt.Checked:
            self.add_checked_data(cols)

    def update_col_expanded(self, col):
        self.async_save_executor.update_col_expanded(col)
