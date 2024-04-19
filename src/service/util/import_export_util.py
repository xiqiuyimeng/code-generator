# -*- coding: utf-8 -*-
import dataclasses

from src.constant.template_dialog_constant import CONFIG_INPUT_WIDGET_TYPE_DICT, DEFAULT_INPUT_WIDGET_TYPE
from src.enum.common_enum import check_required_value_legal, RequiredEnum, ConfigTypeEnum
from src.service.util.group_util import group_model_list, add_group_list

_author_ = 'luwt'
_date_ = '2023/5/15 14:11'


def convert_import_to_model(import_model_class, model_class, data):
    # 之所以要经历两次转化，是为了规范数据，第一次先转化为导入导出使用的实体类，可保证与导出时数据结构相同，第二次转化为数据库实体类
    return model_class(**dataclasses.asdict(import_model_class().convert_import(**data)))


def convert_import_to_model_list(import_model_class, model_class, data_list):
    return [convert_import_to_model(import_model_class, model_class, data) for data in data_list]


# ------------------------------ 导入导出类型映射 start ------------------------------ #

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


def batch_save_type_mapping(type_mapping_sqlite, col_type_mapping_sqlite, data_list):
    # 批量保存类型映射
    type_mapping_sqlite.batch_save_type_mappings(data_list)
    # 保存列类型映射组信息
    for type_mapping in data_list:
        if type_mapping.type_mapping_cols:
            col_type_mapping_sqlite.batch_save(type_mapping.type_mapping_cols, type_mapping.id)


def export_type_mapping(type_mapping_sqlite, col_type_mapping_sqlite, type_mapping_ids):
    # 查询类型映射信息
    type_mapping_list = type_mapping_sqlite.export_type_mapping_by_ids(type_mapping_ids)
    if not type_mapping_list:
        raise Exception('未获取到类型映射信息')
    # 根据类型映射id查询类型映射组信息
    col_type_mapping_list = col_type_mapping_sqlite.export_by_parent_ids(type_mapping_ids)
    # 对映射组信息分组
    if col_type_mapping_list:
        col_type_mapping_dict = group_model_list(col_type_mapping_list, lambda x: x.parent_id)
        # 类型映射匹配映射组信息
        for type_mapping in type_mapping_list:
            type_mapping.type_mapping_cols = col_type_mapping_dict.get(type_mapping.id)
    return type_mapping_list


# ------------------------------ 导入导出类型映射 end ------------------------------ #


# ------------------------------ 导入导出模板 start ------------------------------ #

def create_default_file_name(template_file_name_set, default_file_name, start_idx):
    """创建默认的文件名称，尝试创建，如果名称已存在，则将索引值增加，递归创建"""
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


def check_template_func_name(template_func_list):
    # 检查名称是否重复、是否为空
    error_count = 0
    func_name_set = set()
    for template_func in template_func_list:
        # 检查名称是否存在
        if not template_func.func_name:
            error_count += 1
        # 检查名称是否重复
        elif template_func.func_name in func_name_set:
            error_count += 1
        else:
            func_name_set.add(template_func.func_name)
    # 返回检查错误名称的数量，以便上层方法判断处理
    return error_count


def batch_save_template(template_sqlite, template_config_sqlite, template_file_sqlite,
                        template_func_sqlite, template_list):
    # 批量保存模板
    template_sqlite.batch_save_templates(template_list)
    for template in template_list:
        # 保存配置
        template_config_sqlite.batch_add_config_list(template.id, template.output_config_list,
                                                     template.var_config_list)
        # 保存模板文件
        template_file_sqlite.batch_add_template_files(template.id, template.template_files)
        # 保存模板方法
        template_func_sqlite.batch_add_template_func_list(template.id, template.template_func_list)


def export_template(template_sqlite, template_file_sqlite, template_config_sqlite,
                    template_func_sqlite, template_ids):
    # 1. 查询模板信息
    template_list = template_sqlite.export_template_by_ids(template_ids)
    if not template_list:
        raise Exception('未获取到模板信息')
    # 2. 查询模板文件
    template_file_list = template_file_sqlite.export_files_by_parent_id(template_ids)

    # 3. 文件按模板id分组
    template_id_file_dict = group_model_list(template_file_list, lambda x: x.template_id)

    # 4. 文件按output_config_id分组
    template_output_file_dict = group_model_list(template_file_list, lambda x: x.output_config_id)

    # 5. 查询模板配置
    template_config_list = template_config_sqlite.export_config_by_template_ids(template_ids)

    # 6. 配置分类，并将文件关联到对应的输出配置上
    template_id_output_config_dict, template_id_var_config_dict = dict(), dict()
    for config in template_config_list:
        if config.config_type == ConfigTypeEnum.output_dir.value:
            add_group_list(template_id_output_config_dict, lambda x: x.template_id, config)
            # 关联文件
            config.bind_file_list = template_output_file_dict.get(config.id)
        elif config.config_type == ConfigTypeEnum.template_var.value:
            add_group_list(template_id_var_config_dict, lambda x: x.template_id, config)

    # 7. 查询模板方法
    template_func_list = template_func_sqlite.export_func_list_by_template_id(template_ids)

    # 将模板配置、模板文件、模板方法都关联到模板上
    for template in template_list:
        template.output_config_list = template_id_output_config_dict.get(template.id)
        template.var_config_list = template_id_var_config_dict.get(template.id)
        template.template_files = template_id_file_dict.get(template.id)
        template.template_func_list = template_func_list
    return template_list

# ------------------------------ 导入导出模板 end ------------------------------ #
