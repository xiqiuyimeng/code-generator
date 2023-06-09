# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from src.logger.log import logger as log
from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic
from src.service.util.dataclass_util import init, import_export
from src.service.util.system_storage_util import get_cursor, SelectCol, Condition

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


@init
@dataclass
class TemplateFunc(BasicSqliteDTO):
    # 方法名称
    func_name: str = field(init=False, default=None)
    # 方法体
    func_body: str = field(init=False, default=None)

    def get_name(self):
        return self.func_name


# 类装饰器，需要接收参数，所以这里需要加括号，如果不加括号，wrapper方法将无法获取到类对象
@import_export()
@dataclass
class ImportExportTemplateFunc:
    # 方法名称
    func_name: str = field(init=False, default=None)
    # 方法体
    func_body: str = field(init=False, default=None)


class TemplateFuncSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict, TemplateFunc)

    def save_template_func(self, template_func):
        template_func.item_order = self.get_max_order()
        self.insert(template_func)

    def drop_template_func_table(self):
        log.info(f'清空表 {self.table_name}')
        get_cursor().execute(sql_dict.get('drop'))

    def get_all_func(self):
        return self.select_by_order()

    def get_all_names(self):
        select_col = SelectCol(self.table_name).add('func_name')
        rows = self.select_by_order(select_cols=select_col)
        return [row.func_name for row in rows]

    def batch_save_template_funcs(self, template_func_list):
        max_order = self.get_max_order()
        for order, template_func in enumerate(template_func_list, start=max_order):
            template_func.item_order = order
        self.batch_insert(template_func_list)

    def batch_delete_by_names(self, template_func_list):
        func_names = [template_func.func_name for template_func in template_func_list]
        condition = Condition(self.table_name).add('func_name', func_names, 'in')
        self.delete_by_condition(condition)

    def export_template_func_by_ids(self, template_func_ids):
        select_col = SelectCol(self.table_name).add('func_name').add('func_body')
        condition = Condition(self.table_name).add('id', template_func_ids, 'in')
        return self.select_by_order(return_type=ImportExportTemplateFunc, select_cols=select_col, condition=condition)
