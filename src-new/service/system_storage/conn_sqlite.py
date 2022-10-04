# -*- coding: utf-8 -*-
import dataclasses
import json
from dataclasses import dataclass, field

from service.system_storage.conn_type import mapping_conn_type
from service.system_storage.sqlite_abc import SqliteBasic, BasicSqliteDTO

_author_ = 'luwt'
_date_ = '2022/5/11 10:26'


conn_sql = {
    'create': '''create table  if not exists sql_connection
    (id integer primary key autoincrement,
    conn_name char(50) not null,
    conn_type integer not null,
    conn_info text,
    create_time datetime,
    update_time datetime
    );''',
}


@dataclass
class SqlConnection(BasicSqliteDTO):

    conn_name: str = field(init=False, default=None)
    conn_type: int = field(init=False, default=None)
    # json串，存储连接信息
    conn_info: str = field(init=False, default=None)
    # 根据 conn_info 映射的实体类
    conn_info_type: dataclass = field(init=False, default=None)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        # 映射连接类型实体
        if self.conn_info:
            mapping_conn_type(self)

    def construct_conn_info(self):
        """根据conn_info_type实体构造conn_info"""
        self.conn_info = json.dumps(dataclasses.asdict(self.conn_info_type), ensure_ascii=False)


class ConnSqlite(SqliteBasic):

    def __init__(self):
        super().__init__('sql_connection', conn_sql.get('create'))

    def check_name_available(self, sql_conn):
        """检查连接名称是否可用，名称必须唯一"""
        result = self.select_count(sql_conn)
        return result == 0
