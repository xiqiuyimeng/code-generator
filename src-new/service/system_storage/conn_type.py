# -*- coding: utf-8 -*-
import json
from dataclasses import dataclass
from enum import Enum

from constant.constant import SQLITE_DISPLAY_NAME, MYSQL_DISPLAY_NAME, SQLITE_DB, SQLITE_TB, MYSQL_DB, MYSQL_TB

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


@dataclass
class ConnType:

    type: int
    # 展示名称，也用来标识icon类型
    display_name: str
    db_icon_name: str
    tb_icon_name: str
    # 对应类型承载实际连接信息的实体类
    type_class: str
    # 对应类型的连接对话框
    type_dialog: str


class ConnTypeEnum(Enum):

    sqlite = ConnType(0, SQLITE_DISPLAY_NAME, SQLITE_DB, SQLITE_TB, 'SqliteConn', 'SqliteConnDialog')
    mysql = ConnType(1, MYSQL_DISPLAY_NAME, MYSQL_DB, MYSQL_TB, 'InternetSqlConn', 'MysqlConnDialog')


@dataclass
class SqliteConn:

    file_url: str


@dataclass
class InternetSqlConn:

    host: str
    port: int
    user: str
    pwd: str

