# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from enum import Enum
from typing import List

from src.logger.log import logger as log
from src.service.system_storage.ds_table_col_info_sqlite import DsTableColInfo
from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic
from src.service.util.dataclass_util import init
from src.service.util.system_storage_util import Condition, SelectCol, transactional, get_cursor

_author_ = 'luwt'
_date_ = '2022/10/8 12:30'

table_name = 'ds_table_tab'

sql_dict = {
    'create': f'''create table if not exists {table_name}
    (id integer PRIMARY KEY autoincrement,
    parent_opened_id integer not null,
    item_order integer not null,
    is_current integer not null,
    ds_category char(10) not null,
    create_time datetime,
    update_time datetime
    );''',
    'move_order_forward': f'update {table_name} set item_order = item_order - 1 '
                          f'where item_order > ? and ds_category = ?',
}


@init
@dataclass
class DsTableTab(BasicSqliteDTO):
    # 父id，指向opened_tree_item表
    parent_opened_id: int = field(init=False, default=None)
    # 标识tab是否应该置为当前项
    is_current: int = field(init=False, default=None)
    # 数据源种类
    ds_category: str = field(init=False, default=None)
    # col_list
    col_list: List[DsTableColInfo] = field(init=False, default=None)

    def set_current(self):
        self.is_current = CurrentEnum.is_current.value

    def set_not_current(self):
        self.is_current = CurrentEnum.not_current.value


class CurrentEnum(Enum):
    is_current = 1
    not_current = 0


class DsTableTabSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict, DsTableTab)

    def add_tab(self, opened_table_item):
        self.change_other_not_current(opened_table_item.ds_category)

        table_tab = DsTableTab()
        table_tab.parent_opened_id = opened_table_item.id
        condition = Condition(self.table_name).add('ds_category', opened_table_item.ds_category)
        table_tab.item_order = self.get_max_order(condition)
        table_tab.ds_category = opened_table_item.ds_category
        table_tab.set_current()
        self.insert(table_tab)
        return table_tab

    @transactional
    def change_current(self, current_tab: DsTableTab):
        # 将同一数据源下的其他项全部置为非当前，将当前值置为当前项
        self.change_other_not_current(current_tab.ds_category)
        current_tab.set_current()
        self.update_by_id(current_tab)

    def change_other_not_current(self, ds_category):
        # 将同一数据源种类下的其他项全部置为非当前
        condition = Condition(self.table_name)
        condition.add('is_current', CurrentEnum.is_current.value)
        condition.add('ds_category', ds_category)
        current_tab = self.select_one(condition=condition)
        if current_tab:
            origin_current_tab = DsTableTab()
            origin_current_tab.set_not_current()
            origin_current_tab.id = current_tab.id
            self.update_by_id(origin_current_tab)

    def remove_tab(self, tab):
        self.delete_by_id(tab.id)
        # 调整order，找出排序在删除项之后的，向前整体移动一位
        move_order_forward_sql = sql_dict.get('move_order_forward')
        param = (tab.item_order, tab.ds_category)
        get_cursor().execute(move_order_forward_sql, param)
        log.info(f'将tab_table顺序前移语句 ==> {move_order_forward_sql}')
        log.info(f'将tab_table顺序前移参数 ==> {param}')

    def select_by_opened_ids(self, opened_ids):
        select_col = SelectCol(self.table_name).add('id').add('parent_opened_id')
        condition = Condition(self.table_name).add('parent_opened_id', opened_ids, 'in')
        return self.select_by_order(select_cols=select_col, condition=condition)

    def get_ds_category_tabs(self, ds_category):
        condition = Condition(self.table_name).add('ds_category', ds_category)
        return self.select_by_order(condition=condition)
