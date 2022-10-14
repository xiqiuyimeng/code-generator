# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from enum import Enum
from typing import List

from service.system_storage.ds_table_info_sqlite import DsTableInfo
from service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic
from logger.log import logger as log

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
    'max_order_sql': f'select ifnull(max(tab_order), 0) as max_order from {table_name}'
                     f' where ds_type_name = :ds_type_name',
    'move_order_forward': f'update {table_name} set tab_order = tab_order - 1 '
                          f'where tab_order > :tab_order and ds_type_name = :ds_type_name',
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

    def set_current(self):
        self.is_current = CurrentEnum.is_current.value

    def set_not_current(self):
        self.is_current = CurrentEnum.not_current.value


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
        table_tab.tab_order = self.get_max_order(table_tab.ds_type_name)
        table_tab.ds_type_name = opened_table_item.ds_type_name
        table_tab.set_current()
        self.insert(table_tab)
        return table_tab

    def get_max_order(self, ds_type_name):
        max_order_sql = ds_table_tab_sql_dict.get('max_order_sql')
        db_record = self.db.query(max_order_sql, **{'ds_type_name': ds_type_name})
        log.info(f"查询当前数据源最大order值语句 ==> {max_order_sql}")
        log.info(f"查询当前数据源最大order值参数 ==> {ds_type_name}")
        return db_record.first().max_order + 1

    def change_current(self, current_tab: DsTableTab):
        # 将同一数据源下的其他项全部置为非当前，将当前值置为当前项
        self.change_other_not_current(current_tab.ds_type_name)
        current_tab.set_current()
        self.update(current_tab)

    def change_other_not_current(self, ds_type_name):
        # 将同一数据源下的其他项全部置为非当前
        table_tab = DsTableTab()
        table_tab.set_current()
        table_tab.ds_type_name = ds_type_name
        current_tabs = self.select(table_tab)
        # 当前项应该不多于1个
        if current_tabs:
            origin_current_tab = DsTableTab()
            origin_current_tab.set_not_current()
            origin_current_tab.id = current_tabs[0].id
            self.update(origin_current_tab)

    def remove_tab(self, tab):
        self.delete(tab.id)
        # 调整order，找出排序在删除项之后的，向前整体移动一位
        move_order_forward_sql = ds_table_tab_sql_dict.get('move_order_forward')
        param = {
            'tab_order': tab.tab_order,
            'ds_type_name': tab.ds_type_name
        }
        self.db.query(move_order_forward_sql, **param)
        log.info(f'将tab_table顺序前移语句 ==> {move_order_forward_sql}')
        log.info(f'将tab_table顺序前移参数 ==> {param}')
