# -*- coding: utf-8 -*-
"""
表格结构，大体与树结构类似
"""
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView, QWidget, QHBoxLayout, QCheckBox

from constant_.constant import TABLE_HEADER_LABELS
from view.custom_widget.scrollable_widget import ScrollableWidget
from view.table.table_header import CheckBoxHeader
from view.table.table_item import TableWidgetItem
from view.table.table_item_delegate import ComboboxDelegate, TextInputDelegate

_author_ = 'luwt'
_date_ = '2022/5/10 15:25'


class TableWidget(QTableWidget, ScrollableWidget):

    # 定义信号，点击第一列复选框时，发送当前选中状态、第二列的字段名称和当前行
    item_checkbox_clicked = pyqtSignal(bool, str, int)

    def __init__(self, parent):
        super().__init__(parent)
        self.table_header = ...
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
        self.table_header = CheckBoxHeader()
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
        self.itemChanged.connect(self.change)
        # 需要开启鼠标追踪，才能实现tooltip
        self.setMouseTracking(True)
        self.entered.connect(self.show_tool_tip)

    def show_tool_tip(self, model_index):
        self.setToolTip(model_index.data())

    def change(self, item):
        if not self.filling_table:
            # 如果是第一列，查看选中状态
            if item.column() == 0:
                print(item.row(), item.column(), item.checkState())
            else:
                print(item.text())

    def fill_table(self, cols):
        """
        将列名字段全数填充在表中，四列多行表
        :param cols: 字段信息的数组
        """
        self.filling_table = True
        # 填充数据
        for i, col in enumerate(cols):
            # 插入新的一行
            self.insertRow(i)
            # 设置checkbox在第一列
            self.setCellWidget(i, 0, self.make_checkbox_num_item(i, col.checked))

            self.setItem(i, 1, self.make_item(col.col_name))
            self.setItem(i, 2, self.make_item(col.data_type))
            self.setItem(i, 3, self.make_item(col.full_data_type))
            self.setItem(i, 4, self.make_item(col.is_pk))
            self.setItem(i, 5, self.make_item(col.col_comment))
        # 设置表格根据内容调整
        self.resizeRowsToContents()
        self.filling_table = False

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

        # 收集复选框
        self.table_header.all_header_combobox.append(check_box)
        return table_check_widget
