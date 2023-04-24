# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from enum import Enum

from src.constant.template_dialog_constant import CONFIG_INPUT_WIDGET_TYPE_DICT
from src.logger.log import logger as log
from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic, transactional, get_db_conn

_author_ = 'luwt'
_date_ = '2023/3/9 8:46'


table_name = 'template_config'

sql_dict = {
    'create': f'''create table if not exists {table_name} 
    (id integer primary key autoincrement,
    template_id integer not null,
    config_name char(50) not null,
    config_type integer not null,
    output_var_name char(50),
    config_value_widget char(20) not null,
    is_required integer not null,
    config_desc text,
    placeholder_text text,
    default_value text,
    range_values text,
    item_order integer not null,
    create_time datetime,
    update_time datetime
    );''',
    'delete_by_template_ids': f'delete from {table_name} where template_id in ',
}


@dataclass
class TemplateConfig(BasicSqliteDTO):
    # 模板id
    template_id: int = field(init=False, default=None)
    # 配置项名称
    config_name: str = field(init=False, default=None)
    # 配置项类型
    config_type: int = field(init=False, default=None)
    # 输出的变量名
    output_var_name: str = field(init=False, default=None)
    # 配置输入项使用的控件，控件名称
    config_value_widget: str = field(init=False, default=None)
    # 是否必填
    is_required: int = field(init=False, default=None)
    # 配置项说明
    config_desc: str = field(init=False, default=None)
    # 占位文本
    placeholder_text: str = field(init=False, default=None)
    # 默认值
    default_value: str = field(init=False, default=None)
    # 控件为下拉框时，下拉列表值，逗号分隔
    range_values: str = field(init=False, default=None)
    # 非数据库字段，统计关联的模板文件列表
    bind_file_list: list = field(init=False, default=None)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class ConfigTypeEnum(Enum):
    # 输出路径
    output_dir = 0
    # 模板变量
    template_var = 1


class RequiredEnum(Enum):
    not_required = 0
    required = 1


class TemplateConfigSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict)

    def get_by_template_id(self, template_id):
        param = TemplateConfig()
        param.template_id = template_id
        config_list = self.select_by_order(param)
        # 根据类型分组
        output_config_list, var_config_list = list(), list()
        for config in config_list:
            if config.config_type == ConfigTypeEnum.output_dir.value:
                output_config_list.append(config)
            elif config.config_type == ConfigTypeEnum.template_var.value:
                var_config_list.append(config)
        return output_config_list, var_config_list

    def batch_add_config_list(self, template_id, output_config_list, var_config_list):
        config_list = [*output_config_list, *var_config_list]
        for idx, config in enumerate(config_list, start=1):
            config.template_id = template_id
            config.item_order = idx
        if config_list:
            self.batch_insert(config_list)
        # 处理关联文件的配置id
        for config in output_config_list:
            if not config.bind_file_list:
                continue
            for file in config.bind_file_list:
                file.output_config_id = config.id

    @transactional
    def batch_edit_config_list(self, template_id, output_config_list, var_config_list):
        # 由于是低频操作，可以简单做，删除原有数据，插入新数据
        self.batch_del_config_list((template_id,))
        # 插入新数据
        self.batch_add_config_list(template_id, output_config_list, var_config_list)

    def batch_del_config_list(self, template_ids):
        ids_str = ','.join(map(lambda x: str(x), template_ids))
        sql = f"{sql_dict.get('delete_by_template_ids')} ({ids_str})"
        get_db_conn().query(sql)
        log.info(f'{self.table_name} 根据 template_ids: {template_ids} 删除')


def get_var_name(var_name_list, order=1):
    var_name = f'var_{order}'
    if var_name in var_name_list:
        return get_var_name(var_name_list, order + 1)
    return var_name


def construct_output_config(config_name_list, var_name_list, file_name):
    config_name = f'{file_name} 输出路径'
    if config_name in config_name_list:
        # 名称重复，不生成
        return
    output_config = TemplateConfig()
    output_config.config_name = config_name
    output_config.config_type = ConfigTypeEnum.output_dir.value
    output_config.output_var_name = get_var_name(var_name_list)
    output_config.config_value_widget = tuple(CONFIG_INPUT_WIDGET_TYPE_DICT)[0]
    output_config.is_required = RequiredEnum.required.value
    output_config.config_desc = f'{file_name} 文件将输出到此路径下'
    return output_config
