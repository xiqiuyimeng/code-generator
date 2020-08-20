# -*- coding: utf-8 -*-
"""
对数据库游标对象的一个代理类，暴露给其他服务进行调用，处理数据库相关操作
"""
from itertools import groupby

from src.constant.constant import QUERY_DB_SQL, QUERY_TABLES_SQL, QUERY_SYS_TB, QUERY_SYS_TB_COL
from src.db.get_cursor import Cursor

_author_ = 'luwt'
_date_ = '2020/6/11 10:20'


class DBExecutor:
    """数据库操作类"""

    def __init__(self, host, port, user, pwd):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.port = port
        self.get_cursor()
        self.cursor = self.cursor_.cursor

    def __enter__(self):
        return self

    def get_cursor(self):
        """获取游标"""
        self.cursor_ = Cursor(self.host, self.user, self.pwd, None, self.port)

    def test_conn(self):
        self.cursor_.conn.ping()

    def switch_db(self, db):
        """切换库"""
        self.cursor.execute(f'use {db};')

    def get_data(self, sql):
        """执行sql，获取数据，返回列表格式"""
        self.cursor.execute(sql)
        return list(self.cursor.fetchall())

    def get_dbs_tables(self, sql):
        """取二维数组的第一列"""
        return list(map(lambda x: x[0], self.get_data(sql)))

    def get_dbs(self):
        """获取链接下所有数据库名列表"""
        return self.get_dbs_tables(QUERY_DB_SQL)

    def get_tables(self):
        """获取数据库中所有表名列表"""
        return self.get_dbs_tables(QUERY_TABLES_SQL)

    def get_cols(self, db, table):
        """从系统表查询表的所有字段名列表"""
        sql = f'{QUERY_SYS_TB} where table_schema = "{db}" and table_name = "{table}"'
        return list(map(lambda x: (x[0], x[1], x[3]), self.get_data(sql)))

    def get_tb_cols(self, db, table=None):
        """从系统表中查询指定数据库下的所有字段，也可指定表名"""
        sql = f'{QUERY_SYS_TB_COL} where table_schema = "{db}"'
        if table:
            sql += f' and table_name in ("{",".join(table)}")'
        return self.get_data(sql)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor_.__exit__(exc_type, exc_val, exc_tb)

    def exit(self):
        """关闭游标和链接"""
        self.__exit__(None, None, None)


def get_cols_group_by_table(cols):
    """
    将 get_tb_cols 方法查询出的结果进行分组，按表名分组，得到字典
        tb: (col_A, col_B)
    :param cols: 数据库中查询出的数据
    """
    res = dict()
    cols.sort(key=lambda x: x[1])
    result = groupby(cols, lambda x: x[1])
    for key, group in result:
        cols = tuple(map(lambda x: x[0], list(group)))
        res[key] = cols
    return res
