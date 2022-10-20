# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from enum import Enum

from service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic

_author_ = 'luwt'
_date_ = '2022/10/2 9:31'

table_name = 'opened_tree_item'

opened_item_sql_dict = {
    'create': f'''create table  if not exists {table_name}
    (id integer primary key autoincrement,
    item_name char(100) default null,
    is_current integer not null,
    expanded integer not null,
    checked integer default null,
    parent_id integer not null,
    level integer not null,
    ds_type_name char(10) not null,
    table_tab_id integer default null,
    create_time datetime,
    update_time datetime
    );''',
    'delete_child': f'delete from {table_name} where parent_id = :parent_id',
    'delete_conn': f'delete from {table_name} where parent_id = :parent_id and item_name is null',
}


@dataclass
class OpenedTreeItem(BasicSqliteDTO):

    # 名称，树第一层元素，名称应以节点名为准，这里不做冗余，以id关联
    item_name: str = field(init=False, default=None)
    # 标识元素是否应该置为当前项
    is_current: int = field(init=False, default=None)
    # 标识元素是否展开
    expanded: int = field(init=False, default=None)
    # 复选框状态，与qt复选框选中状态枚举保持一致
    checked: int = field(init=False, default=None)
    # 父id，树第一层元素，指向对应外表id，其余子项，指向当前表父项id
    parent_id: int = field(init=False, default=None)
    # 元素在树中的级别
    level: int = field(init=False, default=None)
    # 数据源 name
    ds_type_name: str = field(init=False, default=None)
    # table_tab表id，用来关联table_tab
    table_tab_id: int = field(init=False, default=None)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class SqlTreeItemLevel(Enum):

    conn_level = 0
    db_level = 1
    tb_level = 2


class CurrentEnum(Enum):

    is_current = 1
    not_current = 0


class ExpandedEnum(Enum):

    expanded = 1
    collapsed = 0


class CheckedEnum(Enum):

    checked = 2
    unchecked = 0


class OpenedTreeItemSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, opened_item_sql_dict)

    def open_item(self, opened_item_id):
        opened_item = OpenedTreeItem()
        opened_item.id = opened_item_id
        opened_item.is_current = CurrentEnum.is_current.value
        opened_item.expanded = ExpandedEnum.expanded.value
        self.update(opened_item)

    def add_opened_child_item(self, child_item_names, opened_item_id, child_level, ds_type):
        is_current = CurrentEnum.not_current.value
        expanded = ExpandedEnum.collapsed.value
        opened_child_items = list()
        for child_name in child_item_names:
            opened_child_item = OpenedTreeItem()
            opened_child_item.item_name = child_name
            opened_child_item.is_current = is_current
            opened_child_item.expanded = expanded
            opened_child_item.parent_id = opened_item_id
            opened_child_item.level = child_level
            opened_child_item.ds_type_name = ds_type
            opened_child_item.checked = CheckedEnum.unchecked.value
            opened_child_items.append(opened_child_item)
        self.batch_insert(opened_child_items)
        return opened_child_items

    def item_current_changed(self, opened_item: OpenedTreeItem):
        # 找出当前数据源类型中当前项，全部置为非当前
        item_param = OpenedTreeItem()
        item_param.is_current = CurrentEnum.is_current.value
        item_param.ds_type_name = opened_item.ds_type_name
        origin_current_items = self.select(item_param)

        update_params = list()
        if origin_current_items:
            for origin_current_item in origin_current_items:
                update_item = OpenedTreeItem()
                update_item.is_current = CurrentEnum.not_current.value
                update_item.id = origin_current_item.id
                update_params.append(update_item)
            self.batch_update(update_params)

        self.update(opened_item)

    def delete_by_parent_id(self, parent_id):
        delete_child_sql = opened_item_sql_dict.get('delete_child')
        self.db.query(delete_child_sql, **{'parent_id': parent_id})

    def delete_conn(self, parent_id):
        delete_conn_sql = opened_item_sql_dict.get('delete_conn')
        self.db.query(delete_conn_sql, **{'parent_id': parent_id})