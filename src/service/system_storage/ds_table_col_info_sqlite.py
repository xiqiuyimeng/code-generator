# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from PyQt6.QtCore import Qt

from src.service.system_storage.ds_col_type_sqlite import DsColTypeSqlite
from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic
from src.service.util.dataclass_util import init
from src.service.util.group_util import group_model_list
from src.service.util.system_storage_util import Condition

_author_ = 'luwt'
_date_ = '2022/10/8 12:32'

table_name = 'ds_table_col_info'

sql_dict = {
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
}


@init
@dataclass
class DsTableColInfo(BasicSqliteDTO):
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
    # 非数据库字段，指向父列数据
    parent_col: dataclass = field(init=False, default=None)

    def handle_data_type(self):
        self.data_type = self.full_data_type.split("(")[0]

    def init_value(self):
        self.is_pk = 0
        self.parent_id = 0
        self.expanded = 0


class DsTableColInfoSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict, DsTableColInfo)

    def save_cols(self, columns, parent_tab_id, check_state, ds_type,
                  parent_id=None, ds_col_type_sqlite=None):
        for index, column in enumerate(columns, start=1):
            column.parent_tab_id = parent_tab_id
            column.checked = check_state
            column.item_order = index
            if parent_id:
                column.parent_id = parent_id
        self.batch_insert(columns)

        # 在添加列的时候，将所有列的类型同步到数据源列类型表中
        if not ds_col_type_sqlite:
            ds_col_type_sqlite = DsColTypeSqlite()
        ds_col_type_sqlite.batch_sync_col_types(ds_type, {col.data_type for col in columns})

        # 考虑存在子集合的情况
        for col_info in columns:
            if not col_info.children:
                continue
            self.save_cols(col_info.children, parent_tab_id, check_state, ds_type,
                           col_info.id, ds_col_type_sqlite)

    def delete_by_parent_tab_id(self, parent_tab_id):
        condition = Condition(self.table_name).add('parent_tab_id', parent_tab_id)
        self.delete_by_condition(condition)

    def delete_by_parent_tab_ids(self, parent_tab_ids):
        condition = Condition(self.table_name).add('parent_tab_id', parent_tab_ids, 'in')
        self.delete_by_condition(condition)

    def get_tab_cols(self, parent_tab_id):
        # 获取当前tab页下所有列数据
        cols = self._get_table_cols(parent_tab_id)
        # 列数据按照 parent_id 分组
        cols_parent_id_dict = group_model_list(cols, lambda x: x.parent_id)

        # 找到所有父id对应的列数据，由于没有id为0的元素，所以这里会自动过滤掉父id为0，只会匹配其他有意义的父id
        parent_col_dict = {col.id: col for col in cols if col.id in cols_parent_id_dict}

        # 获取顶级节点数据，即 parent_id = 0
        top_cols = cols_parent_id_dict.get(0)
        top_cols.sort(key=lambda x: x.item_order)
        for col_id, col_data in parent_col_dict.items():
            # 赋值子集合
            children = cols_parent_id_dict.get(col_id)
            children.sort(key=lambda x: x.item_order)
            col_data.children = children
            # 在子元素中维持一个指向父元素的指针
            for child_col in children:
                child_col.parent_col = col_data
        return top_cols

    def _get_table_cols(self, parent_tab_id):
        condition = Condition(self.table_name).add('parent_tab_id', parent_tab_id)
        return self.select_by_order(condition=condition)

    def refresh_tab_cols(self, tab_id, columns, ds_type):
        self.delete_by_parent_tab_id(tab_id)
        # 默认数据应为未选中情况
        self.save_cols(columns, tab_id, Qt.CheckState.Unchecked.value, ds_type)

    def get_col_list_by_tab_id(self, parent_tab_id):
        condition = Condition(self.table_name).add('parent_tab_id', parent_tab_id)
        return self.select_by_order(condition=condition)
