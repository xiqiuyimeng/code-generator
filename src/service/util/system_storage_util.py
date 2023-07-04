# -*- coding: utf-8 -*-
import os
import sqlite3
import threading
from datetime import datetime
from threading import Lock

from src.constant.constant import SYS_DB_PATH
from src.exception.exception import ThreadStopException
from src.logger.log import logger as log

_author_ = 'luwt'
_date_ = '2023/6/7 14:22'


if not os.path.exists(SYS_DB_PATH):
    os.makedirs(SYS_DB_PATH)
db_name = os.path.join(SYS_DB_PATH, 'generator_db')
# 存放线程id: cursor
thread_id_cursor_dict = dict()
# 存储表字段字典
table_field_dict = dict()
# 批量操作数据库时，参数个数上限
batch_operate_count = 100
# 查询sqlite sequence 的sql
sqlite_sequence_sql = 'select * from sqlite_sequence'
# 查询表结构字段sql
field_list_sql = 'PRAGMA table_info("{}")'
# sqlite连接是否正在使用，如果在使用，那么其他线程需要等待
conn_in_use = False
# 在获取游标的时候，加锁
lock = Lock()

# 创建一个全局的连接，操作本地数据库只使用一个连接，避免多连接并发造成sqlite锁定的问题
conn = sqlite3.connect(db_name, check_same_thread=False)
# 将查询结果转为行对象，可以使用 dict 将结果直接转为字典对象
conn.row_factory = sqlite3.Row


def set_conn_in_use(in_use):
    global conn_in_use
    conn_in_use = in_use


def allow_thread_running():
    key = f'{threading.get_ident()}-terminate'
    if key in thread_id_cursor_dict:
        del thread_id_cursor_dict[key]
        raise ThreadStopException('线程结束')


def set_thread_terminate(thread_id, thread_terminate):
    thread_id_cursor_dict[f'{thread_id}-terminate'] = thread_terminate


def get_db_cursor():
    while conn_in_use:
        log.info("连接被其他线程占用，需要等待")
        pass
    with lock:
        set_conn_in_use(True)
        cursor = conn.cursor()
        # 放入缓存
        thread_id_cursor_dict[threading.get_ident()] = cursor
        return cursor


def get_cursor():
    # 首先检查是否可以继续执行
    allow_thread_running()
    # 如果从缓存中取不到，则获取一个新的对象
    current_thread_cursor = thread_id_cursor_dict.get(threading.get_ident())
    return current_thread_cursor if current_thread_cursor else get_db_cursor()


def release_connection():
    """释放当前线程使用的连接"""
    thread_id = threading.get_ident()
    if thread_id in thread_id_cursor_dict:
        current_thread_cursor = thread_id_cursor_dict.pop(thread_id)
        current_thread_cursor.connection.commit()
        set_conn_in_use(False)


def close_conn():
    conn.close()


def transactional(func):
    def do_transaction(*args, **kwargs):
        # 获取 游标
        cursor = get_cursor()
        # 判断当前连接是否处在事务中
        # 如果已经在事务中，直接使用，事务的控制交由外层事务控制
        if cursor.connection.in_transaction:
            func_result = func(*args, **kwargs)
            return func_result
        else:
            # 连接如果不在事务中，那么可以直接开启事务
            cursor.execute('begin')
            try:
                func_result = func(*args, **kwargs)
                conn.commit()
                return func_result
            except Exception as e:
                conn.rollback()
                log.exception("操作本地数据库事务错误：", e)
                raise e

    return do_transaction


def batch_operate(batch_func):
    def do_batch_operate(cls_obj, batch_params):
        # 如果批量操作数量过多，应该分批来执行，每批100个元素
        if len(batch_params) > batch_operate_count:
            start, end = 0, batch_operate_count
            while start < len(batch_params):
                batch_func(cls_obj, batch_params[start: end])
                start += batch_operate_count
                end += batch_operate_count
        else:
            batch_func(cls_obj, batch_params)

    return do_batch_operate


def get_sqlite_sequence():
    cursor = get_cursor()
    cursor.execute(sqlite_sequence_sql)
    return cursor.fetchall()


def get_now_str():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_field_list(table_name):
    field_list = table_field_dict.get(table_name)
    if not field_list:
        cursor = get_cursor()
        cursor.execute(field_list_sql.format(table_name))
        field_list = [dict(row).get('name') for row in cursor.fetchall()]
        table_field_dict[table_name] = field_list
    return field_list


def update_table_field_dict(table_name):
    if table_name in table_field_dict:
        del table_field_dict[table_name]
    get_field_list(table_name)


class Condition:

    def __init__(self, table_name):
        self.col_list = get_field_list(table_name)
        self.condition_list = list()
        self.params = list()

    def add(self, col, param, operator='eq'):
        if col in self.col_list:
            if operator == 'eq':
                self._add_eq_condition(col, param)
            elif operator == 'in':
                self._add_in_condition(col, param)
        return self

    def _add_eq_condition(self, col, param):
        self.condition_list.append(f'{col} = ?')
        self.params.append(param)

    def _add_in_condition(self, col, params):
        if len(params):
            self.condition_list.append(f'{col} in ({", ".join("?" * len(params))})')
            self.params.extend(params)

    def __str__(self):
        if self.condition_list:
            return f'where {" and ".join(self.condition_list)}'

    def __bool__(self):
        return bool(self.condition_list)


class SelectCol:

    def __init__(self, table_name):
        self.table_name = table_name
        self.col_list = get_field_list(table_name)
        self.select_cols = list()

    def add(self, col):
        if col in self.col_list:
            self.select_cols.append(col)
        return self

    def __str__(self):
        select_cols = self.col_list
        if self.select_cols:
            select_cols = self.select_cols
        return f'select {", ".join(select_cols)} from {self.table_name}'
