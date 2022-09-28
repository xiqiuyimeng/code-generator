# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from service.system_storage.sqlite_abc import SqliteBasic, BasicSqliteDTO

_author_ = 'luwt'
_date_ = '2022/9/15 17:43'

datasource_type_sql = {
    'create': '''create table if not exists datasource_type
    (id integer PRIMARY KEY autoincrement,
    name char(10) not null,
    datasource_type_order integer not null,
    is_current integer not null,
    create_time datetime,
    update_time datetime
    );''',
    'drop': 'drop table datasource_type'
}


@dataclass
class DatasourceType(BasicSqliteDTO):

    name: str = field(default=None, init=False)
    datasource_type_order: int = field(default=None, init=False)
    is_current: int = field(default=None, init=False)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class DatasourceTypeSqlite(SqliteBasic):

    def __init__(self):
        super().__init__('datasource_type', datasource_type_sql.get('create'))

    def drop_table(self):
        self.db.query(datasource_type_sql.get('drop'))

