# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import Union

from src.logger.log import logger as log
from src.service.util.db_id_generator_util import update_id_generator, get_id
from src.service.util.system_storage_util import get_cursor, get_now_str, batch_operate, Condition, get_field_list, \
    SelectCol, update_table_field_dict

_author_ = 'luwt'
_date_ = '2022/5/11 10:25'


@dataclass
class BasicSqliteDTO:
    id: int = field(default=None, init=False, compare=False)
    item_order: int = field(init=False, default=None, compare=False)
    create_time: str = field(default=None, init=False, compare=False)
    update_time: str = field(default=None, init=False, compare=False)


class SqliteBasic:
    """
    操作sqlite数据库的基类，
    约定：每个表必须有id且为自增主键，
         每个表必须有create_time自动初始化，
         每个表必须有update_time自动更新，
         每个表应该有item_order，描述顺序关系
    """

    def __init__(self, table_name, sql_dict, model_type):
        self.table_name = table_name
        self.model_type = model_type
        self._create_table_sql = sql_dict.get('create')
        self._check_table_sql = f'PRAGMA table_info ("{self.table_name}")'
        self._create_table()

        # 常用sql
        self._insert_sql = f'insert into {self.table_name}'
        self._update_sql = f'update {self.table_name} set'
        self._delete_sql = f'delete from {self.table_name}'
        self._max_order_sql = f'select ifnull(max(item_order), 0) as max_order from {self.table_name}'

    def _create_table(self):
        cursor = get_cursor()
        cursor.execute(self._check_table_sql)
        data = cursor.fetchone()
        check_success = data and dict(data)
        if not check_success:
            # 如果表不存在，需要重新创建
            cursor.execute(self._create_table_sql)
            # 创建完成后，需要同步更新id生成器
            update_id_generator(self.table_name)
            # 更新表字段
            update_table_field_dict(self.table_name)

    def insert(self, insert_obj: BasicSqliteDTO):
        """新增记录方法，根据约定，id由数据库管理，创建时间、更新时间传入当前时间"""
        insert_obj.create_time = get_now_str()
        insert_obj.update_time = get_now_str()
        # 分配id
        insert_obj.id = get_id(self.table_name, 1)[0]
        # 过滤掉不合法的field
        insert_dict = self.filter_illegal_field(insert_obj)

        if insert_dict:
            insert_sql = f'{self._insert_sql} ({", ".join(insert_dict)}) ' \
                         f'values ({", ".join("?" * len(insert_dict))})'
            param = tuple(insert_dict.values())
            log.info(f'插入[{self.table_name}]语句 ==> {insert_sql}')
            log.info(f'插入[{self.table_name}]参数 ==> {param}')
            get_cursor().execute(insert_sql, param)

    @batch_operate
    def batch_insert(self, insert_objs):
        """批量插入"""
        id_list = get_id(self.table_name, len(insert_objs))
        for idx, insert_obj in enumerate(insert_objs):
            insert_obj.create_time = get_now_str()
            insert_obj.update_time = get_now_str()
            # 分配id
            insert_obj.id = id_list[idx]
        insert_dict_list = [self.filter_illegal_field(insert_data) for insert_data in insert_objs]

        insert_sql = f'{self._insert_sql} ({", ".join(insert_dict_list[0])}) ' \
                     f'values ({", ".join("?" * len(insert_dict_list[0]))})'
        params = [tuple(row_dict.values()) for row_dict in insert_dict_list]
        log.info(f'批量插入[{self.table_name}]语句 ==> {insert_sql}')
        log.info(f'批量插入[{self.table_name}]参数 ==> {params}')
        get_cursor().executemany(insert_sql, params)

    def delete_by_id(self, obj_id):
        self.delete_by_condition(Condition(self.table_name).add('id', obj_id))

    @batch_operate
    def delete_by_ids(self, obj_ids):
        self.delete_by_condition(Condition(self.table_name).add('id', obj_ids, 'in'))

    def delete_by_condition(self, condition: Condition):
        self.delete(condition, condition.params)

    def delete(self, where_clause, params):
        delete_sql = f'{self._delete_sql} {where_clause}'
        log.info(f'删除[{self.table_name}]语句 ==> {delete_sql}')
        log.info(f'删除[{self.table_name}]参数 ==> {params}')
        get_cursor().execute(delete_sql, params)

    def update_by_id(self, update_obj: BasicSqliteDTO):
        """更新记录方法，根据id更新"""
        self.update_by_condition(update_obj, Condition(self.table_name).add('id', update_obj.id))

    def update_by_condition(self, update_obj: BasicSqliteDTO, condition: Condition):
        self.update(update_obj, condition, condition.params)

    def construct_update_set_sql(self, update_dict):
        # 只更新除id和创建时间以外不为空的属性
        update_field_list = [k for k, v in update_dict.items() if v is not None and k not in ('id', 'create_time')]

        if update_field_list:
            update_field_str = ", ".join([f'{field_str} = ?' for field_str in update_field_list])
            # 拼接sql
            return f'{self._update_sql} {update_field_str}', update_field_list

    def update(self, update_obj: BasicSqliteDTO, where_clause, condition_params):
        """更新记录，创建时间不修改，更新时间为当前时间"""
        update_obj.update_time = get_now_str()
        update_dict = self.filter_illegal_field(update_obj)

        # 获取sql和更新字段列表
        update_set_sql, update_field_list = self.construct_update_set_sql(update_dict)
        update_sql = f'{update_set_sql} {where_clause}'
        # 收集更新的value list
        update_values = [update_dict.get(update_field) for update_field in update_field_list]
        update_values.extend(condition_params)
        log.info(f'更新[{self.table_name}]语句 ==> {update_sql}')
        log.info(f'更新[{self.table_name}]参数 ==> {update_values}')
        get_cursor().execute(update_sql, update_values)

    @batch_operate
    def batch_update(self, update_objs):
        """批量更新"""
        update_dict_list = list()
        for update_obj in update_objs:
            update_obj.update_time = get_now_str()
            update_dict = self.filter_illegal_field(update_obj)
            update_dict_list.append(update_dict)

        # 获取sql和更新字段列表
        update_set_sql, update_field_list = self.construct_update_set_sql(update_dict_list[0])

        # 收集更新的value list
        update_value_list = list()
        for update_dict in update_dict_list:
            row_values = [update_dict.get(update_field) for update_field in update_field_list]
            row_values.append(update_dict.get('id'))
            update_value_list.append(row_values)

        condition = Condition(self.table_name).add('id', update_objs[0].id)

        update_sql = f'{update_set_sql} {condition}'
        log.info(f'批量更新[{self.table_name}]语句 ==> {update_sql}')
        log.info(f'批量更新[{self.table_name}]参数 ==> {update_value_list}')
        get_cursor().executemany(update_sql, update_value_list)

    def select_by_order(self, return_type=None, select_cols: Union[SelectCol, str] = None,
                        condition: Union[Condition, str] = None, sort_order='asc'):
        return self.select(return_type, select_cols, condition, order_by='item_order', sort_order=sort_order)

    def select(self, return_type=None, select_cols: Union[SelectCol, str] = None,
               condition: Union[Condition, str] = None, order_by=None, sort_order='asc'):
        """根据条件查询，根据不为空的属性作为条件进行查询"""
        rows = self.select_by_condition(select_cols, condition, order_by, sort_order)
        # 映射为参数对象类
        if not return_type:
            return_type = self.model_type
        return [return_type(**dict(row)) for row in rows]

    def select_one(self, return_type=None, select_cols: Union[SelectCol, str] = None,
                   condition: Union[Condition, str] = None, order_by=None, sort_order='asc'):
        """根据条件查询，根据不为空的属性作为条件进行查询，返回第一条"""
        result = self.select_by_condition(select_cols, condition, order_by, sort_order, fetch_all=False)
        # 映射为参数对象类
        if not return_type:
            return_type = self.model_type
        return return_type(**dict(result)) if result else None

    def select_by_condition(self, select_cols: Union[SelectCol, str] = None,
                            condition: Union[Condition, str] = None,
                            order_by=None, sort_order='asc', fetch_all=True):
        if not select_cols:
            select_cols = SelectCol(self.table_name)
        if not condition:
            condition = Condition(self.table_name)
        return self._do_select(select_cols, condition, condition.params, order_by, sort_order, fetch_all)

    def _do_select(self, select_col_sql, where_clause=None, params=None, order_by=None,
                   sort_order='asc', fetch_all=True):
        """根据条件查询"""
        select_sql = str(select_col_sql)
        if where_clause:
            select_sql += f' {where_clause}'
        if order_by:
            select_sql += f' order by {order_by} {sort_order}'
        log.info(f'查询[{self.table_name}]语句 ==> {select_sql}')
        cursor = get_cursor()
        if params:
            log.info(f'查询[{self.table_name}]参数 ==> {params}')
            cursor.execute(select_sql, params)
        else:
            cursor.execute(select_sql)
        if fetch_all:
            return cursor.fetchall()
        else:
            return cursor.fetchone()

    def filter_illegal_field(self, data):
        # 过滤掉不合法的field
        legal_fields_dict = dict()
        for db_field in get_field_list(self.table_name):
            if hasattr(data, db_field):
                legal_fields_dict[db_field] = getattr(data, db_field)
        return legal_fields_dict

    def get_max_order(self, condition: Condition = None):
        max_order_sql = self._max_order_sql
        log.info(f"查询 {self.table_name} 最大order值语句 ==> {max_order_sql}")
        cursor = get_cursor()
        if condition:
            max_order_sql += f' {condition}'
            log.info(f"查询 {self.table_name} 最大order值参数 ==> {condition.params}")
            cursor.execute(max_order_sql, condition.params)
        else:
            cursor.execute(max_order_sql)
        row = cursor.fetchone()
        return dict(row).get('max_order') + 1
