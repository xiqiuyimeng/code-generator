# -*- coding: utf-8 -*-
import os
import sqlite3
from collections import namedtuple

from src.sys.sys_info_storage.sqlite_abc import SqliteBasic

_author_ = 'luwt'
_date_ = '2020/6/19 19:41'


Connection = namedtuple('Connection', 'id name host port user pwd')


# 使用占位符的形式，避免特殊字符转义问题
conn_sql = {
    'create': '''create table if not exists connection
    (id integer PRIMARY KEY autoincrement,
    name char(50) not null,
    host char(20) not null,
    port int not null,
    user char(20) not null,
    pwd char(30) not null
    );''',
    'insert': 'insert into connection ',
    'update_selective': 'update connection set ',
    'delete': 'delete from connection where id = ?',
    'select': 'select * from connection',
    'select_name_exist': 'select count(*) > 0 from connection where name = ?',
    'select_id_by_name': 'select id from connection where name = ?',
}


class ConnSqlite(SqliteBasic):

    def __new__(cls, *args, **kwargs):
        # 控制单例，只连接一次库，避免多次无用的连接
        if not hasattr(ConnSqlite, 'instance'):
            ConnSqlite.instance = object.__new__(cls)
            if not os.path.exists(os.path.dirname(__file__)):
                os.makedirs(os.path.dirname(__file__))
            db = os.path.dirname(__file__) + '/' + 'conn_db'
            ConnSqlite.instance.conn = sqlite3.connect(db, check_same_thread=False)
            ConnSqlite.instance.cursor = ConnSqlite.instance.conn.cursor()
            ConnSqlite.instance.cursor.execute(conn_sql.get('create'))
        return ConnSqlite.instance

    def __init__(self):
        super().__init__(conn_sql, self.conn, self.cursor)

    def select_all(self):
        self.cursor.execute(conn_sql.get('select'))
        data = self.cursor.fetchall()
        result = list()
        [result.append(Connection(*row)) for row in data]
        return result

    def select_one(self, conn_id):
        sql = conn_sql.get('select') + ' where id = ?'
        self.cursor.execute(sql, (conn_id,))
        data = self.cursor.fetchone()
        return Connection(*data)

    def select_latest_one(self):
        sql = conn_sql.get('select') + ' order by id desc limit 1'
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        return Connection(*data)

    def get_id_by_name(self, conn_name):
        """根据连接名称查询id，连接名称是唯一的，所以可以这样查"""
        sql = conn_sql.get('select_id_by_name')
        self.cursor.execute(sql, (conn_name, ))
        data = self.cursor.fetchone()
        return data[0]

    def check_name_available(self, conn_id, conn_name):
        """检查连接名称是否可用，名称必须唯一"""
        sql = conn_sql.get('select_name_exist')
        if conn_id:
            sql += f' and id != {conn_id}'
        self.cursor.execute(sql, (conn_name, ))
        data = self.cursor.fetchone()
        return data[0] == 0

