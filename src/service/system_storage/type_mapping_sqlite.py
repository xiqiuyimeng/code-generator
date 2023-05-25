# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from src.logger.log import logger as log
from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic, get_db_conn

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
    'export': f'select id, mapping_name, ds_type, comment, max_col_type_group_num from {table_name} where id in ',
    'all_mapping_names': f'select mapping_name from {table_name}',
    'get_id_by_names': f'select id from {table_name} where mapping_name in '
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
    # 类型映射列信息
    type_mapping_cols: list = field(init=False, default=None)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_name(self):
        return self.mapping_name


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

    def convert_import(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
        return self

    def convert_export(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k) or k == 'id':
                setattr(self, k, v)
        return self


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

    def get_all_mapping_names(self):
        sql = sql_dict.get('all_mapping_names')
        rows = get_db_conn().query(sql)
        log.info(f'{self.table_name} 获取所有映射名称')
        return [row.get('mapping_name') for row in rows.as_dict()]

    def batch_save_type_mappings(self, type_mapping_list):
        max_order = self.get_max_order()
        for order, type_mapping in enumerate(type_mapping_list, start=max_order):
            type_mapping.item_order = order
        self.batch_insert(type_mapping_list)

    def get_id_by_names(self, type_mapping_list):
        name_str = ','.join([f'"{type_mapping.mapping_name}"' for type_mapping in type_mapping_list])
        sql = f"{sql_dict.get('get_id_by_names')} ({name_str})"
        rows = get_db_conn().query(sql)
        log.info(f'{self.table_name} 根据名称查询id')
        return [row.get('id') for row in rows.as_dict()]

    def export_type_mapping_by_ids(self, type_mapping_ids):
        ids_str = ','.join([str(type_mapping_id) for type_mapping_id in type_mapping_ids])
        sql = f"{sql_dict.get('export')} ({ids_str})"
        rows = get_db_conn().query(sql)
        log.info(f'{self.table_name} 根据 id: {type_mapping_ids} 导出')
        return [ImportExportTypeMapping().convert_export(**row) for row in rows.as_dict()]
