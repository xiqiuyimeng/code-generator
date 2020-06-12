# -*- coding: utf-8 -*-
import constant
from get_cursor import Cursor
import global_var as gv
_author_ = 'luwt'
_date_ = '2020/6/11 10:20'

conn_info = 'centos121', 'root', 'admin'


class DBExecutor:
    """数据库操作类"""

    def __init__(self, host, user, pwd):
        self.host = host
        self.user = user
        self.pwd = pwd
        self._cursor = None
        self.cursor = self.get_cursor()

    def get_cursor(self):
        self._cursor = Cursor(self.host, self.user, self.pwd, None)
        gv.cursor = self._cursor.cursor
        return gv.cursor

    def switch_db(self, db):
        self.cursor.execute(f'use {db};')

    def get_data(self, sql):
        self.cursor.execute(sql)
        return list(self.cursor.fetchall())

    def get_dbs_tables(self, sql):
        return list(map(lambda x: x[0], self.get_data(sql)))

    def get_dbs(self):
        return self.get_dbs_tables(constant.QUERY_DB_SQL)

    def get_tables(self):
        return self.get_dbs_tables(constant.QUERY_TABLES_SQL)

    def get_cols(self, table):
        sql = f'{constant.QUERY_SYS_TB} where table_name = "{table}"'
        return self.get_data(sql)

    def exit(self):
        self._cursor.__exit__(None, None, None)


executor = DBExecutor(*conn_info)
dbs = executor.get_dbs()
print(dbs)
executor.switch_db('test')
tables = executor.get_tables()
print(tables)
cols = executor.get_cols('notice')
print(cols)
executor.exit()
