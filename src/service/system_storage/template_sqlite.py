# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from src.logger.log import logger as log
from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic, get_db_conn

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
    'export': f'select id, template_name, template_desc from {table_name} where id in '
}


@dataclass
class Template(BasicSqliteDTO):
    # 模板名称
    template_name: str = field(init=False, default=None)
    # 模板说明
    template_desc: str = field(init=False, default=None)
    # 模板文件列表
    template_files: list = field(init=False, default=None)
    # 模板输出路径配置列表
    output_config_list: list = field(init=False, default=None)
    # 模板变量配置列表
    var_config_list: list = field(init=False, default=None)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


@dataclass
class ImportExportTemplate:
    # 模板名称
    template_name: str = field(default=None)
    # 模板说明
    template_desc: str = field(default=None)
    # 模板文件列表
    template_files: list = field(default=None)
    # 模板输出路径配置列表
    output_config_list: list = field(default=None)
    # 模板变量配置列表
    var_config_list: list = field(default=None)

    def convert_import(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
        return self

    def convert_export(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k) or k == 'id':
                setattr(self, k, v)
        return self


class TemplateSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict)

    def save_template(self, template):
        template.item_order = self.get_max_order()
        self.insert(template)

    def export_template_by_ids(self, template_ids):
        id_str = ','.join([str(template_id) for template_id in template_ids])
        sql = f'{sql_dict.get("export")} ({id_str})'
        rows = get_db_conn().query(sql)
        log.info(f'{self.table_name} 根据id导出模板信息')
        return [ImportExportTemplate().convert_export(**row) for row in rows.as_dict()]
