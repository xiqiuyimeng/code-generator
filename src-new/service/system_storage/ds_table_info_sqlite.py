# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from enum import Enum

from service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic, get_db_conn
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
    parent_id integer,
    item_order integer not null,
    col_type char(20) not null,
    create_time datetime,
    update_time datetime
    );''',
    'delete_by_parent_tab_id': f'delete from {table_name} where parent_tab_id = ',
}


class CheckedEnum(Enum):

    checked = 2
    unchecked = 0


class ColTypeEnum(Enum):

    col = 'col'
    obj = 'object'
    array = 'array'


@dataclass
class DsTableInfo(BasicSqliteDTO):

    # 列名
    col_name: str = field(init=False, default=None)
    # 数据类型，只包含数据类型，不包含字段长度
    data_type: str = field(init=False, default=None)
    # 完整数据类型 = 数据类型 + 字段长度
    full_data_type: str = field(init=False, default=None)
    # 是否是主键
    is_pk: int = field(init=False, default=0)
    # 列注释
    col_comment: str = field(init=False, default=None)
    # 是否勾选，与qt中选中状态枚举保持一致
    checked: int = field(init=False, default=None)
    # 指向table_tab
    parent_tab_id: int = field(init=False, default=None)
    # 父id，指向当前表中的父id
    parent_id: int = field(init=False, default=0)
    # 列类型：列，对象，数组
    col_type: str = field(init=False, default=None)
    # 非数据库字段，维持子项列表
    children: list = field(init=False, default=None)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def handle_data_type(self):
        self.data_type = self.full_data_type.split("(")[0]


class DsTableInfoSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, ds_table_info_sql_dict)

    def add_table(self, columns, parent_tab_id, check_state):
        for index, column in enumerate(columns, start=1):
            column.parent_tab_id = parent_tab_id
            column.checked = check_state
            column.item_order = index
        self.batch_insert(columns)

    @staticmethod
    def delete_by_parent_tab_id(parent_tab_id):
        delete_sql = f"{ds_table_info_sql_dict.get('delete_by_parent_tab_id')}{parent_tab_id}"
        get_db_conn().query(delete_sql)
        log.info(f"删除{table_name}语句 ==> {delete_sql}")
