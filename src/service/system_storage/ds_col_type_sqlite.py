# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from src.logger.log import logger as log
from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic
from src.service.util.dataclass_util import init
from src.service.util.db_id_generator_util import update_id_generator
from src.service.util.group_util import group_model_list
from src.service.util.system_storage_util import transactional, Condition

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
}


@init
@dataclass
class DsColType(BasicSqliteDTO):
    # 数据源列类型
    ds_col_type: str = field(init=False, default=None)
    # 父id，父id为0时，为数据源类型，大于0，则为数据列类型
    parent_id: int = field(init=False, default=None)


class DsColTypeSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict, DsColType)

    def get_all_ds_col_types(self):
        ds_col_types = self.select(order_by='parent_id')
        if ds_col_types:
            # 以parent_id为key，进行分组
            parent_id_dict = group_model_list(ds_col_types, lambda x: x.parent_id)
            # parent id 为 0 的是数据源类型
            ds_types = parent_id_dict.get(0)
            ds_types.sort(key=lambda x: x.item_order)
            ds_col_type_dict = dict()
            for ds_type in ds_types:
                col_types = parent_id_dict.get(ds_type.id, list())
                col_types.sort(key=lambda x: x.item_order)
                # 映射为 ds_type: list[ds_col_type]
                ds_col_type_dict[ds_type.ds_col_type] = [col_type.ds_col_type for col_type in col_types]
            return ds_col_type_dict

    @transactional
    def truncate_table(self):
        condition = Condition(self.table_name)
        self.delete_by_condition(condition)
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
        condition = Condition(self.table_name)
        condition.add('ds_col_type', ds_type)
        condition.add('parent_id', 0)
        return self.select_one(condition=condition)

    def batch_sync_col_types(self, ds_type, col_types):
        """在保存数据表列的时候，批量同步列的类型，以动态维护数据源列类型"""
        # 首先根据数据源类型，找出传入的列类型中，哪些表中不存在
        ds_type_obj = self.get_ds_type(ds_type)
        if ds_type_obj:
            # 查询列类型
            condition = Condition(self.table_name).add('parent_id', ds_type_obj.id)
            col_types_exists = self.select(condition=condition)
            # 求差集，判断是否需要新增
            exists_col_type_set = {col_type.ds_col_type for col_type in col_types_exists}
            diff_set = col_types - exists_col_type_set
            if diff_set:
                # 移除当前数据源类型下所有列类型
                self.delete_children(ds_type_obj.id)
                # 批量插入：新的列类型 + 已经存在的列类型，这样可以进行排序
                all_col_types = sorted(col_types | exists_col_type_set)
                new_col_types = self.batch_assemble_ds_col_types(all_col_types, ds_type_obj.id)
                self.batch_insert(new_col_types)

    def delete_children(self, parent_id):
        condition = Condition(self.table_name).add('parent_id', parent_id)
        self.delete_by_condition(condition)

    def get_ds_types(self):
        log.info(f'查询{self.table_name}中所有数据源类型')
        condition = Condition(self.table_name).add('parent_id', 0)
        return self.select_by_order(condition=condition)

    def batch_delete_ds_types(self, ds_type_ids):
        # 首先删除数据源类型
        self.delete_by_ids(ds_type_ids)
        # 再删除列类型
        condition = Condition(self.table_name).add('parent_id', ds_type_ids, 'in')
        self.delete_by_condition(condition)
