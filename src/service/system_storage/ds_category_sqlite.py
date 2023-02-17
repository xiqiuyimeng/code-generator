# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from enum import Enum

from src.constant.constant import SQL_DS_CATEGORY, STRUCT_DS_CATEGORY
from src.service.system_storage.sqlite_abc import SqliteBasic, BasicSqliteDTO, transactional, get_db_conn

_author_ = 'luwt'
_date_ = '2022/9/15 17:43'

table_name = 'ds_category'

ds_category_sql_dict = {
    'create': f'''create table if not exists {table_name}
    (id integer PRIMARY KEY autoincrement,
    name char(10) not null,
    item_order integer not null,
    is_current integer not null,
    create_time datetime,
    update_time datetime
    );''',
    'drop': f'drop table {table_name}'
}


@dataclass
class DsCategory(BasicSqliteDTO):
    name: str = field(default=None, init=False)
    is_current: int = field(default=None, init=False)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


sql_ds_category_dict = {
    'name': SQL_DS_CATEGORY,
    'item_order': 1,
    'is_current': 1
}
struct_ds_category_dict = {
    'name': STRUCT_DS_CATEGORY,
    'item_order': 2,
    'is_current': 0
}


class DsCategoryEnum(Enum):
    sql_ds_category = DsCategory(**sql_ds_category_dict)
    struct_ds_category = DsCategory(**struct_ds_category_dict)


class DsCategorySqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, ds_category_sql_dict)

    @staticmethod
    def drop_table():
        get_db_conn().query(ds_category_sql_dict.get('drop'))

    @transactional
    def switch_ds_category(self, target_ds_category):
        ds_categories = self.select(DsCategory())
        update_ds_categories = list()
        for ds_category in ds_categories:
            update_ds_category = DsCategory()
            update_ds_category.id = ds_category.id
            if ds_category.name == target_ds_category:
                update_ds_category.is_current = 1
            else:
                update_ds_category.is_current = 0
            update_ds_categories.append(update_ds_category)
        self.batch_update(update_ds_categories)
