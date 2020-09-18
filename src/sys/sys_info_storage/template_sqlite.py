# -*- coding: utf-8 -*-
import os
import sqlite3
from collections import namedtuple
from datetime import datetime

from src.sys.sys_info_storage.sqlite_abc import SqliteBasic

_author_ = 'luwt'
_date_ = '2020/9/15 11:03'


# 模板对象：id，模板名称，java模板java_tp, mapper模板mapper_tp, xml模板xml_tp,
# service模板service_tp, service_impl模板service_impl_tp, controller模板controller_tp
# 类型：0 内置，1 自定义。使用次数，可根据次数排序, is_using：是否在使用中，0否 1是
# 创建时间 更新时间，时间都以时间戳形式存储，取出后再转为格式化字符串。模板说明
Template = namedtuple('Template', 'id tp_name java_tp mapper_tp xml_tp service_tp '
                                  'service_impl_tp controller_tp type use_times is_using '
                                  'create_time update_time comment')


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
    is_using integer not null,
    create_time integer not null,
    update_time integer not null,
    comment text not null
    );''',
    'insert': 'insert into template ',
    'delete': 'delete from template where id = ?',
    'update_selective': 'update template set ',
    'select': 'select * from template',
    'select_templates': 'select tp_name, case type when 0 then "系统内置" when 1 then "自定义" end as type , '
                        'use_times, case is_using when 0 then "否" when 1 then "是" end as is_using, '
                        'create_time, update_time, comment from template',
    'select_name_exist': 'select count(*) > 0 from template where tp_name = ?'
}


def template_factory(cursor, row):
    """自定义返回形式的方法"""
    result = dict()
    # cursor.description，数据结构为关于列的二维数组：(('id', None, None, None, None, None, None),)
    # row 为查到的数据，元祖形式，取col的第一列即为字段名称，对应row中的数据，可组成template返回
    for i, col in enumerate(cursor.description):
        # 时间类型格式化字符串再返回
        if col[0] in ('create_time', 'update_time'):
            data = datetime.fromtimestamp(row[i]).strftime('%Y-%m-%d %H:%M:%S')
        else:
            data = row[i]
        result[col[0]] = data
    # 初始化一个空的template字典
    template_dict = Template(*((None,) * len(Template._fields)))._asdict()
    # 将有值的部分进行更新
    template_dict.update(result)
    # 转化为template类型返回
    return Template(**template_dict)


class TemplateSqlite(SqliteBasic):

    def __new__(cls, *args, **kwargs):
        # 控制单例，只连接一次库，避免多次无用的连接
        if not hasattr(TemplateSqlite, 'instance'):
            TemplateSqlite.instance = object.__new__(cls)
            if not os.path.exists(os.path.dirname(__file__)):
                os.makedirs(os.path.dirname(__file__))
            db = os.path.dirname(__file__) + '/' + 'template_db'
            TemplateSqlite.instance.conn = sqlite3.connect(db, check_same_thread=False)
            # 注册自定义返回形式方法
            TemplateSqlite.instance.conn.row_factory = template_factory
            TemplateSqlite.instance.cursor = TemplateSqlite.instance.conn.cursor()
            TemplateSqlite.instance.cursor.execute(template_sql.get('create'))
        return TemplateSqlite.instance

    def __init__(self):
        super().__init__(template_sql, self.conn, self.cursor)

    def get_templates(self, tp_type=None):
        sql = template_sql.get('select_templates')
        if tp_type is not None:
            sql += f' where type = {tp_type}'
        self.cursor.execute(sql + ' order by use_times desc')
        return self.cursor.fetchall()

    def init_template(self, template_dict):
        template = self.get_templates(tp_type=0)
        if not template:
            template_dict['id'] = None
            template_dict['tp_name'] = '默认模板'
            template_dict['type'] = 0
            template_dict['use_times'] = 0
            template_dict['is_using'] = 1
            now = round(datetime.now().timestamp())
            # 时间以时间戳形式存储
            template_dict['create_time'] = now
            template_dict['update_time'] = now
            template_dict['comment'] = '系统内置的默认模板，如果删除请另外指定默认模板，否则无法生成代码！'
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
        return self.cursor.fetchone()

    def get_using_template(self):
        sql = template_sql.get('select') + f' where is_using = 1'
        self.cursor.execute(sql)
        # 理论上只有一个正在使用中
        return self.cursor.fetchone()
