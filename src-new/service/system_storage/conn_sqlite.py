# -*- coding: utf-8 -*-
import dataclasses
import json
from dataclasses import dataclass, field

from service.system_storage.conn_type import mapping_conn_type
from service.system_storage.sqlite_abc import SqliteBasic, BasicSqliteDTO

_author_ = 'luwt'
_date_ = '2022/5/11 10:26'

table_name = 'sql_connection'

conn_sql_dict = {
    'create': f'''create table  if not exists {table_name}
    (id integer primary key autoincrement,
    conn_name char(50) not null,
    conn_type char(30) not null,
    conn_info text,
    item_order integer not null,
    create_time datetime,
    update_time datetime
    );''',
}


@dataclass
class SqlConnection(BasicSqliteDTO):

    conn_name: str = field(init=False, default=None)
    conn_type: str = field(init=False, default=None)
    # json串，存储连接信息
    conn_info: str = field(init=False, default=None)
    # 根据 conn_info 映射的实体类
    conn_info_type: dataclass = field(init=False, default=None)
    item_order: int = field(init=False, default=None)

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
        super().__init__(table_name, conn_sql_dict)

    def check_name_available(self, sql_conn):
        """检查连接名称是否可用，名称必须唯一"""
        result = self.select_count(sql_conn)
        return result == 0

    def add_conn(self, sql_conn: SqlConnection):
        sql_conn.item_order = self.get_max_order()
        self.insert(sql_conn)
