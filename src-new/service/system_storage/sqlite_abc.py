# -*- coding: utf-8 -*-
import dataclasses
from datetime import datetime
import os

import records
from sqlalchemy.pool import SingletonThreadPool

from constant.constant import SYS_DB_PATH
from logger.log import logger as log

_author_ = 'luwt'
_date_ = '2022/5/11 10:25'


table_field_dict = dict()


@dataclasses.dataclass
class BasicSqliteDTO:
    id: int = dataclasses.field(default=None, init=False, compare=False)
    create_time: str = dataclasses.field(default=None, init=False, compare=False)
    update_time: str = dataclasses.field(default=None, init=False, compare=False)


class SqliteBasic:

    def __init__(self, table_name, create_table_sql):
        """
        操作sqlite数据库的基类，
        约定：每个表必须有id且为自增主键，
            每个表必须有create_time自动初始化，
            每个表必须有update_time自动更新
        """
        self.db: records.Database = ...
        self.table_name = table_name
        self._create_table_sql = create_table_sql
        self._create_table()

        # 常用的增删改查sql
        self._id_clause_sql = 'where id = :id'
        self._insert_sql = f'insert into {self.table_name}'
        self._update_sql = f'update {self.table_name} set'
        self._delete_sql = f'delete from {self.table_name} {self._id_clause_sql}'
        self._select_sql = f'select * from {self.table_name}'
        self._select_count_sql = f'select count(*) as count from {self.table_name}'
        self._select_id_sql = f'select max(id) as id from {self.table_name}'
        self._field_list_sql = f'PRAGMA table_info("{self.table_name}")'

    def _create_table(self):
        if not os.path.exists(SYS_DB_PATH):
            os.makedirs(SYS_DB_PATH)
        db_name = os.path.join(SYS_DB_PATH, f'{self.table_name}_db')
        self.db = records.Database(f'sqlite:///{db_name}',
                                   poolclass=SingletonThreadPool,
                                   connect_args={'check_same_thread': False})
        self.db.query(self._create_table_sql)

    def get_field_list(self):
        field_list = table_field_dict.get(self.table_name)
        if not field_list:
            rows = self.db.query(self._field_list_sql)
            field_list = list(map(lambda x: x.name, rows.all()))
            table_field_dict[self.table_name] = field_list
        return field_list

    def insert(self, insert_obj: BasicSqliteDTO):
        """新增记录方法，根据约定，id由数据库管理，创建时间、更新时间传入当前时间"""
        insert_obj.create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        insert_obj.update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        insert_dict = dataclasses.asdict(insert_obj)
        if insert_dict:
            insert_dict.pop('id')

            # 过滤掉不合法的field
            self.filter_illegal_field(insert_dict)

            field_str = ", ".join(insert_dict.keys())
            value_placeholder_str = ", ".join(list(map(lambda x: f':{x}', insert_dict.keys())))
            insert_sql = f'{self._insert_sql} ({field_str}) values ({value_placeholder_str})'
            log.info(f'插入[{self.table_name}]语句 ==> {insert_sql}')
            log.info(f'插入[{self.table_name}]参数 ==> {insert_dict}')
            with self.db.transaction() as tx:
                tx.query(insert_sql, **insert_dict)
                id_record = tx.query(self._select_id_sql).first()
                insert_obj.id = id_record.get("id")

    def batch_insert(self, insert_objs):
        """批量插入"""
        for insert_obj in insert_objs:
            insert_obj.create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            insert_obj.update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        insert_dict_list = list(map(lambda x: dataclasses.asdict(x), insert_objs))

        for insert_dict in insert_dict_list:
            insert_dict.pop('id')
            # 过滤掉不合法的field
            self.filter_illegal_field(insert_dict)

        field_str = ", ".join(insert_dict_list[0].keys())
        value_placeholder_str = ", ".join(list(map(lambda x: f':{x}', insert_dict_list[0].keys())))
        insert_sql = f'{self._insert_sql} ({field_str}) values ({value_placeholder_str})'
        log.info(f'批量插入[{self.table_name}]语句 ==> {insert_sql}')
        log.info(f'批量插入[{self.table_name}]参数 ==> {insert_dict_list}')
        with self.db.transaction() as tx:
            tx.bulk_query(insert_sql, insert_dict_list)

    def delete(self, obj_id):
        log.info(f'删除[{self.table_name}]语句 ==> {self._delete_sql}')
        log.info(f'删除[{self.table_name}]参数 ==> {obj_id}')
        self.db.query(self._delete_sql, **{"id": obj_id})

    def update(self, update_obj: BasicSqliteDTO):
        """更新记录方法，根据id更新，创建时间不修改，更新时间传入当前时间"""
        update_obj.update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        update_dict = dataclasses.asdict(update_obj)
        update_dict.pop('create_time')

        # 过滤掉不合法的field
        self.filter_illegal_field(update_dict)

        # 只更新除id以外不为空的属性
        update_field_list = list(map(lambda x: x[0],
                                     filter(lambda x: x[1] is not None and x[0] != 'id', update_dict.items())))

        # 收集更新的value dict
        update_val_dict = {"id": update_dict.get("id")}
        for field in update_field_list:
            update_val_dict[field] = update_dict.get(field)

        if update_field_list:
            update_field_str = ", ".join(list(map(lambda x: f'{x} = :{x}', update_field_list)))
            update_sql = f'{self._update_sql} {update_field_str} {self._id_clause_sql}'
            log.info(f'更新[{self.table_name}]语句 ==> {update_sql}')
            log.info(f'更新[{self.table_name}]参数 ==> {update_val_dict}')

            self.db.query(update_sql, **update_val_dict)

    def batch_update(self, update_objs):
        """批量更新"""
        update_dict_list = list()
        for update_obj in update_objs:
            update_obj.update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            update_dict = dataclasses.asdict(update_obj)
            update_dict.pop('create_time')
            update_dict_list.append(update_dict)

            # 过滤掉不合法的field
            self.filter_illegal_field(update_dict)
        # 只更新除id以外不为空的属性
        update_field_list = list(map(lambda x: x[0],
                                     filter(lambda x: x[1] is not None and x[0] != 'id', update_dict_list[0].items())))

        # 收集value list
        update_value_list = list()
        for update_obj_dict in update_dict_list:
            update_val_dict = {"id": update_obj_dict.get("id")}
            for field in update_field_list:
                update_val_dict[field] = update_obj_dict.get(field)
            update_value_list.append(update_val_dict)

        if update_field_list:
            update_field_str = ", ".join(list(map(lambda x: f'{x} = :{x}', update_field_list)))
            update_sql = f'{self._update_sql} {update_field_str} {self._id_clause_sql}'
            log.info(f'批量更新[{self.table_name}]语句 ==> {update_sql}')
            log.info(f'批量更新[{self.table_name}]参数 ==> {update_value_list}')

            self.db.bulk_query(update_sql, update_value_list)

    def select(self, select_obj):
        """根据条件查询，根据不为空的属性作为条件进行查询"""
        rows = self._do_select(self._select_sql, select_obj)
        # 映射为参数对象类
        result = list(map(lambda x: select_obj.__class__(**x), rows.all()))
        return result

    def select_count(self, select_obj):
        """根据条件查询，查询存在的记录数量"""
        rows = self._do_select(self._select_count_sql, select_obj)
        return rows.first().as_dict().get('count')

    def _do_select(self, sql, select_obj):
        """根据条件查询，查询存在的记录数量"""
        select_sql = sql
        select_dict = dataclasses.asdict(select_obj)

        # 过滤掉不合法的field
        self.filter_illegal_field(select_dict)

        select_field_list = list(map(lambda x: x[0], filter(lambda x: x[1] is not None, select_dict.items())))
        select_value_dict = dict()
        if select_field_list:
            select_clause = ' and '.join(list(map(lambda x: f'{x} = :{x}', select_field_list)))
            select_sql = f'{sql} where {select_clause}'
            # 收集查询value
            for select_field in select_field_list:
                select_value_dict[select_field] = select_dict[select_field]

        log.info(f'查询[{self.table_name}]语句 ==> {select_sql}')
        log.info(f'查询[{self.table_name}]参数 ==> {select_value_dict}')
        return self.db.query(select_sql, **select_value_dict)

    def filter_illegal_field(self, operation_dict):
        # 过滤掉不合法的field
        illegal_field_list = operation_dict.keys() - self.get_field_list()
        [operation_dict.pop(k) for k in illegal_field_list]
