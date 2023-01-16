# -*- coding: utf-8 -*-
import os
import threading
from dataclasses import dataclass, field
from datetime import datetime

import records
from sqlalchemy.pool import SingletonThreadPool

from constant.constant import SYS_DB_PATH
from exception.exception import ThreadStopException
from logger.log import logger as log

_author_ = 'luwt'
_date_ = '2022/5/11 10:25'

db_name = os.path.join(SYS_DB_PATH, f'generator_db')
table_field_dict = dict()
thread_id_db_dict = dict()
# 批量操作数据库时，参数个数上限
batch_operate_count = 100


@dataclass
class BasicSqliteDTO:
    id: int = field(default=None, init=False, compare=False)
    item_order: int = field(init=False, default=None, compare=False)
    create_time: str = field(default=None, init=False, compare=False)
    update_time: str = field(default=None, init=False, compare=False)


def get_db():
    if not os.path.exists(SYS_DB_PATH):
        os.makedirs(SYS_DB_PATH)
    db = records.Database(f'sqlite:///{db_name}',
                          poolclass=SingletonThreadPool,
                          connect_args={'check_same_thread': False})
    # 放入缓存
    thread_id_db_dict[threading.get_ident()] = db
    return db


def transactional(f):
    def do_transaction(*args, **kw):
        thread_id = threading.get_ident()
        # 获取db_conn
        db_conn = get_db_conn()
        # 如果是 Database 对象，那么证明前面没有事务，获取连接，替换缓存中的 Database 对象，
        # 如果不是 Database 对象，说明是 Connection 对象，那么应该已经处于事务中，直接使用即可
        if isinstance(db_conn, records.Database):
            cache_db, allow_close_conn = True, True
            new_db = get_db()
            conn = new_db.get_connection()
            # 放入缓存
            thread_id_db_dict[thread_id] = conn
        else:
            conn = db_conn
            cache_db, allow_close_conn = False, False
        # 开启事务
        tx = conn.transaction()
        try:
            func_result = f(*args, **kw)
            tx.commit()
            return func_result
        except Exception as e:
            tx.rollback()
            log.exception("操作本地数据库事务错误：", e)
            raise e
        finally:
            if cache_db:
                # 将原来的 Database 对象重新放回去
                thread_id_db_dict[thread_id] = db_conn
            if allow_close_conn:
                # 关闭当前事务创建的连接
                conn.close()
    return do_transaction


def allow_thread_running():
    if thread_id_db_dict.get(f'{threading.get_ident()}-terminate'):
        raise ThreadStopException('线程结束')


def set_thread_terminate(thread_id, thread_terminate):
    thread_id_db_dict[f'{thread_id}-terminate'] = thread_terminate


def get_db_conn():
    # 首先检查是否可以继续执行
    allow_thread_running()
    # 如果从缓存中取不到，则获取一个新的对象
    current_thread_db = thread_id_db_dict.get(threading.get_ident())
    return current_thread_db if current_thread_db else get_db()


def batch_operate(batch_params, batch_func):
    # 如果批量操作数量过多，应该分批来执行，每批100个元素
    if len(batch_params) > batch_operate_count:
        start, end = 0, batch_operate_count
        while start < len(batch_params):
            batch_func(batch_params[start: end])
            start += batch_operate_count
            end += batch_operate_count
    else:
        batch_func(batch_params)


class SqliteBasic:

    def __init__(self, table_name, sql_dict):
        """
        操作sqlite数据库的基类，
        约定：每个表必须有id且为自增主键，
            每个表必须有create_time自动初始化，
            每个表必须有update_time自动更新，
            每个表应该有item_order，描述顺序关系
        """
        self.table_name = table_name
        self._create_table_sql = sql_dict.get('create')
        self._create_table()

        # 常用的增删改查sql
        self._id_clause_sql = 'where id = :id'
        self._insert_sql = f'insert into {self.table_name}'
        self._update_sql = f'update {self.table_name} set'
        self._delete_sql = f'delete from {self.table_name} {self._id_clause_sql}'
        self._select_sql = f'select * from {self.table_name}'
        self._select_count_sql = f'select count(*) as count from {self.table_name}'
        self._field_list_sql = f'PRAGMA table_info("{self.table_name}")'
        self._max_order_sql = f'select ifnull(max(item_order), 0) as max_order from {self.table_name}'

    def _create_table(self):
        get_db_conn().query(self._create_table_sql)

    def get_field_list(self):
        field_list = table_field_dict.get(self.table_name)
        if not field_list:
            rows = get_db_conn().query(self._field_list_sql)
            field_list = list(map(lambda x: x.name, rows.all()))
            table_field_dict[self.table_name] = field_list
        return field_list

    def insert(self, insert_obj: BasicSqliteDTO):
        """新增记录方法，根据约定，id由数据库管理，创建时间、更新时间传入当前时间"""
        insert_obj.create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        insert_obj.update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 过滤掉不合法的field
        insert_dict = self.filter_illegal_field(insert_obj)
        if insert_dict:
            insert_dict.pop('id')

            field_str = ", ".join(insert_dict.keys())
            value_placeholder_str = ", ".join(list(map(lambda x: f':{x}', insert_dict.keys())))
            insert_sql = f'{self._insert_sql} ({field_str}) values ({value_placeholder_str})'
            log.info(f'插入[{self.table_name}]语句 ==> {insert_sql}')
            log.info(f'插入[{self.table_name}]参数 ==> {insert_dict}')

            get_db_conn().query(insert_sql, **insert_dict)
            # 查询id
            id_record = self.select(insert_obj)[0]
            insert_obj.id = id_record.id

    def batch_insert(self, insert_objs):
        batch_operate(insert_objs, self._batch_insert)

    def _batch_insert(self, insert_objs):
        """批量插入"""
        for insert_obj in insert_objs:
            insert_obj.create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            insert_obj.update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        insert_dict_list = list(map(lambda x: self.filter_illegal_field(x), insert_objs))

        for insert_dict in insert_dict_list:
            insert_dict.pop('id')

        field_str = ", ".join(insert_dict_list[0].keys())
        value_placeholder_str = ", ".join(list(map(lambda x: f':{x}', insert_dict_list[0].keys())))
        insert_sql = f'{self._insert_sql} ({field_str}) values ({value_placeholder_str})'
        log.info(f'批量插入[{self.table_name}]语句 ==> {insert_sql}')
        log.info(f'批量插入[{self.table_name}]参数 ==> {insert_dict_list}')

        get_db_conn().bulk_query(insert_sql, insert_dict_list)
        # 查询id
        for insert_obj in insert_objs:
            id_record = self.select(insert_obj)[0]
            insert_obj.id = id_record.id

    def delete(self, obj_id):
        log.info(f'删除[{self.table_name}]语句 ==> {self._delete_sql}')
        log.info(f'删除[{self.table_name}]参数 ==> {obj_id}')
        get_db_conn().query(self._delete_sql, **{"id": obj_id})

    def batch_delete(self, obj_ids):
        batch_operate(obj_ids, self._batch_delete)

    def _batch_delete(self, obj_ids):
        log.info(f'批量删除[{self.table_name}]语句 ==> {self._delete_sql}')
        log.info(f'批量删除[{self.table_name}]参数 ==> {obj_ids}')
        get_db_conn().bulk_query(self._delete_sql, list(map(lambda x: {'id': x}, obj_ids)))

    def update(self, update_obj: BasicSqliteDTO):
        """更新记录方法，根据id更新，创建时间不修改，更新时间传入当前时间"""
        update_obj.update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        update_dict = self.filter_illegal_field(update_obj)
        update_dict.pop('create_time')

        # 只更新除id以外不为空的属性
        update_field_list = list(map(lambda x: x[0],
                                     filter(lambda x: x[1] is not None and x[0] != 'id', update_dict.items())))

        # 收集更新的value dict
        update_val_dict = {"id": update_dict.get("id")}
        for update_field in update_field_list:
            update_val_dict[update_field] = update_dict.get(update_field)

        if update_field_list:
            update_field_str = ", ".join(list(map(lambda x: f'{x} = :{x}', update_field_list)))
            update_sql = f'{self._update_sql} {update_field_str} {self._id_clause_sql}'
            log.info(f'更新[{self.table_name}]语句 ==> {update_sql}')
            log.info(f'更新[{self.table_name}]参数 ==> {update_val_dict}')

            get_db_conn().query(update_sql, **update_val_dict)

    def batch_update(self, update_objs):
        batch_operate(update_objs, self._batch_update)

    def _batch_update(self, update_objs):
        """批量更新"""
        update_dict_list = list()
        for update_obj in update_objs:
            update_obj.update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            update_dict = self.filter_illegal_field(update_obj)
            update_dict.pop('create_time')
            update_dict_list.append(update_dict)

        # 只更新除id以外不为空的属性
        update_field_list = list(map(lambda x: x[0],
                                     filter(lambda x: x[1] is not None and x[0] != 'id', update_dict_list[0].items())))

        # 收集value list
        update_value_list = list()
        for update_obj_dict in update_dict_list:
            update_val_dict = {"id": update_obj_dict.get("id")}
            for update_field in update_field_list:
                update_val_dict[update_field] = update_obj_dict.get(update_field)
            update_value_list.append(update_val_dict)

        if update_field_list:
            update_field_str = ", ".join(list(map(lambda x: f'{x} = :{x}', update_field_list)))
            update_sql = f'{self._update_sql} {update_field_str} {self._id_clause_sql}'
            log.info(f'批量更新[{self.table_name}]语句 ==> {update_sql}')
            log.info(f'批量更新[{self.table_name}]参数 ==> {update_value_list}')

            get_db_conn().bulk_query(update_sql, update_value_list)

    def select_by_order(self, select_obj, sort_order='asc'):
        return self.select(select_obj, order_by='item_order', sort_order=sort_order)

    def select(self, select_obj, order_by=None, sort_order='asc'):
        """根据条件查询，根据不为空的属性作为条件进行查询"""
        rows = self._do_select(self._select_sql, select_obj, order_by, sort_order)
        # 映射为参数对象类
        return list(map(lambda x: select_obj.__class__(**x), rows.all()))

    def select_count(self, select_obj, order_by=None, sort_order='asc'):
        """根据条件查询，查询存在的记录数量"""
        rows = self._do_select(self._select_count_sql, select_obj, order_by, sort_order)
        return rows.first().as_dict().get('count')

    def _do_select(self, sql, select_obj, order_by=None, sort_order='asc'):
        """根据条件查询，查询存在的记录数量"""
        select_sql = sql
        # 过滤掉不合法的field
        select_dict = self.filter_illegal_field(select_obj)

        select_field_list = list(map(lambda x: x[0], filter(lambda x: x[1] is not None, select_dict.items())))
        select_value_dict = dict()
        if select_field_list:
            select_clause = ' and '.join(list(map(lambda x: f'{x} = :{x}', select_field_list)))
            select_sql = f'{sql} where {select_clause}'
            # 收集查询value
            for select_field in select_field_list:
                select_value_dict[select_field] = select_dict[select_field]

        if order_by:
            select_sql = f'{select_sql} order by {order_by} {sort_order}'

        log.info(f'查询[{self.table_name}]语句 ==> {select_sql}')
        log.info(f'查询[{self.table_name}]参数 ==> {select_value_dict}')
        return get_db_conn().query(select_sql, **select_value_dict)

    def filter_illegal_field(self, data):
        # 过滤掉不合法的field
        legal_fields_dict = dict()
        for db_field in self.get_field_list():
            if hasattr(data, db_field):
                legal_fields_dict[db_field] = getattr(data, db_field)
        return legal_fields_dict

    def get_max_order(self, condition_dict=None):
        max_order_sql = self._max_order_sql
        if condition_dict:
            clause_list = list()
            for key in condition_dict.keys():
                clause_list.append(f'{key} = :{key}')
            max_order_sql = f'{max_order_sql} where {" and ".join(clause_list)}'
            db_record = get_db_conn().query(max_order_sql, **condition_dict)
        else:
            db_record = get_db_conn().query(max_order_sql)
        log.info(f"查询 {self.table_name} 最大order值语句 ==> {max_order_sql}")
        log.info(f"查询 {self.table_name} 最大order值参数 ==> {condition_dict}")
        return db_record.first().max_order + 1
