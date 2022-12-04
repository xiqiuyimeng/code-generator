# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic
from service.system_storage.struct_type import mapping_struct_type

_author_ = 'luwt'
_date_ = '2022/11/11 16:49'

table_name = 'struct_info'

struct_sql_dict = {
    'create': f'''create table  if not exists {table_name}
    (id integer primary key autoincrement,
    opened_item_id integer not null,
    struct_name char(50) not null,
    struct_type char(30) not null,
    content text,
    file_url text,
    create_time datetime,
    update_time datetime
    );''',
}


@dataclass
class StructInfo(BasicSqliteDTO):

    opened_item_id: str = field(init=False, default=None)
    struct_name: str = field(init=False, default=None)
    struct_type: str = field(init=False, default=None)
    # 具体结构体内容，文本信息
    content: str = field(init=False, default=None)
    # 结构体文件地址
    file_url: str = field(init=False, default=None)
    # 根据struct type映射为 StructType
    struct_type_info: dataclass = field(init=False, default=None, compare=False)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        mapping_struct_type(self)


class StructSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, struct_sql_dict)
