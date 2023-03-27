# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic

_author_ = 'luwt'
_date_ = '2023/3/8 18:03'


table_name = 'template'

sql_dict = {
    'create': f'''create table if not exists {table_name} 
    (id integer primary key autoincrement,
    template_name char(50) not null,
    template_desc text,
    item_order integer not null,
    create_time datetime,
    update_time datetime
    );''',
}


@dataclass
class Template(BasicSqliteDTO):
    # 模板名称
    template_name: str = field(init=False, default=None)
    # 模板说明
    template_desc: str = field(init=False, default=None)
    # 模板文件列表
    template_files: list = field(init=False, default=None)
    # 模板输入配置列表
    template_config_list: list = field(init=False, default=None)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class TemplateSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict)

    def save_template(self, template):
        template.item_order = self.get_max_order()
        self.insert(template)
