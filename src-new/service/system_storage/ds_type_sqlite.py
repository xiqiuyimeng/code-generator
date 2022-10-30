# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from enum import Enum

from constant.constant import SQL_DATASOURCE_TYPE, STRUCTURE_DATASOURCE_TYPE
from service.system_storage.sqlite_abc import SqliteBasic, BasicSqliteDTO, transactional, get_db_conn

_author_ = 'luwt'
_date_ = '2022/9/15 17:43'

table_name = 'datasource_type'

datasource_type_sql_dict = {
    'create': f'''create table if not exists {table_name}
    (id integer PRIMARY KEY autoincrement,
    name char(10) not null,
    ds_type_order integer not null,
    is_current integer not null,
    create_time datetime,
    update_time datetime
    );''',
    'drop': f'drop table {table_name}'
}


@dataclass
class DatasourceType(BasicSqliteDTO):

    name: str = field(default=None, init=False)
    ds_type_order: int = field(default=None, init=False)
    is_current: int = field(default=None, init=False)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


sql_ds_dict = {
    'name': SQL_DATASOURCE_TYPE,
    'ds_type_order': 1,
    'is_current': 1
}
structure_ds_dict = {
    'name': STRUCTURE_DATASOURCE_TYPE,
    'ds_type_order': 2,
    'is_current': 0
}


class DatasourceTypeEnum(Enum):
    sql_ds_type = DatasourceType(**sql_ds_dict)
    structure_ds_type = DatasourceType(**structure_ds_dict)


class DatasourceTypeSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, datasource_type_sql_dict)

    @staticmethod
    def drop_table():
        get_db_conn().query(datasource_type_sql_dict.get('drop'))

    @transactional
    def switch_ds_type(self, ds_type_name):
        datasource_types = self.select(DatasourceType())
        update_ds_types = list()
        for ds_type in datasource_types:
            update_ds_type = DatasourceType()
            update_ds_type.id = ds_type.id
            if ds_type.name == ds_type_name:
                update_ds_type.is_current = 1
            else:
                update_ds_type.is_current = 0
            update_ds_types.append(update_ds_type)
        self.batch_update(update_ds_types)

