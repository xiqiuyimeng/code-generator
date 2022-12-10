# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QHeaderView, QWidget, QHBoxLayout, QCheckBox, QToolButton

from constant.constant import TABLE_HEADER_LABELS, EXPAND_CHILD_TABLE, COLLAPSE_CHILD_TABLE
from constant.icon_enum import get_icon
from service.async_func.async_tab_table_task import AsyncSaveTabObjExecutor
from service.system_storage.ds_table_info_sqlite import DsTableInfo
from service.util.tree_node import TreeData
from view.custom_widget.scrollable_widget import ScrollableWidget
from view.table.table_header import CheckBoxHeader
from view.table.table_item import TableWidgetItem
from view.table.table_item_delegate import ComboboxDelegate, TextInputDelegate

_author_ = 'luwt'
_date_ = '2022/12/6 15:50'


class AbstractTableWidget(QTableWidget, ScrollableWidget):

    def __init__(self, main_window, parent, cols):
        super().__init__(parent)
        self.main_window = main_window
        self.cols = cols
        # 获取tab widget中的队列线程执行器
        self.async_save_executor = self.get_async_save_executor()
        # 选中数据
        self.tree_data = self.get_tree_data()
        self.tree_item = parent.tree_item
        self.table_header: CheckBoxHeader = ...
        self.filling_table = False
        # 保存代理引用，否则将会被垃圾回收
        self.combox_delegate = ...
        self.text_input_delegate = ...
        self.setup_ui()
        self.connect_signal()

    def get_async_save_executor(self) -> AsyncSaveTabObjExecutor: ...

    def get_tree_data(self) -> TreeData: ...

    def setup_ui(self):
        # 设置双击触发修改
        self.setEditTriggers(QAbstractItemView.DoubleClicked)
        # 交替行颜色
        self.setAlternatingRowColors(True)

        # 表格设置为6列
        self.setColumnCount(6)
        # 实例化自定义表头
        self.table_header = CheckBoxHeader(parent=self)
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
        # 默认行号隐藏
        self.verticalHeader().setHidden(True)

        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # 设置第五列（是否是主键）combox代理项，在编辑时触发
        self.combox_delegate = ComboboxDelegate()
        self.setItemDelegateForColumn(4, self.combox_delegate)
        # 第六列设置代理项
        self.text_input_delegate = TextInputDelegate()
        self.setItemDelegateForColumn(5, self.text_input_delegate)

        # 按像素滚动
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

    def connect_signal(self):
        self.itemChanged.connect(self.data_change)
        # 需要开启鼠标追踪，才能实现tooltip
        self.setMouseTracking(True)
        self.entered.connect(self.show_tool_tip)

    def data_change(self, item):
        # 数据变化时触发
        if not self.filling_table:
            # 保存数据
            self.save_data(item.row(), item.column(), item.text())

    def show_tool_tip(self, model_index):
        self.setToolTip(model_index.data())

    def fill_table(self): ...

    def add_checked_data(self, cols): ...

    def remove_checked_data(self, cols): ...

    def add_all_table_cols_checked(self):
        self.add_checked_data(self.cols)

    def remove_all_table_checked(self): ...

    def make_item(self, text):
        item = TableWidgetItem(self)
        item.setText(text)
        return item

    def make_checkbox_num_item(self, row_index, col_data):
        table_check_widget = QWidget()
        check_layout = QHBoxLayout(table_check_widget)

        check_box = QCheckBox()
        check_layout.addWidget(check_box)
        # 如果存在子项，就添加一个展开按钮，连接打开子表方法
        if col_data.children:
            add_child_table_button = QToolButton()
            add_child_table_button.setIcon(get_icon(EXPAND_CHILD_TABLE))
            add_child_table_button.clicked.connect(
                lambda: self.add_child_table_func(col_data, row_index, add_child_table_button))

            check_layout.addWidget(add_child_table_button)

        # 设置布局的左间距变小，主要是为了与表头的复选框对齐
        check_layout.setContentsMargins(4, check_layout.contentsMargins().top(),
                                        check_layout.contentsMargins().right(),
                                        check_layout.contentsMargins().bottom())

        # 设置checkbox状态
        check_box.setText(str(row_index + 1))
        if col_data.checked:
            check_box.setCheckState(Qt.Checked)
        # 点击时需要保存数据，并联动表头复选框
        check_box.clicked.connect(lambda checked: self.click_row_checkbox(checked, row_index))

        # 收集复选框
        self.table_header.checkbox_list.append(check_box)
        return table_check_widget

    def add_child_table_func(self, col_data, row_index, button):
        # 当前行之前的行（列数据列表）
        before_rows = self.cols[:row_index]
        # 当前行之前的行，存在的子表数
        child_tables = len(list(filter(lambda x: x.has_child_table, before_rows)))
        # 新的子表，需要在当前行下，新插入一行放入子表，
        # 下一行的索引 = 当前行索引 + 当前行之前，已经插入的新行 + 1
        row_index += 1 + child_tables
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
                # 还没有创建过子表，创建一个新的子表
                # 首先插入新行
                self.insertRow(row_index)
                # 为了美观，将新行单元格所有列合并
                self.setSpan(row_index, 0, 1, 6)
                child_table = self.add_child_table(col_data.children, row_index)
                self.setCellWidget(row_index, 0, child_table)
                # 标记当前列数据，已经存在子表
                col_data.has_child_table = 1

    def add_child_table(self, children_cols, row_index) -> QWidget: ...

    def click_row_checkbox(self, checked, row):
        # 联动表头
        self.table_header.link_header_checked()
        # 选中一行数据
        if not self.filling_table:
            # 将列数据置为选中状态，保存数据
            self.save_data(row, 0, checked)

    def save_data(self, row, col, data): ...

    def batch_update_check_state(self, check_state):
        modify_col_data_list = list()
        for col in self.cols:
            col.checked = check_state
            modify_col_data = DsTableInfo()
            modify_col_data.id = col.id
            modify_col_data.checked = check_state
            modify_col_data_list.append(modify_col_data)
        # 保存数据
        self.async_save_executor.batch_save_data(modify_col_data_list)
        # 批量选中数据或取消选中
        if check_state == Qt.Unchecked:
            self.remove_all_table_checked()
        elif check_state == Qt.Checked:
            self.add_all_table_cols_checked()