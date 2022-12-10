# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from enum import Enum
from typing import List

from service.system_storage.ds_table_col_info_sqlite import DsTableColInfo
from service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic, get_db_conn, transactional
from logger.log import logger as log

_author_ = 'luwt'
_date_ = '2022/10/8 12:30'

table_name = 'ds_table_tab'

ds_table_tab_sql_dict = {
    'create': f'''create table if not exists {table_name}
    (id integer PRIMARY KEY autoincrement,
    parent_opened_id integer not null,
    item_order integer not null,
    is_current integer not null,
    ds_type char(10) not null,
    create_time datetime,
    update_time datetime
    );''',
    'move_order_forward': f'update {table_name} set item_order = item_order - 1 '
                          f'where item_order > :item_order and ds_type = :ds_type',
}


@dataclass
class DsTableTab(BasicSqliteDTO):

    # 父id，指向opened_tree_item表
    parent_opened_id: int = field(init=False, default=None)
    # 标识tab是否应该置为当前项
    is_current: int = field(init=False, default=None)
    # 数据源类型
    ds_type: str = field(init=False, default=None)
    # col_list
    col_list: List[DsTableColInfo] = field(init=False, default=None)

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
        self.change_other_not_current(opened_table_item.ds_type)

        table_tab = DsTableTab()
        table_tab.parent_opened_id = opened_table_item.id
        table_tab.item_order = self.get_max_order({'ds_type': opened_table_item.ds_type})
        table_tab.ds_type = opened_table_item.ds_type
        table_tab.set_current()
        self.insert(table_tab)
        return table_tab

    @transactional
    def change_current(self, current_tab: DsTableTab):
        # 将同一数据源下的其他项全部置为非当前，将当前值置为当前项
        self.change_other_not_current(current_tab.ds_type)
        current_tab.set_current()
        self.update(current_tab)

    def change_other_not_current(self, ds_type):
        # 将同一数据源下的其他项全部置为非当前
        table_tab = DsTableTab()
        table_tab.set_current()
        table_tab.ds_type = ds_type
        current_tabs = self.select(table_tab)
        # 当前项应该不多于1个
        if current_tabs:
            origin_current_tab = DsTableTab()
            origin_current_tab.set_not_current()
            origin_current_tab.id = current_tabs[0].id
            self.update(origin_current_tab)

    @transactional
    def remove_tab(self, tab):
        self.delete(tab.id)
        # 调整order，找出排序在删除项之后的，向前整体移动一位
        move_order_forward_sql = ds_table_tab_sql_dict.get('move_order_forward')
        param = {
            'item_order': tab.item_order,
            'ds_type': tab.ds_type
        }
        get_db_conn().query(move_order_forward_sql, **param)
        log.info(f'将tab_table顺序前移语句 ==> {move_order_forward_sql}')
        log.info(f'将tab_table顺序前移参数 ==> {param}')
