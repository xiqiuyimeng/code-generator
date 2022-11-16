# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from enum import Enum

from service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic

_author_ = 'luwt'
_date_ = '2022/11/11 16:49'

table_name = 'struct_content'

struct_content_sql_dict = {
    'create': f'''create table  if not exists {table_name}
    (id integer primary key autoincrement,
    storage_type integer not null,
    content text,
    file_url text,
    create_time datetime,
    update_time datetime
    );''',
}


class StorageTypeEnum(Enum):

    text = 0
    file = 1


@dataclass
class StructContent(BasicSqliteDTO):

    # 存储类型
    storage_type: int = field(init=False, default=None)
    # 具体结构体内容，文本信息
    content: str = field(init=False, default=None)
    # 结构体文件地址
    file_url: str = field(init=False, default=None)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class StructContentSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, struct_content_sql_dict)
