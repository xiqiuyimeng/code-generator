# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic

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
    # 类型映射列信息，映射列名：list
    type_mapping_cols: dict = field(init=False, default=None)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class TypeMappingSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict)

    def save_type_mapping(self, type_mapping):
        type_mapping.item_order = self.get_max_order()
        self.insert(type_mapping)

    def get_type_mapping_by_id(self, type_mapping_id):
        param = TypeMapping()
        param.id = type_mapping_id
        return self.select_one(param)
