# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic
from src.service.system_storage.struct_type import mapping_struct_type
from src.service.util.dataclass_util import init
from src.service.util.system_storage_util import SelectCol, Condition

_author_ = 'luwt'
_date_ = '2022/11/11 16:49'

table_name = 'struct_info'

sql_dict = {
    'create': f'''create table if not exists {table_name}
    (id integer primary key autoincrement,
    opened_item_id integer not null,
    struct_name char(50) not null,
    struct_type char(30) not null,
    content text,
    file_url text,
    create_time datetime,
    update_time datetime
    );''',
}


@init
@dataclass
class StructInfo(BasicSqliteDTO):
    opened_item_id: str = field(init=False, default=None, compare=False)
    struct_name: str = field(init=False, default=None)
    struct_type: str = field(init=False, default=None)
    # 具体结构体内容，文本信息
    content: str = field(init=False, default=None)
    # 结构体文件地址
    file_url: str = field(init=False, default=None)
    # 根据struct type映射为 StructType
    struct_type_info: dataclass = field(init=False, default=None, compare=False)


class StructSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict, StructInfo)

    def select_list(self):
        select_col = SelectCol(self.table_name).add('opened_item_id').add('struct_type')
        struct_list = self.select(select_cols=select_col)
        for struct in struct_list:
            mapping_struct_type(struct)
        return struct_list

    def delete_by_opened_item_id(self, opened_item_id):
        condition = Condition(self.table_name).add('opened_item_id', opened_item_id)
        self.delete_by_condition(condition)

    def delete_by_opened_item_ids(self, opened_item_ids):
        condition = Condition(self.table_name).add('opened_item_id', opened_item_ids, 'in')
        self.delete_by_condition(condition)

    def get_struct_info(self, opened_item_id):
        condition = Condition(self.table_name).add('opened_item_id', opened_item_id)
        struct = self.select_one(condition=condition)
        mapping_struct_type(struct)
        return struct
