# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic
from src.service.util.dataclass_util import init, import_export
from src.service.util.system_storage_util import transactional, Condition

_author_ = 'luwt'
_date_ = '2023/2/12 11:46'

table_name = 'col_type_mapping'

sql_dict = {
    'create': f'''create table if not exists {table_name}
    (id integer primary key autoincrement,
    ds_col_type char(20) not null,
    mapping_col_name char(20) not null,
    mapping_type char(20) not null,
    import_desc text,
    group_num integer not null,
    parent_id integer not null,
    item_order integer not null,
    create_time datetime,
    update_time datetime
    );''',
}


@init
@dataclass
class ColTypeMapping(BasicSqliteDTO):
    # 数据源列类型
    ds_col_type: str = field(init=False, default=None)
    # 映射列名称，在模板中使用
    mapping_col_name: str = field(init=False, default=None)
    # 映射类型
    mapping_type: str = field(init=False, default=None)
    # 引包声明
    import_desc: str = field(init=False, default=None)
    # 类型映射组，当一个列映射多组类型时，需要派生出多个组
    group_num: int = field(init=False, default=None)
    # 类型映射列表父id
    parent_id: int = field(init=False, default=None)


@import_export(('parent_id',))
@dataclass
class ImportExportColTypeMapping:
    # 数据源列类型
    ds_col_type: str = field(default=None)
    # 映射列名称，在模板中使用
    mapping_col_name: str = field(default=None)
    # 映射类型
    mapping_type: str = field(default=None)
    # 引包声明
    import_desc: str = field(default=None)
    # 类型映射组，当一个列映射多组类型时，需要派生出多个组
    group_num: int = field(default=None)


class ColTypeMappingSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict, ColTypeMapping)

    def get_by_parent_id(self, parent_id):
        condition = Condition(self.table_name).add('parent_id', parent_id)
        return self.select_by_order(condition=condition)

    def batch_save(self, col_type_mappings, parent_id):
        # 批量保存
        for order, col_type_mapping in enumerate(col_type_mappings, start=1):
            col_type_mapping.item_order = order
            col_type_mapping.parent_id = parent_id
        self.batch_insert(col_type_mappings)

    @transactional
    def edit_col_type_mappings(self, col_type_mappings, parent_id):
        # 首先删除原数据
        self.delete_by_parent_ids((parent_id,))
        # 插入新数据
        if col_type_mappings:
            for order, col_type_mapping in enumerate(col_type_mappings, start=1):
                col_type_mapping.item_order = order
                col_type_mapping.parent_id = parent_id
            self.batch_insert(col_type_mappings)

    def delete_by_parent_ids(self, parent_ids):
        self.delete_by_condition(Condition(self.table_name).add('parent_id', parent_ids, 'in'))

    def export_by_parent_ids(self, parent_ids):
        condition = Condition(self.table_name).add('parent_id', parent_ids, 'in')
        return self.select_by_order(return_type=ImportExportColTypeMapping, condition=condition)
