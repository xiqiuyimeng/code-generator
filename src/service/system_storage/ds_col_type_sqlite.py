# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from itertools import groupby

from src.logger.log import logger as log
from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic, get_db_conn, transactional
from src.service.util.db_id_generator import update_id_generator

_author_ = 'luwt'
_date_ = '2023/2/12 19:28'


table_name = 'ds_col_type'

sql_dict = {
    'create': f'''create table if not exists {table_name}
    (id integer primary key autoincrement,
    ds_col_type char(20) not null,
    parent_id integer(20) not null,
    item_order integer not null,
    create_time datetime,
    update_time datetime
    );''',
    'truncate': f'delete from {table_name}',
    'delete_children': f'delete from {table_name} where parent_id = :parent_id',
    'delete_children_by_parent_ids': f'delete from {table_name} where parent_id in ',
    'get_ds_type': f'select * from {table_name} where parent_id = 0',
}


@dataclass
class DsColType(BasicSqliteDTO):
    # 数据源列类型
    ds_col_type: str = field(init=False, default=None)
    # 父id，父id为0时，为数据源类型，大于0，则为数据列类型
    parent_id: int = field(init=False, default=None)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class DsColTypeSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict)

    def get_all_ds_col_types(self):
        ds_col_types = self.select(DsColType(), order_by='parent_id')
        if ds_col_types:
            # 以parent_id为key，进行分组
            parent_id_group = groupby(ds_col_types, key=lambda x: x.parent_id)
            parent_id_dict = dict(map(lambda x: (x[0], list(x[1])), parent_id_group))

            ds_types = parent_id_dict.get(0)
            ds_types.sort(key=lambda x: x.item_order)
            ds_col_type_dict = dict()
            for ds_type in ds_types:
                col_types = parent_id_dict.get(ds_type.id, list())
                col_types.sort(key=lambda x: x.item_order)
                # 映射为 ds_type: tuple ds_col_type
                ds_col_type_dict[ds_type.ds_col_type] = list(map(lambda x: x.ds_col_type, col_types))
            return ds_col_type_dict

    @transactional
    def truncate_table(self):
        truncate_sql = sql_dict.get('truncate')
        get_db_conn().query(truncate_sql)
        # 将id 生成器重置
        update_id_generator(table_name)
        log.info(f'清空表{self.table_name}成功')

    @staticmethod
    def assemble_ds_type(ds_type, item_order):
        ds_col_type = DsColType()
        ds_col_type.ds_col_type = ds_type
        ds_col_type.parent_id = 0
        ds_col_type.item_order = item_order
        return ds_col_type

    @staticmethod
    def batch_assemble_ds_col_types(col_types, parent_id):
        ds_col_types = list()
        for order, col_type in enumerate(col_types, start=1):
            ds_col_type = DsColType()
            ds_col_type.ds_col_type = col_type
            ds_col_type.parent_id = parent_id
            ds_col_type.item_order = order
            ds_col_types.append(ds_col_type)
        return ds_col_types

    def get_ds_type(self, ds_type):
        query_param = DsColType()
        query_param.ds_col_type = ds_type
        query_param.parent_id = 0
        return self.select_one(query_param)

    def batch_sync_col_types(self, ds_type, col_types):
        """在保存数据表列的时候，批量同步列的类型，以动态维护数据源列类型"""
        # 首先根据数据源类型，找出传入的列类型中，哪些表中不存在
        ds_type_obj = self.get_ds_type(ds_type)
        if ds_type_obj:
            # 查询列类型
            query_param = DsColType()
            query_param.parent_id = ds_type_obj.id
            col_types_exists = self.select(query_param)
            # 求差集，判断是否需要新增
            exists_col_type_set = set(map(lambda x: x.ds_col_type, col_types_exists))
            dff_set = col_types - exists_col_type_set
            if dff_set:
                # 移除当前数据源类型下所有列类型
                delete_children_sql = sql_dict.get('delete_children')
                get_db_conn().query(delete_children_sql, **{'parent_id': ds_type_obj.id})
                # 批量插入：新的列类型 + 已经存在的列类型，这样可以进行排序
                all_col_types = sorted(col_types | exists_col_type_set)
                new_col_types = self.batch_assemble_ds_col_types(all_col_types, ds_type_obj.id)
                self.batch_insert(new_col_types)

    def get_ds_types(self):
        log.info(f'查询{self.table_name}中所有数据源类型')
        sql = sql_dict.get('get_ds_type')
        ds_type_rows = get_db_conn().query(sql)
        return list(map(lambda x: DsColType(**x), ds_type_rows.as_dict()))

    def batch_delete_ds_types(self, ds_type_ids):
        # 首先删除数据源类型
        self.batch_delete(ds_type_ids)
        # 再删除列类型
        parent_ids = ','.join(map(lambda x: str(x), ds_type_ids))
        delete_col_type_sql = f"{sql_dict.get('delete_children_by_parent_ids')}({parent_ids})"
        get_db_conn().query(delete_col_type_sql)
