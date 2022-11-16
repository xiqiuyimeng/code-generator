# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic

_author_ = 'luwt'
_date_ = '2022/11/11 16:49'

table_name = 'struct_info'

struct_sql_dict = {
    'create': f'''create table  if not exists {table_name}
    (id integer primary key autoincrement,
    opened_item_id integer not null,
    struct_name char(50) not null,
    struct_type char(30) not null,
    content_id integer,
    item_order integer not null,
    create_time datetime,
    update_time datetime
    );''',
}


@dataclass
class StructInfo(BasicSqliteDTO):

    opened_item_id: str = field(init=False, default=None, compare=False)
    struct_name: str = field(init=False, default=None)
    struct_type: str = field(init=False, default=None, compare=False)
    # 结构体具体内容id
    content_id: str = field(init=False, default=None, compare=False)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class StructSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, struct_sql_dict)
