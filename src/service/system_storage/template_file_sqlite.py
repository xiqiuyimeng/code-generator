# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from enum import Enum

from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic
from src.service.util.dataclass_util import init, import_export
from src.service.util.system_storage_util import Condition, transactional

_author_ = 'luwt'
_date_ = '2023/3/9 8:42'

table_name = 'template_file'

sql_dict = {
    'create': f'''create table if not exists {table_name}
    (id integer primary key autoincrement,
    file_name char(50) not null,
    file_name_template text null,
    file_content text,
    is_current integer not null,
    tab_opened integer not null,
    is_current_tab integer,
    tab_item_order integer,
    output_config_id integer,
    template_id integer not null,
    item_order integer not null,
    create_time datetime,
    update_time datetime
    );''',
}


@init
@dataclass
class TemplateFile(BasicSqliteDTO):
    # 模板文件名称
    file_name: str = field(init=False, default=None)
    # 模板文件名称的模板，用来存放生成模板文件的模板语法
    file_name_template: str = field(init=False, default=None)
    # 模板文件内容
    file_content: str = field(init=False, default=None)
    # 是否是当前项
    is_current: int = field(init=False, default=None)
    # 是否打开了tab页
    tab_opened: int = field(init=False, default=None)
    # 是否是当前tab
    is_current_tab: int = field(init=False, default=None)
    # tab页顺序
    tab_item_order: int = field(init=False, default=None)
    # 文件输出路径配置项id
    output_config_id: int = field(init=False, default=None)
    # 模板id，用来关联文件和模板
    template_id: int = field(init=False, default=None)


@import_export(('template_id', 'output_config_id'))
@dataclass
class ImportExportTemplateFile:
    # 模板文件名称
    file_name: str = field(default=None)
    # 模板文件名称的模板，用来存放生成模板文件的模板语法
    file_name_template: str = field(default=None)
    # 模板文件内容
    file_content: str = field(default=None)
    # 是否是当前项
    is_current: int = field(default=None)
    # 是否打开了tab页
    tab_opened: int = field(default=None)
    # 是否是当前tab
    is_current_tab: int = field(default=None)
    # tab页顺序
    tab_item_order: int = field(default=None)


class CurrentEnum(Enum):
    current = 1
    not_current = 0


class TabOpenedEnum(Enum):
    opened = 1
    not_opened = 0


class TemplateFileSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict, TemplateFile)

    def get_by_template_id(self, template_id):
        condition = Condition(self.table_name).add('template_id', template_id)
        return self.select_by_order(condition=condition)

    def batch_add_template_files(self, template_id, template_files):
        for idx, template_file in enumerate(template_files, start=1):
            template_file.template_id = template_id
            template_file.item_order = idx
        self.batch_insert(template_files)

    @transactional
    def batch_edit_template_files(self, template_id, template_files):
        # 由于是低频操作，可以简单做，删除原有数据，插入新数据
        self.batch_del_template_files((template_id,))
        # 插入新数据
        if template_files:
            self.batch_add_template_files(template_id, template_files)

    def batch_del_template_files(self, template_ids):
        condition = Condition(self.table_name).add('template_id', template_ids, 'in')
        self.delete_by_condition(condition)

    def export_files_by_parent_id(self, template_ids):
        condition = Condition(self.table_name).add('template_id', template_ids, 'in')
        return self.select_by_order(return_type=ImportExportTemplateFile, condition=condition)
