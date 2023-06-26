# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from enum import Enum

from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic
from src.service.util.dataclass_util import init, import_export
from src.service.util.system_storage_util import Condition, transactional

_author_ = 'luwt'
_date_ = '2023/3/28 10:51'

table_name = 'template_func'

sql_dict = {
    'create': f'''create table if not exists {table_name} 
    (id integer primary key autoincrement,
    func_name text not null,
    func_body text not null,
    template_id integer not null,
    is_current integer not null,
    checked integer not null,
    item_order integer not null,
    create_time datetime,
    update_time datetime
    );''',
    'get_template_ids': f'select distinct template_id from {table_name}',
}


@init
@dataclass
class TemplateFunc(BasicSqliteDTO):
    # 方法名称
    func_name: str = field(init=False, default=None)
    # 方法体
    func_body: str = field(init=False, default=None)
    # 模板id
    template_id: int = field(init=False, default=None)
    # 是否是当前项
    is_current: int = field(init=False, default=None)
    # 选中状态
    checked: int = field(init=False, default=None)

    def get_name(self):
        return self.func_name


# 类装饰器，需要接收参数，所以这里需要加括号，如果不加括号，wrapper方法将无法获取到类对象
@import_export(('template_id',))
@dataclass
class ImportExportTemplateFunc:
    # 方法名称
    func_name: str = field(default=None)
    # 方法体
    func_body: str = field(default=None)
    # 是否是当前项
    is_current: int = field(default=None)
    # 选中状态
    checked: int = field(default=None)


class CurrentEnum(Enum):
    current_func = 1
    not_current_func = 0


class TemplateFuncSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict, TemplateFunc)

    def get_by_template_id(self, template_id):
        condition = Condition(self.table_name).add('template_id', template_id)
        return self.select_by_order(condition=condition)

    def batch_add_template_func_list(self, template_id, template_func_list):
        if not template_func_list:
            return
        for idx, template_func in enumerate(template_func_list, start=1):
            template_func.template_id = template_id
            template_func.item_order = idx
        self.batch_insert(template_func_list)

    @transactional
    def batch_edit_template_func_list(self, template_id, template_func_list):
        # 先删除，再插入
        self.batch_del_template_func_list((template_id,))
        # 插入新数据
        self.batch_add_template_func_list(template_id, template_func_list)

    def batch_del_template_func_list(self, template_ids):
        condition = Condition(self.table_name).add('template_id', template_ids, 'in')
        self.delete_by_condition(condition)

    def export_func_list_by_template_id(self, template_ids):
        condition = Condition(self.table_name).add('template_id', template_ids, 'in')
        return self.select_by_order(return_type=ImportExportTemplateFunc, condition=condition)

    def select_distinct_template_ids(self):
        row_list = self.select_by_condition(select_cols=sql_dict.get('get_template_ids'))
        return [(dict(row).get('template_id')) for row in row_list]
