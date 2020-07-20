# -*- coding: utf-8 -*-
import os
from collections import namedtuple
import sqlite3
_author_ = 'luwt'
_date_ = '2020/6/19 19:41'


Connection = namedtuple('Connection', 'id name host port user pwd')


DB = os.path.dirname(__file__) + '/mysql_generator'
SYS_TABLE = ''
CONN_TABLE = 'connection'

conn_sql = {
    'create': f'''create table if not exists {CONN_TABLE}
    (id integer PRIMARY KEY autoincrement,
    name char(50) not null,
    host char(20) not null,
    port int not null,
    user char(20) not null,
    pwd char(30) not null
    );''',
    'insert': f'insert into {CONN_TABLE}(name, host, port, user, pwd)',
    'update': f'update {CONN_TABLE} ',
    'delete': f'delete from {CONN_TABLE} where id = ',
    'select': f'select * from {CONN_TABLE}',
    'select_name_exist': f'select count(*) > 0 from {CONN_TABLE} where name = ',
    'select_id_by_name': f'select id from {CONN_TABLE} where name = ',
}

conn = sqlite3.connect(DB, check_same_thread=False)
cursor = conn.cursor()
cursor.execute(conn_sql.get('create'))


def add_conn(connection):
    values = f' values("{connection.name}", "{connection.host}",' \
             f' {connection.port}, "{connection.user}", "{connection.pwd}")'
    sql = conn_sql.get('insert') + values
    cursor.execute(sql)
    conn.commit()


def delete_conn(conn_id):
    sql = conn_sql.get('delete') + f'{conn_id}'
    cursor.execute(sql)
    conn.commit()


def update_conn(connection):
    set_sql = f' set name = "{connection.name}",' \
              f'host = "{connection.host}", ' \
              f'port = {connection.port}, ' \
              f'user = "{connection.user}", ' \
              f'pwd = "{connection.pwd}"' \
              f'where id = {connection.id}'
    sql = conn_sql.get('update') + set_sql
    cursor.execute(sql)
    conn.commit()


def get_conns():
    cursor.execute(conn_sql.get('select'))
    data = cursor.fetchall()
    result = list()
    for row in data:
        result.append(Connection(*row))
    return result


def get_conn(conn_id):
    sql = conn_sql.get('select') + f' where id = {conn_id}'
    cursor.execute(sql)
    data = cursor.fetchone()
    return Connection(*data)


def get_new_conn():
    sql = conn_sql.get('select') + ' order by id desc limit 1'
    cursor.execute(sql)
    data = cursor.fetchone()
    return Connection(*data)


def check_name_available(conn_name):
    """检查连接名称是否可用，名称必须唯一"""
    sql = conn_sql.get('select_name_exist') + f'"{conn_name}"'
    cursor.execute(sql)
    data = cursor.fetchone()
    return data[0] == 0


def get_id_by_name(conn_name):
    """根据连接名称查询id，连接名称是唯一的，所以可以这样查"""
    sql = conn_sql.get('select_id_by_name') + f'"{conn_name}"'
    cursor.execute(sql)
    data = cursor.fetchone()
    return data[0]

