# -*- coding: utf-8 -*-
import pymysql

from src.service.sql_ds_executor.db_executor import SqlDBExecutor
from src.service.system_storage.ds_table_col_info_sqlite import DsTableColInfo, CheckedEnum, ColTypeEnum

_author_ = 'luwt'
_date_ = '2022/10/1 12:52'


class MySqlDBExecutor(SqlDBExecutor):

    def connect_db(self):
        conn = pymysql.connect(host=self.conn_info.host,
                               port=self.conn_info.port,
                               user=self.conn_info.user,
                               passwd=self.conn_info.pwd,
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
        self.cursor = conn.cursor()

    def parse_db_name(self, row) -> str:
        return tuple(row.values())[0]

    def parse_tb_name(self, row) -> str:
        return tuple(row.values())[0]

    def parse_col_data(self, row) -> DsTableColInfo:
        table_info = DsTableColInfo()
        table_info.col_name = row.get('Field')
        table_info.full_data_type = row.get('Type')
        table_info.is_pk = row.get('Key') == 'PRI'
        table_info.col_comment = row.get('Comment')
        table_info.checked = CheckedEnum.unchecked.value
        table_info.handle_data_type()
        table_info.col_type = ColTypeEnum.col.value
        return table_info
