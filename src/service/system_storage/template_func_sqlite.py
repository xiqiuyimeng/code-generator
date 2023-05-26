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
    'select_all_names': f'select func_name from {table_name}',
    'delete_by_names': f'delete from {table_name} where func_name in ',
    'export_by_ids': f'select func_name, func_body from {table_name} where id in ',
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

    def get_name(self):
        return self.func_name


@dataclass
class ImportExportTemplateFunc:
    # 方法名称
    func_name: str = field(init=False, default=None)
    # 方法体
    func_body: str = field(init=False, default=None)

    def convert_import(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
        return self

    def convert_export(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
        return self


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

    def get_all_names(self):
        sql = sql_dict.get('select_all_names')
        rows = get_db_conn().query(sql)
        log.info(f'{self.table_name} 获取所有模板方法名称')
        return [row.get('func_name') for row in rows.as_dict()]

    def batch_save_template_funcs(self, template_func_list):
        max_order = self.get_max_order()
        for order, template_func in enumerate(template_func_list, start=max_order):
            template_func.item_order = order
        self.batch_insert(template_func_list)

    def batch_delete_by_names(self, template_func_list):
        name_list_str = ','.join([f'"{template_func.func_name}"' for template_func in template_func_list])
        sql = f'{sql_dict.get("delete_by_names")} ({name_list_str})'
        log.info(f'{self.table_name} 根据名称删除模板方法')
        get_db_conn().query(sql)

    def export_template_func_by_ids(self, template_func_ids):
        id_str = ','.join([str(func_id) for func_id in template_func_ids])
        sql = f'{sql_dict.get("export_by_ids")} ({id_str})'
        rows = get_db_conn().query(sql)
        log.info(f'{self.table_name} 根据id导出模板方法')
        return [ImportExportTemplateFunc().convert_export(**row) for row in rows.as_dict()]
