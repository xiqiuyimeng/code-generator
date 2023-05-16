# -*- coding: utf-8 -*-
import dataclasses

from src.constant.template_dialog_constant import CONFIG_INPUT_WIDGET_TYPE_DICT, DEFAULT_INPUT_WIDGET_TYPE
from src.service.system_storage.template_config_sqlite import RequiredEnum, check_required_value_legal

_author_ = 'luwt'
_date_ = '2023/5/15 14:11'


def convert_import_to_model(import_model_class, model_class, data):
    # 之所以要经历两次转化，是为了规范数据，第一次先转化为导入导出使用的实体类，可保证与导出时数据结构相同，第二次转化为数据库实体类
    return model_class(**dataclasses.asdict(import_model_class().convert_import(**data)))


def convert_import_to_model_list(import_model_class, model_class, data_list):
    return [convert_import_to_model(import_model_class, model_class, data) for data in data_list]


def add_group_list(group_dict, get_group_key, data):
    key = get_group_key(data)
    data_group_list = group_dict.get(key)
    # 如果之前没存储过，那么创建list
    if data_group_list is None:
        data_group_list = list()
        group_dict[key] = data_group_list
    data_group_list.append(data)


def group_model_list(data_list, get_group_key):
    model_list_dict = dict()
    for data in data_list:
        add_group_list(model_list_dict, get_group_key, data)
    return model_list_dict


def check_repair_type_mapping_group_num(mapping_col_group_dict):
    for group_idx, group_num in enumerate(sorted(mapping_col_group_dict)):
        # 如果组号不对，更新组号
        if group_idx != group_num:
            error_group_list = mapping_col_group_dict.get(group_num)
            for group_col in error_group_list:
                group_col.group_num = group_idx
            # 将元素移动到 group_idx 组内
            if mapping_col_group_dict.get(group_idx) is None:
                mapping_col_group_dict[group_idx] = error_group_list
            else:
                mapping_col_group_dict[group_idx].extend(error_group_list)
            # 删除原有组
            del mapping_col_group_dict[group_num]


def create_default_file_name(template_file_name_set, default_file_name, start_idx):
    current_file_name = default_file_name.format(start_idx)
    if current_file_name in template_file_name_set:
        return create_default_file_name(template_file_name_set, default_file_name, start_idx + 1)
    return current_file_name


def check_duplicate_template_file_name(template_files):
    duplicate_file_name_count = 0
    template_file_name_set, empty_name_file_list = set(), list()
    for file in template_files:
        if not file.file_name:
            empty_name_file_list.append(file)
        elif file.file_name in template_file_name_set:
            duplicate_file_name_count += 1
        else:
            template_file_name_set.add(file.file_name)
    # 如果文件名称存在空的情况，给予一个默认值
    if empty_name_file_list:
        default_file_name, start_idx = '模板文件-系统创建-{}', 1
        for empty_name_file in empty_name_file_list:
            empty_name_file.file_name = create_default_file_name(template_file_name_set,
                                                                 default_file_name, start_idx)
    return duplicate_file_name_count


def repair_template_config(config, config_type):
    # 配置类型修正
    config.config_type = config_type
    # 变量控件类型校验，如果类型不对，那么重置为一个默认类型
    if config.config_value_widget not in CONFIG_INPUT_WIDGET_TYPE_DICT:
        config.config_value_widget = DEFAULT_INPUT_WIDGET_TYPE
    # 是否必填，如果当前值不合法，重置为必填
    if not check_required_value_legal(config.is_required):
        config.is_required = RequiredEnum.required.value


def check_template_config(config_list, config_type):
    error_name_count, error_var_name_count = 0, 0
    config_name_list, var_name_list = list(), list()
    for config in config_list:
        # 配置名称不可重复
        if config.config_name in config_name_list:
            error_name_count += 1
        else:
            config_name_list.append(config.config_name)
        # 输出变量名称不可重复
        if config.output_var_name in var_name_list:
            error_var_name_count += 1
        else:
            var_name_list.append(config.output_var_name)
        # 修正配置数据
        repair_template_config(config, config_type)
    return error_name_count, error_var_name_count
