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
    data_type char(50) not null,
    full_data_type char(50) not null,
    is_pk integer not null,
    col_comment char(200) default null,
    checked integer not null,
    parent_tab_id integer not null,
    parent_id integer,
    item_order integer not null,
    col_type char(20) not null,
    expanded integer,
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
    is_pk: int = field(init=False, default=None)
    # 列注释
    col_comment: str = field(init=False, default=None)
    # 是否勾选，与qt中选中状态枚举保持一致
    checked: int = field(init=False, default=None)
    # 指向table_tab
    parent_tab_id: int = field(init=False, default=None)
    # 父id，指向当前表中的父id
    parent_id: int = field(init=False, default=None)
    # 列类型：列，对象，数组
    col_type: str = field(init=False, default=None)
    # 是否展开，用于存在子表的情况下，0，未展开 1，展开
    expanded: int = field(init=False, default=None)
    # 非数据库字段，是否在页面已经创建了子表，用于页面展示交互
    has_child_table: int = field(init=False, default=0)
    # 非数据库字段，维持子项列表
    children: list = field(init=False, default=None)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        if kwargs.get('init'):
            self.init_value()

    def handle_data_type(self):
        self.data_type = self.full_data_type.split("(")[0]

    def init_value(self):
        self.is_pk = 0
        self.parent_id = 0
        self.expanded = 0


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
