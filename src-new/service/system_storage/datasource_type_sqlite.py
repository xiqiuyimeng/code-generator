# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from enum import Enum

from service.system_storage.sqlite_abc import SqliteBasic, BasicSqliteDTO

_author_ = 'luwt'
_date_ = '2022/9/15 17:43'

datasource_type_sql = {
    'create': '''create table if not exists datasource_type
    (id integer PRIMARY KEY autoincrement,
    name char(10) not null,
    ds_type_order integer not null,
    icon_path char(100) not null,
    is_current integer not null,
    create_time datetime,
    update_time datetime
    );''',
    'drop': 'drop table datasource_type'
}


@dataclass
class DatasourceType(BasicSqliteDTO):

    name: str = field(default=None, init=False)
    ds_type_order: int = field(default=None, init=False)
    icon_path: str = field(default=None, init=False)
    is_current: int = field(default=None, init=False)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


sql_ds_dict = {
    'name': 'sql数据源',
    'ds_type_order': 1,
    'icon_path': ':/icon/add.png',
    'is_current': 1
}
structure_ds_dict = {
    'name': 'structure数据源',
    'ds_type_order': 2,
    'icon_path': ':/icon/add.png',
    'is_current': 0
}


class DatasourceTypeEnum(Enum):
    sql_ds_type = DatasourceType(**sql_ds_dict)
    structure_ds_type = DatasourceType(**structure_ds_dict)


class DatasourceTypeSqlite(SqliteBasic):

    def __init__(self):
        super().__init__('datasource_type', datasource_type_sql.get('create'))

    def drop_table(self):
        self.db.query(datasource_type_sql.get('drop'))

    def switch_ds_type(self, ds_type_name):
        datasource_types = self.select(DatasourceType())
        for ds_type in datasource_types:
            if ds_type.name == ds_type_name:
                ds_type.is_current = 1
            else:
                ds_type.is_current = 0
        self.batch_update(datasource_types)

