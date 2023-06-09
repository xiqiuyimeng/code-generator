# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic
from src.service.util.dataclass_util import init, import_export
from src.service.util.system_storage_util import Condition, SelectCol

_author_ = 'luwt'
_date_ = '2023/2/12 11:46'

table_name = 'type_mapping'

sql_dict = {
    'create': f'''create table if not exists {table_name}
    (id integer primary key autoincrement,
    mapping_name char(50) not null,
    ds_type char(20) not null,
    comment text,
    max_col_type_group_num integer not null,
    item_order integer not null,
    create_time datetime,
    update_time datetime
    );''',
}


@init
@dataclass
class TypeMapping(BasicSqliteDTO):
    # 数据源类型映射名称
    mapping_name: str = field(init=False, default=None)
    # 数据源类型，例如 mysql、oracle、sqlite、json
    ds_type: str = field(init=False, default=None)
    # 数据源类型映射说明
    comment: str = field(init=False, default=None)
    # 列类型映射表中，当前映射下最大的映射组号，用以渲染列类型映射表结构
    max_col_type_group_num: int = field(init=False, default=None)
    # 类型映射列信息
    type_mapping_cols: list = field(init=False, default=None)

    def get_name(self):
        return self.mapping_name


@import_export(('id',))
@dataclass
class ImportExportTypeMapping:
    # 数据源类型映射名称
    mapping_name: str = field(default=None)
    # 数据源类型，例如 mysql、oracle、sqlite、json
    ds_type: str = field(default=None)
    # 数据源类型映射说明
    comment: str = field(default=None)
    # 列类型映射表中，当前映射下最大的映射组号，用以渲染列类型映射表结构
    max_col_type_group_num: int = field(default=None)
    # 类型映射列信息
    type_mapping_cols: list = field(default=None)


class TypeMappingSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict, TypeMapping)

    def save_type_mapping(self, type_mapping):
        type_mapping.item_order = self.get_max_order()
        self.insert(type_mapping)

    def get_type_mapping_by_id(self, type_mapping_id):
        condition = Condition(self.table_name).add('id', type_mapping_id)
        return self.select_one(condition=condition)

    def get_all_mapping_names(self):
        select_col = SelectCol(self.table_name).add('mapping_name')
        rows = self.select_by_order(select_cols=select_col)
        return [row.mapping_name for row in rows]

    def batch_save_type_mappings(self, type_mapping_list):
        max_order = self.get_max_order()
        for order, type_mapping in enumerate(type_mapping_list, start=max_order):
            type_mapping.item_order = order
        self.batch_insert(type_mapping_list)

    def get_id_by_names(self, type_mapping_list):
        select_col = SelectCol(self.table_name).add('id')
        mapping_names = [type_mapping.mapping_name for type_mapping in type_mapping_list]
        condition = Condition(self.table_name).add('mapping_name', mapping_names, 'in')
        rows = self.select_by_order(select_cols=select_col, condition=condition)
        return [row.id for row in rows]

    def export_type_mapping_by_ids(self, type_mapping_ids):
        select_col = SelectCol(self.table_name)
        select_col.add('id')
        select_col.add('mapping_name')
        select_col.add('ds_type')
        select_col.add('comment')
        select_col.add('max_col_type_group_num')
        condition = Condition(self.table_name).add('id', type_mapping_ids, 'in')
        return self.select_by_order(return_type=ImportExportTypeMapping,
                                    select_cols=select_col, condition=condition)
