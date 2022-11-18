# -*- coding: utf-8 -*-
"""
表格结构，大体与树结构类似
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView, QWidget, QHBoxLayout, QCheckBox

from constant_.constant import TABLE_HEADER_LABELS
from service.system_storage.ds_table_info_sqlite import DsTableInfo
from view.custom_widget.scrollable_widget import ScrollableWidget
from view.table.table_header import CheckBoxHeader
from view.table.table_item import TableWidgetItem
from view.table.table_item_delegate import ComboboxDelegate, TextInputDelegate
from view.tree.tree_item.tree_item_func import get_item_sql_conn, get_item_opened_record

_author_ = 'luwt'
_date_ = '2022/5/10 15:25'


class TableWidget(QTableWidget, ScrollableWidget):

    def __init__(self, parent, cols):
        super().__init__(parent)
        self.cols = cols
        # 获取tab widget中的队列线程执行器
        self.async_save_executor = self.parent().parent()\
            .main_window.sql_tab_widget.async_save_executor
        # 选中数据
        self.tree_data = self.parent().parent().main_window.sql_tree_widget.tree_data
        self.tree_item = parent.tree_item
        self.table_header: CheckBoxHeader = ...
        self.filling_table = False
        # 保存代理引用，否则将会被垃圾回收
        self.combox_delegate = ...
        self.text_input_delegate = ...
        self.setup_ui()
        self.connect_signal()

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
        self.horizontalHeader().resizeSection(0, 60)
        # 第二列字段列，根据大小自动调整宽度
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # 最后备注列拉伸到最大
        self.horizontalHeader().setStretchLastSection(True)
        # 默认行号隐藏
        self.verticalHeader().setHidden(True)

        # 设置第五列（是否是主键）combox代理项，在编辑时触发
        self.combox_delegate = ComboboxDelegate()
        self.setItemDelegateForColumn(4, self.combox_delegate)
        # 第六列设置代理项
        self.text_input_delegate = TextInputDelegate()
        self.setItemDelegateForColumn(5, self.text_input_delegate)

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

    def fill_table(self):
        """
        将列名字段全数填充在表中，四列多行表
        """
        self.filling_table = True
        checked_col_list = list()
        # 填充数据
        for i, col in enumerate(self.cols):
            # 插入新的一行
            self.insertRow(i)
            # 设置checkbox在第一列
            self.setCellWidget(i, 0, self.make_checkbox_num_item(i, col.checked))

            if col.checked:
                checked_col_list.append(col)

            self.setItem(i, 1, self.make_item(col.col_name))
            self.setItem(i, 2, self.make_item(col.data_type))
            self.setItem(i, 3, self.make_item(col.full_data_type))
            self.setItem(i, 4, self.make_item('是' if col.is_pk else '否'))
            self.setItem(i, 5, self.make_item(col.col_comment))
        # 设置表格根据内容调整
        self.resizeRowsToContents()
        self.filling_table = False

        # 保存选中数据
        if checked_col_list:
            self.add_checked_data(checked_col_list)

    def add_checked_data(self, cols):
        sql_conn = get_item_sql_conn(self.tree_item.parent().parent())
        add_data = {
            'conn': get_item_opened_record(self.tree_item.parent().parent()),
            'db': get_item_opened_record(self.tree_item.parent()),
            'tb': get_item_opened_record(self.tree_item),
            'col': cols,
        }
        self.tree_data.add_node(add_data, sql_conn)

    def remove_checked_data(self, cols):
        del_data = {
            'conn': self.tree_item.parent().parent().text(0),
            'db': self.tree_item.parent().text(0),
            'tb': self.tree_item.text(0),
            'col': cols,
        }
        self.tree_data.del_node(del_data, recursive_del=True)

    def add_all_table_cols_checked(self):
        self.add_checked_data(self.cols)

    def remove_all_table_checked(self):
        del_data = {
            'conn': self.tree_item.parent().parent().text(0),
            'db': self.tree_item.parent().text(0),
            'tb': self.tree_item.text(0)
        }
        self.tree_data.del_node(del_data, recursive_del=True)

    def make_item(self, text):
        item = TableWidgetItem(self)
        item.setText(text)
        return item

    def make_checkbox_num_item(self, i, check_state):
        table_check_widget = QWidget()
        check_layout = QHBoxLayout(table_check_widget)

        check_box = QCheckBox()
        check_layout.addWidget(check_box)
        # 设置布局的左间距变小，主要是为了与表头的复选框对齐
        check_layout.setContentsMargins(4, check_layout.contentsMargins().top(),
                                        check_layout.contentsMargins().right(),
                                        check_layout.contentsMargins().bottom())

        # 设置checkbox状态
        check_box.setText(str(i + 1))
        if check_state:
            check_box.setCheckState(Qt.Checked)
        # 点击时需要保存数据，并联动表头复选框
        check_box.clicked.connect(lambda checked: self.click_row_checkbox(checked, i))

        # 收集复选框
        self.table_header.checkbox_list.append(check_box)
        return table_check_widget

    def click_row_checkbox(self, checked, row):
        # 联动表头
        self.table_header.link_header_checked()
        # 选中一行数据
        if not self.filling_table:
            # 将列数据置为选中状态，保存数据
            self.save_data(row, 0, checked)

    def save_data(self, row, col, data):
        # 根据row找到对应的列信息数据
        col_data = self.cols[row]
        modify_col_data = DsTableInfo()
        modify_col_data.id = col_data.id

        if col == 0:
            col_data.checked = data
            modify_col_data.checked = data
        elif col == 1:
            col_data.col_name = data
            modify_col_data.col_name = data
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

        # 保存到树选中数据中，由于保存的列对象是从 self.cols中取的，
        # 所以树中保存的列对象引用指向列表中对象，在数据变化时，无需手动同步
        # 如果是选中，则为添加数据，否则为删除数据
        if col_data.checked:
            self.add_checked_data(col_data)
        else:
            self.remove_checked_data(col_data)

        # 保存数据
        self.async_save_executor.save_table_data(modify_col_data)

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
