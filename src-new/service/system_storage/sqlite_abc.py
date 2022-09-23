# -*- coding: utf-8 -*-
import dataclasses
from datetime import datetime
import os

import records
from sqlalchemy.pool import SingletonThreadPool

from constant.constant import SYS_DB_PATH

_author_ = 'luwt'
_date_ = '2022/5/11 10:25'


@dataclasses.dataclass
class BasicSqliteDTO:
    id: int = dataclasses.field(default=None, init=False, compare=False)
    create_time: str = dataclasses.field(default=None, init=False)
    update_time: str = dataclasses.field(default=None, init=False)


class SqliteBasic:

    def __init__(self, table_name, create_table_sql):
        """
        操作sqlite数据库的基类，
        约定：每个表必须有id且为自增主键，
            每个表必须有create_time自动初始化，
            每个表必须有update_time自动更新
        """
        self.db = ...
        self.table_name = table_name
        self._create_table_sql = create_table_sql
        self._create_table()

        # 常用的增删改查sql
        self._id_clause_sql = 'where id = :id'
        self._insert_sql = f'insert into {self.table_name}'
        self._update_sql = f'update {self.table_name} set'
        self._delete_sql = f'delete from {self.table_name} {self._id_clause_sql}'
        self._select_sql = f'select * from {self.table_name}'
        self._select_id_sql = f'select max(id) as id from {self.table_name}'
        print("init-----")

    def _create_table(self):
        if not os.path.exists(SYS_DB_PATH):
            os.makedirs(SYS_DB_PATH)
        db_name = os.path.join(SYS_DB_PATH, f'{self.table_name}_db')
        self.db = records.Database(f'sqlite:///{db_name}',
                                   poolclass=SingletonThreadPool,
                                   connect_args={'check_same_thread': False})
        self.db.query(self._create_table_sql)

    def insert(self, insert_obj: BasicSqliteDTO):
        """新增记录方法，根据约定，id由数据库管理，创建时间、更新时间传入当前时间"""
        insert_obj.create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        insert_obj.update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        insert_dict = dataclasses.asdict(insert_obj)
        if insert_dict:
            insert_dict.pop('id')
            field_str = ", ".join(insert_dict.keys())
            value_placeholder_str = ", ".join(list(map(lambda x: f':{x}', insert_dict.keys())))
            insert_sql = f'{self._insert_sql} ({field_str}) values ({value_placeholder_str})'
            print(insert_sql)
            with self.db.transaction() as tx:
                tx.query(insert_sql, **insert_dict)
                id_record = tx.query(self._select_id_sql).first()
                insert_obj.id = id_record.get("id")

    def delete(self, obj_id):
        self.db.query(self._delete_sql, **{"id": obj_id})

    def update(self, update_obj: BasicSqliteDTO):
        """更新记录方法，根据id更新，创建时间不修改，更新时间传入当前时间"""
        update_obj.update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        update_dict = dataclasses.asdict(update_obj)
        update_dict.pop('create_time')

        # 只更新除id以外不为空的属性
        update_field_list = list(map(lambda x: x[0],
                                     filter(lambda x: x[1] is not None and x[0] != 'id', update_dict.items())))
        if update_field_list:
            update_field_str = ", ".join(list(map(lambda x: f'{x} = :{x}', update_field_list)))
            update_sql = f'{self._update_sql} {update_field_str} {self._id_clause_sql}'
            print(update_sql)

            self.db.query(update_sql, **update_dict)

    def select(self, select_obj):
        """根据条件查询，根据不为空的属性作为条件进行查询"""
        select_sql = self._select_sql
        select_dict = dataclasses.asdict(select_obj)
        select_field_list = list(map(lambda x: x[0], filter(lambda x: x[1] is not None, select_dict.items())))
        if select_field_list:
            select_clause = ' and '.join(list(map(lambda x: f'{x} = :{x}', select_field_list)))
            select_sql = f'{self._select_sql} where {select_clause}'
        print(select_sql)
        rows = self.db.query(select_sql, **select_dict)
        # 映射为参数对象类
        result = list(map(lambda x: select_obj.__class__(**x), rows.all()))
        return result
