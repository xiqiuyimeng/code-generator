# -*- coding: utf-8 -*-
import dataclasses
import json
from dataclasses import dataclass, field

from src.service.system_storage.conn_type import mapping_conn_type
from src.service.system_storage.opened_tree_item_sqlite import OpenedTreeItemSqlite
from src.service.system_storage.sqlite_abc import SqliteBasic, BasicSqliteDTO
from src.service.util.dataclass_util import init

_author_ = 'luwt'
_date_ = '2022/5/11 10:26'

table_name = 'sql_connection'

sql_dict = {
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


@init
@dataclass
class SqlConnection(BasicSqliteDTO):
    conn_name: str = field(init=False, default=None)
    conn_type: str = field(init=False, default=None)
    # json串，存储连接信息
    conn_info: str = field(init=False, default=None)
    # 根据 conn_info 映射的实体类
    conn_info_type: dataclass = field(init=False, default=None)

    def construct_conn_info(self):
        """根据conn_info_type实体构造conn_info"""
        self.conn_info = json.dumps(dataclasses.asdict(self.conn_info_type), ensure_ascii=False)


class ConnSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict)

    def get_conn_id_types(self):
        rows = self._do_select(sql_dict.get('select_id_type'), SqlConnection())
        return [SqlConnection(**row) for row in rows.as_dict()]

    def get_conn_by_id(self, conn_id):
        conn_param = SqlConnection()
        conn_param.id = conn_id
        conn = self.select_one(conn_param)
        if conn.conn_info:
            mapping_conn_type(conn)
        return conn
