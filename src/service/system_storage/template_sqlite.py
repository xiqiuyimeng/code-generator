# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from src.logger.log import logger as log
from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic, get_db_conn
from src.service.util.dataclass_util import init, import_export

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
    'export': f'select id, template_name, template_desc from {table_name} where id in ',
    'select_all_names': f'select template_name from {table_name}',
    'get_id_by_names': f'select id from {table_name} where template_name in ',
}


@init
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

    def get_name(self):
        return self.template_name


@import_export(('id',))
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

    def get_all_names(self):
        sql = sql_dict.get('select_all_names')
        rows = get_db_conn().query(sql)
        log.info(f'{self.table_name} 获取所有模板名称')
        return [row.get('template_name') for row in rows.as_dict()]

    def get_id_by_names(self, template_list):
        name_str = ','.join([f'"{template.template_name}"' for template in template_list])
        sql = f"{sql_dict.get('get_id_by_names')} ({name_str})"
        rows = get_db_conn().query(sql)
        log.info(f'{self.table_name} 根据名称查询id')
        return [row.get('id') for row in rows.as_dict()]

    def batch_save_templates(self, template_list):
        max_order = self.get_max_order()
        for order, template in enumerate(template_list, start=max_order):
            template.item_order = order
        self.batch_insert(template_list)
