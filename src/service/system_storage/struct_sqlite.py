# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from src.logger.log import logger as log
from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic, get_db_conn
from src.service.system_storage.struct_type import mapping_struct_type

_author_ = 'luwt'
_date_ = '2022/11/11 16:49'

table_name = 'struct_info'

struct_sql_dict = {
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
    'select_list': f'select opened_item_id, struct_type from {table_name}',
    'delete_by_opened_item_id': f'delete from {table_name} where opened_item_id = ',
    'delete_by_opened_item_ids': f'delete from {table_name} where opened_item_id in ',
}


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

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        mapping_struct_type(self)


class StructSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, struct_sql_dict)

    def select_list(self):
        rows = self._do_select(struct_sql_dict.get('select_list'), StructInfo())
        return list(map(lambda x: StructInfo(**x), rows.all()))

    def delete_by_opened_item_id(self, opened_item_id):
        sql = f"{struct_sql_dict.get('delete_by_opened_item_id')}{opened_item_id}"
        get_db_conn().query(sql)
        log.info(f'删除[{self.table_name}]语句 ==> {sql}')

    def delete_by_opened_item_ids(self, opened_item_ids):
        opened_item_id_list = ", ".join(map(lambda x: str(x), opened_item_ids))
        sql = f"{struct_sql_dict.get('delete_by_opened_item_ids')}({opened_item_id_list})"
        get_db_conn().query(sql)
        log.info(f'删除[{self.table_name}]语句 ==> {sql}')

    def get_struct_info(self, opened_item_id):
        param = StructInfo()
        param.opened_item_id = opened_item_id
        return self.select_one(param)
