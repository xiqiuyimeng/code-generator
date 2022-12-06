# -*- coding: utf-8 -*-
import records
from sqlalchemy.pool import SingletonThreadPool

from service.sql_ds_executor.db_executor import SqlDBExecutor
from service.system_storage.conn_type import get_conn_type_by_type
from service.system_storage.ds_table_info_sqlite import DsTableInfo, CheckedEnum, ColTypeEnum

_author_ = 'luwt'
_date_ = '2022/10/1 12:52'


class SqliteDBExecutor(SqlDBExecutor):

    def __init__(self, *args):
        super().__init__(*args)

    def connect_db(self):
        self.db = records.Database(self.sql_url, poolclass=SingletonThreadPool,
                                   connect_args={'check_same_thread': False})

    def get_sql_connect_url(self):
        return f'sqlite:///{self.conn_info.file_url}'

    def open_conn(self):
        query_db_sql = get_conn_type_by_type(self.sql_conn.conn_type).query_db_sql
        db_records = self.get_data(query_db_sql)
        return tuple(map(lambda x: x.get('name'), db_records.as_dict(ordered=True)))

    def open_db(self, db):
        query_tb_sql = get_conn_type_by_type(self.sql_conn.conn_type).query_tb_sql
        db_records = self.get_data(query_tb_sql)
        return tuple(map(lambda x: x.get('tbl_name'), db_records.as_dict(ordered=True)))

    def open_tb(self, db, tb):
        query_col_sql = get_conn_type_by_type(self.sql_conn.conn_type).query_col_sql.format(tb)
        db_records = self.get_data(query_col_sql)
        return tuple(map(lambda x: self.convert_tb_data(x), db_records.as_dict(ordered=True)))

    def convert_tb_data(self, db_record):
        table_info = DsTableInfo()
        table_info.col_name = db_record.get('name')
        table_info.full_data_type = db_record.get('type')
        table_info.is_pk = db_record.get('pk')
        table_info.checked = CheckedEnum.unchecked.value
        table_info.col_comment = ''
        table_info.handle_data_type()
        table_info.col_type = ColTypeEnum.col.value
        return table_info
