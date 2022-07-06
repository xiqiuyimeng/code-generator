# -*- coding: utf-8 -*-
from service.db_operator.get_cursor import Cursor
from constant.constant import QUERY_DB_SQL, QUERY_TABLES_SQL, QUERY_COLUMNS_SQL

_author_ = 'luwt'
_date_ = '2022/5/30 21:59'


class DBExecutor:

    def __init__(self, conn_name, host, port, user, pwd):
        self.cursor_ = Cursor(conn_name, host, user, pwd, port)
        self.cursor = self.cursor_.cursor

    def __enter__(self):
        return self

    def test_conn(self):
        """测试连接"""
        self.cursor_.conn.ping()

    def get_data(self, sql):
        """执行sql，获取数据"""
        self.cursor.execute(sql)
        return tuple(self.cursor.fetchall())

    def switch_db(self, db):
        """切换库"""
        self.cursor.execute(f'use {db};')

    def open_conn(self):
        """获取连接下所有数据库名称"""
        return tuple(map(lambda x: x[0], self.get_data(QUERY_DB_SQL)))

    def open_db(self, db):
        """获取指定库下所有表名"""
        self.switch_db(db)
        return tuple(map(lambda x: x[0], self.get_data(QUERY_TABLES_SQL)))

    def open_tb(self, db, tb):
        self.switch_db(db)
        # 取出field、type、comment
        return tuple(map(lambda x: (x[0], x[1], x[8]), self.get_data(QUERY_COLUMNS_SQL.format(tb))))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor_.__exit__(exc_type, exc_val, exc_tb)
