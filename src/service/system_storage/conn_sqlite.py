# -*- coding: utf-8 -*-
import dataclasses
import json
from dataclasses import dataclass, field

from src.service.system_storage.conn_type import mapping_conn_type
from src.service.system_storage.opened_tree_item_sqlite import OpenedTreeItemSqlite
from src.service.system_storage.sqlite_abc import SqliteBasic, BasicSqliteDTO

_author_ = 'luwt'
_date_ = '2022/5/11 10:26'

table_name = 'sql_connection'

conn_sql_dict = {
    'create': f'''create table if not exists {table_name}
    (id integer primary key autoincrement,
    conn_name char(50) not null,
    conn_type char(30) not null,
    conn_info text,
    create_time datetime,
    update_time datetime
    );''',
    'select_id_type': f'select conn.id, conn.conn_type '
                      f'from {table_name} conn, {OpenedTreeItemSqlite().table_name} opened_item '
                      f'where conn.id = opened_item.parent_id and opened_item.level = 0 '
                      f'order by opened_item.item_order',
}


@dataclass
class SqlConnection(BasicSqliteDTO):

    conn_name: str = field(init=False, default=None)
    conn_type: str = field(init=False, default=None)
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
        super().__init__(table_name, conn_sql_dict)

    def get_conn_id_types(self):
        rows = self._do_select(conn_sql_dict.get('select_id_type'), SqlConnection())
        return list(map(lambda x: SqlConnection(**x), rows.as_dict()))

    def check_name_available(self, sql_conn):
        """检查连接名称是否可用，名称必须唯一"""
        result = self.select_count(sql_conn)
        return result == 0
