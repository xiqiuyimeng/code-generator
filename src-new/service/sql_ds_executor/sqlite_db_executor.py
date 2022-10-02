# -*- coding: utf-8 -*-
import records
from sqlalchemy.pool import SingletonThreadPool

from service.sql_ds_executor.db_executor import SqlDBExecutor
from service.system_storage.conn_type import get_conn_type_by_type

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

    def open_tb(self, db, tb): ...
