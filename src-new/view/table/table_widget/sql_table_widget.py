# -*- coding: utf-8 -*-

from service.async_func.async_tab_table_task import AsyncSaveTabObjExecutor
from service.system_storage.ds_table_col_info_sqlite import DsTableColInfo
from service.util.tree_node import TreeData
from view.table.table_widget.abstract_table_widget import AbstractTableWidget
from view.tree.tree_item.tree_item_func import get_item_opened_record

_author_ = 'luwt'
_date_ = '2022/5/10 15:25'


class SqlTableWidget(AbstractTableWidget):

    def get_async_save_executor(self) -> AsyncSaveTabObjExecutor:
        return self.main_window.sql_tab_widget.async_save_executor

    def get_tree_data(self) -> TreeData:
        return self.main_window.sql_tree_widget.tree_data

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
            self.setCellWidget(i, 0, self.make_checkbox_num_item(i, col))

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
        add_data = {
            0: get_item_opened_record(self.tree_item.parent().parent()),
            1: get_item_opened_record(self.tree_item.parent()),
            2: get_item_opened_record(self.tree_item),
            3: cols,
        }
        self.tree_data.add_node(add_data)

    def remove_checked_data(self, col):
        del_data = {
            0: get_item_opened_record(self.tree_item.parent().parent()).id,
            1: get_item_opened_record(self.tree_item.parent()).id,
            2: get_item_opened_record(self.tree_item).id,
            3: col.id,
        }
        self.tree_data.del_node(del_data)

    def remove_all_table_checked(self):
        del_data = {
            0: get_item_opened_record(self.tree_item.parent().parent()).id,
            1: get_item_opened_record(self.tree_item.parent()).id,
            2: get_item_opened_record(self.tree_item).id,
        }
        self.tree_data.del_node(del_data)

    def save_data(self, row, col, data):
        # 根据row找到对应的列信息数据
        col_data = self.cols[row]
        modify_col_data = DsTableColInfo()
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
