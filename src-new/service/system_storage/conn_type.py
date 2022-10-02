# -*- coding: utf-8 -*-
import json
from dataclasses import dataclass, field
from enum import Enum

from constant.constant import SQLITE_DISPLAY_NAME, MYSQL_DISPLAY_NAME, SQLITE_DB, SQLITE_TB, MYSQL_DB, MYSQL_TB, \
    MYSQL_QUERY_DB_SQL, MYSQL_QUERY_TB_SQL, MYSQL_QUERY_COL_SQL, SQLITE_QUERY_DB_SQL, SQLITE_QUERY_TB_SQL, \
    SQLITE_QUERY_COL_SQL

_author_ = 'luwt'
_date_ = '2022/9/27 17:59'


def mapping_conn_type(sql_conn):
    for conn_type in ConnTypeEnum:
        if conn_type.value.type == sql_conn.conn_type:
            # 根据匹配到的类型，映射为具体的对象
            result = globals()[conn_type.value.type_class](**json.loads(sql_conn.conn_info))
            sql_conn.conn_info_type = result


def get_conn_type(display_name):
    for conn_type in ConnTypeEnum:
        if conn_type.value.display_name == display_name:
            return conn_type.value
    return ConnTypeEnum.sqlite.value


def get_conn_type_by_type(sql_conn_type):
    for conn_type in ConnTypeEnum:
        if conn_type.value.type == sql_conn_type:
            return conn_type.value
    return ConnTypeEnum.sqlite.value


def get_conn_dialog(display_name):
    return get_conn_type(display_name).type_dialog


def get_conn_node(display_name):
    return get_conn_type(display_name).conn_node


def get_db_node(display_name):
    return get_conn_type(display_name).db_node


def get_tb_node(display_name):
    return get_conn_type(display_name).tb_node


@dataclass
class ConnType:

    type: int = field(init=False)
    # 展示名称，也用来标识icon类型
    display_name: str = field(init=False)
    db_icon_name: str = field(init=False)
    tb_icon_name: str = field(init=False)
    # 对应类型承载实际连接信息的实体类
    type_class: str = field(init=False)
    # 对应类型的连接对话框
    type_dialog: str = field(init=False)
    # 对应类型的数据库连接类
    db_executor: str = field(init=False)
    # 查询数据库列表sql
    query_db_sql: str = field(init=False)
    # 查询数据库表名列表sql
    query_tb_sql: str = field(init=False)
    # 查询数据库列sql
    query_col_sql: str = field(init=False)


class ConnTypeEnum(Enum):

    sqlite = ConnType()
    sqlite.type = 0
    sqlite.display_name = SQLITE_DISPLAY_NAME
    sqlite.db_icon_name = SQLITE_DB
    sqlite.tb_icon_name = SQLITE_TB
    sqlite.type_class = 'SqliteConn'
    sqlite.type_dialog = 'SqliteConnDialog'
    sqlite.db_executor = 'SqliteDBExecutor'
    sqlite.query_db_sql = SQLITE_QUERY_DB_SQL
    sqlite.query_tb_sql = SQLITE_QUERY_TB_SQL
    sqlite.query_col_sql = SQLITE_QUERY_COL_SQL

    mysql = ConnType()
    mysql.type = 1
    mysql.display_name = MYSQL_DISPLAY_NAME
    mysql.db_icon_name = MYSQL_DB
    mysql.tb_icon_name = MYSQL_TB
    mysql.type_class = 'InternetSqlConn'
    mysql.type_dialog = 'MysqlConnDialog'
    mysql.db_executor = 'MySqlDBExecutor'
    mysql.query_db_sql = MYSQL_QUERY_DB_SQL
    mysql.query_tb_sql = MYSQL_QUERY_TB_SQL
    mysql.query_col_sql = MYSQL_QUERY_COL_SQL


@dataclass
class SqliteConn:

    file_url: str


@dataclass
class InternetSqlConn:

    host: str
    port: int
    user: str
    pwd: str

