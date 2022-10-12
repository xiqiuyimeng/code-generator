# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from enum import Enum

from service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic
from logger.log import logger as log

_author_ = 'luwt'
_date_ = '2022/10/8 12:32'

table_name = 'ds_table_info'

ds_table_info_sql_dict = {
    'create': f'''create table if not exists {table_name}
    (id integer PRIMARY KEY autoincrement,
    col_name char(50) not null,
    data_type char(20) not null,
    full_data_type char(20) not null,
    is_pk integer not null,
    col_comment char(200) default null,
    checked integer not null,
    parent_tab_id integer not null,
    create_time datetime,
    update_time datetime
    );''',
    'delete_by_parent_tab_id': f'delete from {table_name} where parent_tab_id = ',
}


class CheckedEnum(Enum):
    checked = 1
    unchecked = 0


@dataclass
class DsTableInfo(BasicSqliteDTO):

    # 列名
    col_name: str = field(init=False, default=None)
    # 数据类型，只包含数据类型，不包含字段长度
    data_type: str = field(init=False, default=None)
    # 完整数据类型 = 数据类型 + 字段长度
    full_data_type: str = field(init=False, default=None)
    # 是否是主键
    is_pk: int = field(init=False, default=None)
    # 列注释
    col_comment: str = field(init=False, default=None)
    # 是否勾选
    checked: int = field(init=False, default=None)
    # 指向table_tab
    parent_tab_id: int = field(init=False, default=None)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def handle_data_type(self):
        self.data_type = self.full_data_type.split("(")[0]


class DsTableInfoSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, ds_table_info_sql_dict)

    def add_table(self, columns, parent_tab_id):
        for column in columns:
            column.parent_tab_id = parent_tab_id
        self.batch_insert(columns)

    def delete_by_parent_tab_id(self, parent_tab_id):
        delete_sql = f"{ds_table_info_sql_dict.get('delete_by_parent_tab_id')}{parent_tab_id}"
        self.db.query(delete_sql)
        log.info(f"删除{table_name}语句 ==> {delete_sql}")
