# -*- coding: utf-8 -*-
import sqlite3

from src.service.sql_ds_executor.db_executor import SqlDBExecutor
from src.service.system_storage.ds_table_col_info_sqlite import DsTableColInfo, CheckedEnum, ColTypeEnum

_author_ = 'luwt'
_date_ = '2022/10/1 12:52'


class SqliteDBExecutor(SqlDBExecutor):

    def connect_db(self):
        conn = sqlite3.connect(self.conn_info.file_url, check_same_thread=False)
        # 查询结果可以以字典形式展现
        conn.row_factory = sqlite3.Row
        self.cursor = conn.cursor()

    def parse_db_name(self, row) -> str:
        return dict(row).get('name')

    def parse_tb_name(self, row) -> str:
        return dict(row).get('tbl_name')

    def parse_col_data(self, row) -> DsTableColInfo:
        row_data = dict(row)
        table_info = DsTableColInfo()
        table_info.col_name = row_data.get('name')
        table_info.full_data_type = row_data.get('type')
        table_info.is_pk = row_data.get('pk')
        table_info.checked = CheckedEnum.unchecked.value
        # sqlite 没有注释
        table_info.col_comment = ''
        table_info.handle_data_type()
        table_info.col_type = ColTypeEnum.col.value
        return table_info
