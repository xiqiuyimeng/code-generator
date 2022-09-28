# -*- coding: utf-8 -*-
import json
from dataclasses import dataclass
from enum import Enum

_author_ = 'luwt'
_date_ = '2022/9/27 17:59'


def mapping_conn_type(sql_conn):
    for conn_type in ConnTypeEnum:
        if conn_type.value.type == sql_conn.conn_type:
            # 根据匹配到的类型，映射为具体的对象
            result = globals()[conn_type.value.type_class](**json.loads(sql_conn.conn_info))
            sql_conn.conn_info_obj = result


def get_conn_dialog(display_name):
    for conn_type in ConnTypeEnum:
        if conn_type.value.display_name == display_name:
            return conn_type.value.type_dialog


@dataclass
class ConnType:

    type: int
    display_name: str
    # 对应类型承载实际连接信息的实体类
    type_class: str
    # 对应类型的菜单icon
    type_menu_icon: str
    # 对应类型的连接对话框
    type_dialog: str


class ConnTypeEnum(Enum):

    sqlite = ConnType(0, 'sqlite', 'SqliteConn', ':/icon/add.png', 'SqliteConnDialog')
    mysql = ConnType(1, 'mysql', 'MysqlConn', ':/icon/add.png', 'MysqlConnDialog')


@dataclass
class SqliteConn:

    file_url: str


@dataclass
class MysqlConn:

    host: str
    port: int
    user: str
    pwd: str

