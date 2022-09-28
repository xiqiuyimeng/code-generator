# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from service.system_storage.sqlite_abc import SqliteBasic, BasicSqliteDTO

_author_ = 'luwt'
_date_ = '2022/9/15 17:43'

# 使用占位符的形式，避免特殊字符转义问题
frame_type_sql = {
    'create': '''create table if not exists frame_type
    (id integer PRIMARY KEY autoincrement,
    name char(10) not null,
    type integer not null,
    frame_order integer not null,
    is_current integer not null,
    create_time datetime,
    update_time datetime
    );''',
    'drop': 'drop table frame_type'
}


@dataclass
class FrameType(BasicSqliteDTO):

    name: str = field(default=None, init=False)
    type: int = field(default=None, init=False)
    frame_order: int = field(default=None, init=False)
    is_current: int = field(default=None, init=False)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class FrameTypeSqlite(SqliteBasic):

    def __init__(self):
        super().__init__('frame_type', frame_type_sql.get('create'))

    def drop_table(self):
        self.db.query(frame_type_sql.get('drop'))

