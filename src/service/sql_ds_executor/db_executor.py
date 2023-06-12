# -*- coding: utf-8 -*-

from src.service.system_storage.conn_sqlite import SqlConnection
from src.service.system_storage.conn_type import get_conn_type_by_type
from src.service.system_storage.ds_table_col_info_sqlite import DsTableColInfo

_author_ = 'luwt'
_date_ = '2022/5/30 21:59'


class SqlDBExecutor:

    def __init__(self, connection: SqlConnection):
        self.sql_conn = connection
        self.conn_info = connection.conn_info_type
        self.cursor = ...

    def connect_db(self):
        ...

    def get_data(self, sql):
        if self.cursor is Ellipsis:
            self.connect_db()
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def test_conn(self):
        self.connect_db()

    def open_conn(self):
        query_db_sql = get_conn_type_by_type(self.sql_conn.conn_type).query_db_sql
        return [self.parse_db_name(row) for row in self.get_data(query_db_sql)]

    def parse_db_name(self, row) -> str:
        ...

    def open_db(self, db, check=True):
        if check:
            self.check_db(db)
        query_tb_sql = get_conn_type_by_type(self.sql_conn.conn_type).query_tb_sql.format(db)
        return [self.parse_tb_name(row) for row in self.get_data(query_tb_sql)]

    def check_db(self, db):
        check_db_sql = get_conn_type_by_type(self.sql_conn.conn_type).check_db_sql.format(db)
        db_records = self.get_data(check_db_sql)
        if not db_records:
            raise Exception(f'{db}库不存在')

    def parse_tb_name(self, row) -> str:
        ...

    def open_tb(self, db, tb, check=True):
        if check:
            self.check_tb(db, tb)
        query_col_sql = get_conn_type_by_type(self.sql_conn.conn_type).query_col_sql.format(db, tb)
        return [self.parse_col_data(row) for row in self.get_data(query_col_sql)]

    def check_tb(self, db, tb):
        self.check_db(db)
        check_tb_sql = get_conn_type_by_type(self.sql_conn.conn_type).check_tb_sql.format(db, tb)
        db_records = self.get_data(check_tb_sql.format(db, tb))
        if not db_records:
            raise Exception(f'{tb}表不存在')

    def parse_col_data(self, row) -> DsTableColInfo:
        ...
