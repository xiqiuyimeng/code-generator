# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from enum import Enum

from src.logger.log import logger as log
from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic, get_db_conn, transactional

_author_ = 'luwt'
_date_ = '2023/3/9 8:42'


table_name = 'template_file'

sql_dict = {
    'create': f'''create table if not exists {table_name}
    (id integer primary key autoincrement,
    file_name char(50) not null,
    file_name_template text not null,
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
    'delete_by_template_ids': f'delete from {table_name} where template_id in ',
}


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

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class CurrentEnum(Enum):
    current = 1
    not_current = 0


class TabOpenedEnum(Enum):
    opened = 1
    not_opened = 0


class TemplateFileSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict)

    def get_by_template_id(self, template_id):
        param = TemplateFile()
        param.template_id = template_id
        return self.select_by_order(param)

    def batch_add_template_files(self, template_id, template_files):
        for idx, template_file in enumerate(template_files, start=1):
            template_file.template_id = template_id
            template_file.item_order = idx
        self.batch_insert(template_files)

    @transactional
    def batch_edit_template_files(self, template_id, template_files):
        # 由于是低频操作，可以简单做，删除原有数据，插入新数据
        self.batch_del_template_files((template_id, ))
        # 插入新数据
        if template_files:
            self.batch_add_template_files(template_id, template_files)

    def batch_del_template_files(self, template_ids):
        ids_str = ','.join(map(lambda x: str(x), template_ids))
        sql = f"{sql_dict.get('delete_by_template_ids')} ({ids_str})"
        get_db_conn().query(sql)
        log.info(f'{self.table_name} 根据 template_ids: {template_ids} 删除')
