# -*- coding: utf-8 -*-
import os
import re
import sqlite3
from collections import namedtuple
from datetime import datetime

from src.sys.sys_info_storage.sqlite_abc import SqliteBasic

_author_ = 'luwt'
_date_ = '2020/9/15 11:03'


# 模板对象：id，模板名称，java模板java_tp, mapper模板mapper_tp, xml模板xml_tp,
# service模板service_tp, service_impl模板service_impl_tp, controller模板controller_tp
# 类型：0 内置，1 自定义。使用次数，可根据次数排序, is_using：是否在使用中，0否 1是
# 创建时间 更新时间，时间都以时间戳形式存储，取出后再转为格式化字符串
Template = namedtuple('Template', 'id tp_name java_tp mapper_tp xml_tp service_tp '
                                  'service_impl_tp controller_tp type use_times is_using '
                                  'create_time update_time')


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
    update_time integer not null
    );''',
    'insert': 'insert into template ',
    'delete': 'delete from template where id = ?',
    'batch_delete': 'delete from template where tp_name in ',
    'update_selective': 'update template set ',
    'select': 'select * from template',
    'select_templates': 'select tp_name, case type when 0 then "系统内置" when 1 then "自定义" end as type , '
                        'use_times, case is_using when 0 then "否" when 1 then "是" end as is_using, '
                        'create_time, update_time from template',
    'select_name_exist': 'select count(*) > 0 from template where tp_name = ?',
    'select_max_name_end': 'select tp_name from template where tp_name like ? order by id desc limit 1',
    'reset_using': 'update template set is_using = 0 where is_using = 1',
    'using_template': 'update template set is_using = 1 where tp_name = ?'
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
    if set(result.keys()) <= set(Template._fields):
        # 初始化一个空的template字典
        template_dict = Template(*((None,) * len(Template._fields)))._asdict()
        # 将有值的部分进行更新
        template_dict.update(result)
        # 转化为template类型返回
        return Template(**template_dict)
    return tuple(zip(result.values()))


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

    def insert(self, mapping_dict):
        now = round(datetime.now().timestamp())
        mapping_dict['create_time'] = now
        mapping_dict['update_time'] = now
        mapping_dict['is_using'] = 0
        mapping_dict['type'] = 1
        mapping_dict['use_times'] = 0
        super().insert(Template(**mapping_dict))

    def update_selective(self, mapping_dict):
        mapping_dict['update_time'] = round(datetime.now().timestamp())
        super().update_selective(Template(**mapping_dict))

    def get_templates(self, tp_type=None):
        sql = template_sql.get('select_templates')
        if tp_type is not None:
            sql += f' where type = {tp_type}'
        self.cursor.execute(sql + ' order by use_times desc')
        return self.cursor.fetchall()

    def init_template(self, template_dict):
        """初始化模板"""
        using_template = self.get_using_template()
        template_dict['id'] = None
        template_dict['tp_name'] = '默认模板'
        template_dict['type'] = 0
        template_dict['use_times'] = 0
        template_dict['is_using'] = 1 if not using_template else 0
        now = round(datetime.now().timestamp())
        # 时间以时间戳形式存储
        template_dict['create_time'] = now
        template_dict['update_time'] = now
        super().insert(Template(**template_dict))

    def check_tp_name_available(self, tp_name, tp_id=None):
        sql = template_sql.get('select_name_exist')
        if tp_id:
            sql += f' and id != {tp_id}'
        self.cursor.execute(sql, (tp_name, ))
        data = self.cursor.fetchone()
        return data[0][0] == 0

    def select_tp_name_max_end(self, tp_name):
        sql = template_sql.get('select_max_name_end')
        self.cursor.execute(sql, (tp_name + '%', ))
        return self.cursor.fetchone()

    def get_template(self, tp_name):
        sql = template_sql.get('select') + f' where tp_name = ?'
        self.cursor.execute(sql, (tp_name, ))
        return self.cursor.fetchone()

    def get_template_refresh_table(self, tp_name):
        sql = template_sql.get("select_templates") + f' where tp_name = ?'
        self.cursor.execute(sql, (tp_name, ))
        return self.cursor.fetchone()

    def get_using_template(self):
        sql = template_sql.get('select') + f' where is_using = 1'
        self.cursor.execute(sql)
        # 理论上只有一个正在使用中
        return self.cursor.fetchone()

    def get_available_name(self, template):
        # 首先判断当前名字是否是copy后的，如果是，去查询相似名字时需要去掉-copy后缀，
        # 否则直接以当前名字查询相似名字
        search = re.search(r"(?<=-copy)\d+$", template.tp_name)
        # 假定当前模板名称为无后缀名称
        none_suffix_name = template.tp_name
        if search:
            # 如果能匹配到，截取出无后缀名称（去掉-copy数字）
            none_suffix_name = template.tp_name[: search.span()[0] - 5]
        # 在数据库中查询后缀最大的名称
        max_suffix_name = self.select_tp_name_max_end(none_suffix_name).tp_name
        # 再次匹配查出的名称，若能匹配到，将后缀数字加1，否则直接加后缀
        max_suffix_search = re.search(r"(?<=-copy)\d+$", max_suffix_name)
        if max_suffix_search:
            tp_name = re.sub(r"(?<=-copy)\d+$", str(int(max_suffix_search.group()) + 1), max_suffix_name)
        else:
            tp_name = max_suffix_name + "-copy1"
        return tp_name

    def batch_copy(self, tp_names):
        # 根据名称找到需要复制的模板
        sql = template_sql.get('select') + f" where tp_name in ({', '.join('?' * len(tp_names))})"
        self.cursor.execute(sql, tp_names)
        templates = self.cursor.fetchall()
        new_templates = list()
        for template in templates:
            tp_name = self.get_available_name(template)
            new_template_dict = {
                'id': None,
                'tp_name': tp_name,
            }
            template_dict = template._asdict()
            template_dict.update(new_template_dict)
            self.insert(template_dict)
            select_sql = template_sql.get('select_templates') + f' where tp_name = ?'
            self.cursor.execute(select_sql, (tp_name, ))
            new_templates.append(self.cursor.fetchone())
        return new_templates

    def batch_delete(self, tp_names):
        sql = template_sql.get('batch_delete') + f"({','.join('?' * len(tp_names))})"
        self.cursor.execute(sql, tp_names)
        self.conn.commit()

    def change_using_template(self, tp_name):
        """改变使用中的模板，先将之前使用中的模板置为未使用，再将新模板置为使用中"""
        sql = template_sql.get('reset_using')
        self.cursor.execute(sql)
        self.conn.commit()
        # 置为使用中
        using_sql = template_sql.get('using_template')
        self.cursor.execute(using_sql, (tp_name, ))
        self.conn.commit()



