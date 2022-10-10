# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from enum import Enum
from typing import List

from service.system_storage.ds_table_info_sqlite import DsTableInfo
from service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic

_author_ = 'luwt'
_date_ = '2022/10/8 12:30'

table_name = 'ds_table_tab'

ds_table_tab_sql_dict = {
    'create': f'''create table if not exists {table_name}
    (id integer PRIMARY KEY autoincrement,
    parent_opened_id integer not null,
    tab_order integer not null,
    is_current integer not null,
    ds_type_name char(10) not null,
    create_time datetime,
    update_time datetime
    );''',
    'max_order_sql': f'select ifnull(max(id), 0) as max_order from {table_name}'
}


@dataclass
class DsTableTab(BasicSqliteDTO):

    # 父id，指向opened_tree_item表
    parent_opened_id: int = field(init=False, default=None)
    # tab 顺序
    tab_order: str = field(init=False, default=None)
    # 标识tab是否应该置为当前项
    is_current: int = field(init=False, default=None)
    # 数据源类型
    ds_type_name: str = field(init=False, default=None)
    # col_list
    col_list: List[DsTableInfo] = field(init=False, default=None)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class CurrentEnum(Enum):

    is_current = 1
    not_current = 0


class DsTableTabSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, ds_table_tab_sql_dict)

    def add_tab(self, opened_table_item):
        self.change_other_not_current(opened_table_item.ds_type_name)

        table_tab = DsTableTab()
        table_tab.parent_opened_id = opened_table_item.id
        table_tab.tab_order = self.get_max_order()
        table_tab.is_current = CurrentEnum.is_current.value
        table_tab.ds_type_name = opened_table_item.ds_type_name
        self.insert(table_tab)
        return table_tab

    def get_max_order(self):
        db_record = self.db.query(ds_table_tab_sql_dict.get('max_order_sql'))
        return db_record.first().max_order

    def change_current(self, current_tab: DsTableTab):
        # 将同一数据源下的其他项全部置为非当前，将当前值置为当前项
        self.change_other_not_current(current_tab.ds_type_name)
        current_tab.is_current = CurrentEnum.is_current.value
        self.update(current_tab)

    def change_other_not_current(self, ds_type_name):
        # 将同一数据源下的其他项全部置为非当前
        table_tab = DsTableTab()
        table_tab.is_current = CurrentEnum.is_current.value
        table_tab.ds_type_name = ds_type_name
        current_tabs = self.select(table_tab)
        # 当前项应该不多于1个
        if current_tabs:
            origin_current_tab = DsTableTab()
            origin_current_tab.is_current = CurrentEnum.not_current.value
            origin_current_tab.id = current_tabs[0].id
            self.update(origin_current_tab)
