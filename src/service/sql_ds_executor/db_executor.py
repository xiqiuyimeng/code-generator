# -*- coding: utf-8 -*-
import records

from exception.exception import BusinessException
from service.system_storage.conn_sqlite import SqlConnection
from service.system_storage.conn_type import get_conn_type_by_type

_author_ = 'luwt'
_date_ = '2022/5/30 21:59'


class SqlDBExecutor:

    def __init__(self, connection: SqlConnection):
        self.sql_conn = connection
        self.conn_info = connection.conn_info_type
        self.sql_url = self.get_sql_connect_url()
        self.db: records.Database = ...
        self.connect_db()

    def connect_db(self): ...

    def get_data(self, sql):
        return self.db.query(sql)

    def test_conn(self):
        self.db.get_connection()

    def open_conn(self): ...

    def open_db(self, db, check=True): ...

    def open_tb(self, db, tb, check=True): ...

    def get_sql_connect_url(self) -> str: ...


class InternetDBExecutor(SqlDBExecutor):

    def connect_db(self):
        self.db = records.Database(self.sql_url)

    def get_sql_connect_url(self) -> str:
        return f'{self.get_dialect_driver()}://{self.conn_info.user}:{self.conn_info.pwd}@' \
               f'{self.conn_info.host}:{self.conn_info.port}'

    def open_conn(self):
        query_db_sql = get_conn_type_by_type(self.sql_conn.conn_type).query_db_sql
        db_records = self.get_data(query_db_sql)
        return tuple(map(lambda x: map(lambda y: y, x.values()).__next__(), db_records.as_dict(ordered=True)))

    def open_db(self, db, check=True):
        if check:
            self.check_db(db)
        query_tb_sql = get_conn_type_by_type(self.sql_conn.conn_type).query_tb_sql.format(db)
        db_records = self.get_data(query_tb_sql)
        return tuple(map(lambda x: map(lambda y: y, x.values()).__next__(), db_records.as_dict(ordered=True)))

    def open_tb(self, db, tb, check=True):
        if check:
            self.check_tb(db, tb)
        query_col_sql = get_conn_type_by_type(self.sql_conn.conn_type).query_col_sql.format(db, tb)
        db_records = self.get_data(query_col_sql)
        return tuple(map(lambda x: self.convert_tb_data(x), db_records.as_dict(ordered=True)))

    def check_db(self, db):
        check_db_sql = self.get_check_db_sql()
        db_records = self.get_data(check_db_sql.format(db)).all()
        if not db_records:
            raise BusinessException(f'{db}库不存在')

    def check_tb(self, db, tb):
        self.check_db(db)
        check_tb_sql = self.get_check_tb_sql()
        db_records = self.get_data(check_tb_sql.format(db, tb)).all()
        if not db_records:
            raise BusinessException(f'{tb}表不存在')

    def get_dialect_driver(self) -> str: ...

    def get_check_db_sql(self) -> str: ...

    def get_check_tb_sql(self) -> str: ...

    def convert_tb_data(self, db_record): ...
