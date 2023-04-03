# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from src.constant.table_constant import DS_COL_TYPE_TABLE_HEADER, DEFAULT_MAPPING_GROUP_TITLE
from src.view.table.table_header.table_header_abc import TableHeaderABC
from src.view.table.table_header.table_header_style_delegate import TableHeaderStyleDelegate, \
    ColTypeMappingTableHeaderStyleDelegate

_author_ = 'luwt'
_date_ = '2023/2/16 17:41'


class ColTypeMappingTableHeaderABC(TableHeaderABC):
    # 组号变化信号
    group_num_changed = pyqtSignal(int)

    def __init__(self, *args):
        # 表头2行5列
        super().__init__(2, 5, *args)

    def setup_item_span(self):
        # 设置第一列，合并两行
        self.setSpan(0, 0, 2, 1)
        self.setSpan(0, 1, 2, 1)
        self.setup_other_item_span()

    def setup_header_items(self):
        # 设置表头文本
        self.setItem(0, 1, self.make_item(DS_COL_TYPE_TABLE_HEADER[0]))

    def setup_other_item_span(self): ...


class ColTypeMappingFrozenTableHeader(ColTypeMappingTableHeaderABC):

    def __init__(self, *args):
        super().__init__(*args)
        # 设置代理
        self.setItemDelegate(TableHeaderStyleDelegate())

    def setup_header_items(self):
        super().setup_header_items()
        # 隐藏前两列之后所有列
        [self.setColumnHidden(col, True) for col in range(2, self.columnCount())]


class ColTypeMappingTableHeader(ColTypeMappingTableHeaderABC):

    def __init__(self, *args):
        self.max_group_num = 0
        super().__init__(*args)
        # 设置代理
        self.setItemDelegate(ColTypeMappingTableHeaderStyleDelegate())

    def setup_other_item_span(self):
        # 合并列
        self.setSpan(0, 2, 1, 3)
        self.setSpan(1, 2, 1, 1)
        self.setSpan(1, 3, 1, 1)
        self.setSpan(1, 4, 1, 1)

    def setup_header_items(self):
        super().setup_header_items()
        # 设置表头文本
        self.setItem(0, 2, self.make_item(DEFAULT_MAPPING_GROUP_TITLE))

        self.setItem(1, 2, self.make_item(DS_COL_TYPE_TABLE_HEADER[1]))
        self.setItem(1, 3, self.make_item(DS_COL_TYPE_TABLE_HEADER[2]))
        self.setItem(1, 4, self.make_item(DS_COL_TYPE_TABLE_HEADER[3]))

    def add_type_mapping_group(self):
        # 增加1组3列
        column_count = self.horizontalHeader().count()
        self.insertColumn(column_count)
        self.insertColumn(column_count + 1)
        self.insertColumn(column_count + 2)
        # 合并单元格
        self.setSpan(0, column_count, 1, 3)

        self.setItem(0, column_count, self.make_item(self._get_group_title()))
        self.setItem(1, column_count, self.make_item(DS_COL_TYPE_TABLE_HEADER[1]))
        self.setItem(1, column_count + 1, self.make_item(DS_COL_TYPE_TABLE_HEADER[2]))
        self.setItem(1, column_count + 2, self.make_item(DS_COL_TYPE_TABLE_HEADER[3]))

        # 发射信号
        self.group_num_changed.emit(self.max_group_num)

    def _get_group_title(self):
        self.max_group_num += 1
        return f'映射组{self.max_group_num}'

    def del_type_mapping_group(self):
        column_count = self.columnCount()
        self.removeColumn(column_count - 1)
        self.removeColumn(column_count - 2)
        self.removeColumn(column_count - 3)
        # 将组号减1
        self.max_group_num -= 1
        # 发射信号
        self.group_num_changed.emit(self.max_group_num)

    def get_ds_col_type_title(self):
        return self.item(0, 1).text()

    def get_mapping_col_name_title(self):
        return self.item(1, 2).text()

    def get_mapping_type_title(self):
        return self.item(1, 3).text()

    def get_mapping_group_title(self, col):
        # 因为组名在每组的第三列，所以应该计算当前列所在组的第三列索引值
        return self.item(0, col - (col - 2) % 3).text()
