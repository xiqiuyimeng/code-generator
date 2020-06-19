# -*- coding: utf-8 -*-
import sqlite3
_author_ = 'luwt'
_date_ = '2020/6/19 19:41'


DB = 'mysql_generator'
SYS_TABLE = ''
CONN_TABLE = 'connection'

conn_sql = {
    'create': f'''create table if not exists {CONN_TABLE}
    (id int primary key not null,
    name char(50) not null,
    host char(20) not null,
    port int not null,
    user char(20) not null,
    pwd char(30) not null
    );''',
    'insert': f'insert into {CONN_TABLE} values ()',
    'update': f'update {CONN_TABLE} set name = "", host = "", port = 3306, user = "", pwd = "" where id = 1',
    'delete': f'delete from {CONN_TABLE} where id = 1',
    'select': f'select * from {CONN_TABLE}',
}
