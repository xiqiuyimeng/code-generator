# -*- coding: utf-8 -*-
import os
import sqlite3
from collections import namedtuple

from src.sys.sys_info_storage.sqlite_abc import SqliteBasic

_author_ = 'luwt'
_date_ = '2020/9/15 11:03'


# 模板对象：id，模板名称，java模板java_tp, mapper模板mapper_tp, xml模板xml_tp,
# service模板service_tp, service_impl模板service_impl_tp, controller模板controller_tp
# 类型：0 内置，1 自定义。使用次数，可根据次数排序, is_using：是否在使用中，0否 1是
Template = namedtuple('Template', 'id tp_name java_tp mapper_tp xml_tp service_tp '
                                  'service_impl_tp controller_tp type use_times is_using')


template_sql = {
    'create': '''create table if not exists template (
    id integer primary key autoincrement,
    tp_name char(50) not null,
    java_tp blob not null,
    mapper_tp text not null,
    xml_tp text not null,
    service_tp text not null,
    service_impl_tp text not null,
    controller_tp text not null,
    type integer not null,
    use_times integer not null,
    is_using integer not null
    );''',
    'insert': 'insert into template ',
    'delete': 'delete from template where id = ?',
    'update_selective': 'update template set ',
    'select': 'select * from template',
    'select_name_exist': 'select count(*) > 0 from template where tp_name = ?'
}


class TemplateSqlite(SqliteBasic):

    def __new__(cls, *args, **kwargs):
        # 控制单例，只连接一次库，避免多次无用的连接
        if not hasattr(TemplateSqlite, 'instance'):
            TemplateSqlite.instance = object.__new__(cls)
            if not os.path.exists(os.path.dirname(__file__)):
                os.makedirs(os.path.dirname(__file__))
            db = os.path.dirname(__file__) + '/' + 'template_db'
            TemplateSqlite.instance.conn = sqlite3.connect(db, check_same_thread=False)
            TemplateSqlite.instance.cursor = TemplateSqlite.instance.conn.cursor()
            TemplateSqlite.instance.cursor.execute(template_sql.get('create'))
        return TemplateSqlite.instance

    def __init__(self):
        super().__init__(template_sql, self.conn, self.cursor)

    def get_templates(self, tp_type=None):
        sql = template_sql.get('select')
        if tp_type is not None:
            sql += f' where type = {tp_type}'
        self.cursor.execute(sql + ' order by use_times desc')
        data = self.cursor.fetchall()
        result = list()
        [result.append(Template(*row)) for row in data]
        return result

    def init_template(self, template_dict):
        template = self.get_templates(tp_type=0)
        if not template:
            template_dict['id'] = None
            template_dict['tp_name'] = '默认模板'
            template_dict['type'] = 0
            template_dict['use_times'] = 0
            template_dict['is_using'] = 1
            default_template = Template(**template_dict)
            self.insert(default_template)

    def check_tp_name_available(self, tp_id, tp_name):
        sql = template_sql.get('select_name_exists')
        if tp_id:
            sql += f' and id != {tp_id}'
        self.cursor.execute(sql, (tp_name, ))
        data = self.cursor.fetchone()
        return data[0] == 0

    def get_template(self, tp_id):
        sql = template_sql.get('select') + f' where id = {tp_id}'
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        return Template(*data)

    def get_using_template(self):
        sql = template_sql.get('select') + f' where is_using = 1'
        self.cursor.execute(sql)
        # 理论上只有一个正在使用中
        data = self.cursor.fetchone()
        return Template(*data)
