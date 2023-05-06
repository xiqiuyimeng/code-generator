# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from src.logger.log import logger as log
from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic, get_db_conn

_author_ = 'luwt'
_date_ = '2023/3/28 10:51'


table_name = 'template_func'

sql_dict = {
    'create': f'''create table if not exists {table_name} 
    (id integer primary key autoincrement,
    func_name text not null,
    func_body text not null,
    item_order integer not null,
    create_time datetime,
    update_time datetime
    );''',
    'drop': f'drop table {table_name}',
}


@dataclass
class TemplateFunc(BasicSqliteDTO):
    # 方法名称
    func_name: str = field(init=False, default=None)
    # 方法体
    func_body: str = field(init=False, default=None)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class TemplateFuncSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict)

    def save_template_func(self, template_func):
        template_func.item_order = self.get_max_order()
        self.insert(template_func)

    def drop_template_func_table(self):
        log.info(f'清空表 {self.table_name}')
        get_db_conn().query(sql_dict.get('drop'))

    def get_all_func(self):
        param = TemplateFunc()
        return self.select_by_order(param)

