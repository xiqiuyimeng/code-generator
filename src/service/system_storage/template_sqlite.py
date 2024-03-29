# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic
from src.service.util.dataclass_util import init, import_export
from src.service.util.system_storage_util import Condition, SelectCol

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


@init
@dataclass
class Template(BasicSqliteDTO):
    # 模板名称
    template_name: str = field(init=False, default=None)
    # 模板说明
    template_desc: str = field(init=False, default=None)
    # 模板输出路径配置列表
    output_config_list: list = field(init=False, default=None)
    # 模板变量配置列表
    var_config_list: list = field(init=False, default=None)
    # 模板文件列表
    template_files: list = field(init=False, default=None)
    # 模板方法列表
    template_func_list: list = field(init=False, default=None)

    def get_name(self):
        return self.template_name


@import_export(('id',))
@dataclass
class ImportExportTemplate:
    # 模板名称
    template_name: str = field(default=None)
    # 模板说明
    template_desc: str = field(default=None)
    # 模板输出路径配置列表
    output_config_list: list = field(default=None)
    # 模板变量配置列表
    var_config_list: list = field(default=None)
    # 模板文件列表
    template_files: list = field(default=None)
    # 模板方法列表
    template_func_list: list = field(init=False, default=None)


class TemplateSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict, Template)

    def get_template_by_id(self, template_id):
        condition = Condition(self.table_name).add('id', template_id)
        return self.select_one(condition=condition)

    def save_template(self, template):
        template.item_order = self.get_max_order()
        self.insert(template)

    def export_template_by_ids(self, template_ids):
        select_col = SelectCol(self.table_name).add('id').add('template_name').add('template_desc')
        condition = Condition(self.table_name).add('id', template_ids, 'in')
        return self.select_by_order(return_type=ImportExportTemplate, select_cols=select_col, condition=condition)

    def get_all_names(self):
        select_col = SelectCol(self.table_name).add('template_name')
        rows = self.select_by_order(select_cols=select_col)
        return [row.template_name for row in rows]

    def get_id_by_names(self, template_list):
        select_col = SelectCol(self.table_name).add('id')
        template_names = [template.template_name for template in template_list]
        condition = Condition(self.table_name).add('template_name', template_names, 'in')
        rows = self.select_by_order(select_cols=select_col, condition=condition)
        return [row.id for row in rows]

    def batch_save_templates(self, template_list):
        max_order = self.get_max_order()
        for order, template in enumerate(template_list, start=max_order):
            template.item_order = order
        self.batch_insert(template_list)

    def get_template_by_ids(self, template_ids):
        condition = Condition(self.table_name).add('id', template_ids, 'in')
        return self.select_by_order(condition=condition)
