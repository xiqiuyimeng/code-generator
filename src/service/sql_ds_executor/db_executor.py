# -*- coding: utf-8 -*-

from src.service.system_storage.conn_sqlite import SqlConnection
from src.enum.conn_type_enum import get_conn_type_by_type
from src.service.system_storage.ds_table_col_info_sqlite import DsTableColInfo

_author_ = 'luwt'
_date_ = '2022/5/30 21:59'


class SqlDBExecutor:

    def __init__(self, connection: SqlConnection):
        self.conn_type = get_conn_type_by_type(connection.conn_type)
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
        query_db_sql = self.conn_type.query_db_sql
        return [self.parse_db_name(row) for row in self.get_data(query_db_sql)]

    def parse_db_name(self, row) -> str:
        ...

    def open_db(self, db, check=True):
        if check:
            self.check_db(db)
        query_tb_sql = self.conn_type.query_tb_sql.format(db)
        return [self.parse_tb_name(row) for row in self.get_data(query_tb_sql)]

    def check_db(self, db):
        check_db_sql = self.conn_type.check_db_sql.format(db)
        db_records = self.get_data(check_db_sql)
        if not db_records:
            raise Exception(f'{db}库不存在')

    def parse_tb_name(self, row) -> str:
        ...

    def open_tb(self, db, tb, check=True):
        if check:
            self.check_tb(db, tb)
        query_col_sql = self.conn_type.query_col_sql.format(db, tb)
        return [self.parse_col_data(row) for row in self.get_data(query_col_sql)]

    def check_tb(self, db, tb):
        self.check_db(db)
        check_tb_sql = self.conn_type.check_tb_sql.format(db, tb)
        db_records = self.get_data(check_tb_sql)
        if not db_records:
            raise Exception(f'{tb}表不存在')

    def parse_col_data(self, row) -> DsTableColInfo:
        ...

    def get_table_comment(self, db, tb) -> str:
        table_comment_sql = self.conn_type.query_tb_comment_sql.format(db, tb)
        # 有些数据库不支持查询表注释，所以需要判断语句是否存在
        if table_comment_sql:
            db_records = self.get_data(table_comment_sql)
            if db_records:
                return self.parse_table_comment(db_records[0])

    def parse_table_comment(self, row) -> str:
        ...
