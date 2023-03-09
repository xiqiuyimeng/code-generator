# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from src.logger.log import logger as log
from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic, get_db_conn, transactional

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
    'delete_by_parent_ids': f'delete from {table_name} where parent_id in '
}


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

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class ColTypeMappingSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict)

    def get_by_parent_id(self, parent_id):
        param = ColTypeMapping()
        param.parent_id = parent_id
        return self.select_by_order(param)

    def save_col_type_mappings(self, col_type_mappings):
        # 批量保存
        for order, col_type_mapping in enumerate(col_type_mappings, start=1):
            col_type_mapping.item_order = order
        self.batch_insert(col_type_mappings)

    @transactional
    def edit_col_type_mappings(self, col_type_mappings, parent_id):
        # 首先删除原数据
        self.delete_by_parent_ids((parent_id, ))
        # 插入新数据
        if col_type_mappings:
            for order, col_type_mapping in enumerate(col_type_mappings, start=1):
                col_type_mapping.item_order = order
                col_type_mapping.parent_id = parent_id
            self.batch_insert(col_type_mappings)

    def delete_by_parent_ids(self, parent_ids):
        ids_str = ','.join(map(lambda x: str(x), parent_ids))
        sql = f"{sql_dict.get('delete_by_parent_ids')} ({ids_str})"
        get_db_conn().query(sql)
        log.info(f'{self.table_name} 根据parent_id: {parent_ids} 删除')
