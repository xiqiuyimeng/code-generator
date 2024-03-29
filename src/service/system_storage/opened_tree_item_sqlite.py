# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from PyQt6.QtCore import Qt

from src.enum.common_enum import SqlTreeItemLevelEnum, CurrentEnum, ExpandedEnum
from src.enum.ds_category_enum import DsCategoryEnum
from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic
from src.service.util.dataclass_util import init
from src.service.util.system_storage_util import Condition, transactional

_author_ = 'luwt'
_date_ = '2022/10/2 9:31'

table_name = 'opened_tree_item'

sql_dict = {
    'create': f'''create table if not exists {table_name}
    (id integer primary key autoincrement,
    item_name char(100) default null,
    is_current integer not null,
    expanded integer not null,
    checked integer default null,
    parent_id integer not null,
    level integer not null,
    ds_category char(10) not null,
    item_order integer not null,
    create_time datetime,
    update_time datetime
    );''',
    'max_level': f'select max(level) as max_level from {table_name} where ds_category = ',
}


@init
@dataclass
class OpenedTreeItem(BasicSqliteDTO):
    # 名称，对于sql数据源，是树的第一层元素，名称应以节点名为准，这里不做冗余，以id关联
    # 对于结构体数据源，是树节点元素
    item_name: str = field(init=False, default=None)
    # 标识元素是否应该置为当前项
    is_current: int = field(init=False, default=None)
    # 标识元素是否展开
    expanded: int = field(init=False, default=None)
    # 复选框状态，与qt复选框选中状态枚举保持一致
    checked: int = field(init=False, default=None)
    # 父id，sql数据源树第一层元素，指向对应外表id，其余子项，指向当前表父项id
    # 结构体数据源指向当前表父项id
    parent_id: int = field(init=False, default=None)
    # 元素在树中的级别
    level: int = field(init=False, default=None)
    # 数据源种类名称
    ds_category: str = field(init=False, default=None)
    # 数据类型，用以区分数据源中的各种类型，例如 sql数据源中的 ConnType，
    # 结构体数据源中的 StructType
    data_type: dataclass = field(init=False, default=None, compare=False)


class OpenedTreeItemSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict, OpenedTreeItem)

    def open_item(self, opened_item_id):
        opened_item = OpenedTreeItem()
        opened_item.id = opened_item_id
        opened_item.is_current = CurrentEnum.is_current.value
        opened_item.expanded = ExpandedEnum.expanded.value
        self.update_by_id(opened_item)

    def add_opened_child_item(self, child_item_names, opened_item_id, child_level,
                              ds_category, data_type, init_checked=True, insert_db=True):
        is_current = CurrentEnum.not_current.value
        expanded = ExpandedEnum.collapsed.value
        opened_child_items = list()
        for index, child_name in enumerate(child_item_names, start=1):
            opened_child_item = OpenedTreeItem()
            opened_child_item.item_name = child_name
            opened_child_item.is_current = is_current
            opened_child_item.expanded = expanded
            opened_child_item.parent_id = opened_item_id
            opened_child_item.level = child_level
            opened_child_item.ds_category = ds_category
            if init_checked:
                opened_child_item.checked = Qt.CheckState.Unchecked.value
            opened_child_item.item_order = index
            opened_child_item.data_type = data_type
            opened_child_items.append(opened_child_item)
        if insert_db:
            self.batch_insert(opened_child_items)
        return opened_child_items

    @transactional
    def item_current_changed(self, opened_item: OpenedTreeItem):
        # 找出当前数据源类型中当前项，全部置为非当前
        condition = Condition(self.table_name)
        condition.add('is_current', CurrentEnum.is_current.value)
        condition.add('ds_category', opened_item.ds_category)
        origin_current_items = self.select(condition=condition)

        update_params = list()
        if origin_current_items:
            for origin_current_item in origin_current_items:
                update_item = OpenedTreeItem()
                update_item.is_current = CurrentEnum.not_current.value
                update_item.id = origin_current_item.id
                update_params.append(update_item)
            self.batch_update(update_params)

        self.update_by_id(opened_item)

    def recursive_get_children(self, parent_id, level, ds_category, max_level=None):
        if max_level is not None and level > max_level:
            return
        opened_items = self.get_children(parent_id, level, ds_category)
        if opened_items:
            yield opened_items
            for opened_item in opened_items:
                # 作为父元素，继续查询子元素
                yield from self.recursive_get_children(opened_item.id,
                                                       opened_item.level + 1,
                                                       opened_item.ds_category,
                                                       max_level)

    def get_children(self, parent_id, level, ds_category):
        condition = Condition(self.table_name)
        condition.add('ds_category', ds_category)
        condition.add('level', level)
        condition.add('parent_id', parent_id)
        return self.select_by_order(condition=condition)

    def add_conn_opened_item(self, conn_id, conn_name):
        conn_item = OpenedTreeItem()
        conn_item.item_name = conn_name
        conn_item.is_current = CurrentEnum.not_current.value
        conn_item.expanded = ExpandedEnum.collapsed.value
        conn_item.parent_id = conn_id
        conn_item.level = SqlTreeItemLevelEnum.conn_level.value
        conn_item.ds_category = DsCategoryEnum.sql_ds_category.get_name()
        conn_item.item_order = self.get_max_order()
        self.insert(conn_item)
        return conn_item

    def update_conn_opened_record(self, conn_id, conn_name):
        condition = Condition(self.table_name)
        condition.add('parent_id', conn_id)
        condition.add('level', SqlTreeItemLevelEnum.conn_level.value)
        condition.add('ds_category', DsCategoryEnum.sql_ds_category.get_name())
        opened_conn_tree_item = self.select_one(condition=condition)
        if opened_conn_tree_item:
            opened_conn_tree_item.item_name = conn_name
            self.update_by_id(opened_conn_tree_item)

    def add_struct_opened_item(self, name, parent_id, level):
        ds_category = DsCategoryEnum.struct_ds_category.get_name()
        opened_tree_item = OpenedTreeItem()
        opened_tree_item.item_name = name
        opened_tree_item.is_current = CurrentEnum.not_current.value
        opened_tree_item.expanded = ExpandedEnum.collapsed.value
        opened_tree_item.parent_id = parent_id
        opened_tree_item.level = level
        opened_tree_item.ds_category = ds_category
        opened_tree_item.checked = Qt.CheckState.Unchecked.value
        condition = Condition(self.table_name)
        condition.add('ds_category', ds_category)
        condition.add('level', level)
        condition.add('parent_id', parent_id)
        opened_tree_item.item_order = self.get_max_order(condition)
        self.insert(opened_tree_item)
        return opened_tree_item

    def reorder_opened_items(self, reorder_items):
        update_opened_items = list()
        for opened_item in reorder_items:
            reorder_item = OpenedTreeItem()
            reorder_item.id = opened_item.id
            reorder_item.item_order = opened_item.item_order
            update_opened_items.append(reorder_item)
        self.batch_update(update_opened_items)

    def update_checked(self, opened_record):
        update_param = OpenedTreeItem()
        update_param.id = opened_record.id
        update_param.checked = opened_record.checked
        self.update_by_id(update_param)

    def update_child_checked(self, opened_record):
        # 批量更新所有子项选中状态
        update_param = OpenedTreeItem()
        update_param.checked = opened_record.checked
        self.update_by_condition(update_param, Condition(self.table_name).add('parent_id', opened_record.id))

    def get_max_level(self, ds_category):
        max_level_sql = f'{sql_dict.get("max_level")}"{ds_category}"'
        result = self.select_by_condition(select_cols=max_level_sql, fetch_all=False)
        return dict(result).get('max_level') if result else -1
