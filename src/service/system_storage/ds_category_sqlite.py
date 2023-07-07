# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from src.service.system_storage.sqlite_abc import SqliteBasic, BasicSqliteDTO
from src.service.util.dataclass_util import init
from src.service.util.system_storage_util import get_cursor, transactional

_author_ = 'luwt'
_date_ = '2022/9/15 17:43'

table_name = 'ds_category'

sql_dict = {
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


@init
@dataclass
class DsCategory(BasicSqliteDTO):
    name: str = field(default=None, init=False)
    is_current: int = field(default=None, init=False)


class DsCategorySqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict, DsCategory)

    @staticmethod
    def drop_table():
        get_cursor().execute(sql_dict.get('drop'))

    @transactional
    def switch_ds_category(self, target_ds_category):
        ds_categories = self.select_by_order()
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
